import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Info } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import './index.css';

interface SourceItem {
  scheme_name: string;
  url: string;
}

interface Message {
  id: number;
  type: 'user' | 'bot';
  text: string;
  sources?: SourceItem[];
}

// Groww Logo SVG: Exact match from screenshot
const GrowwLogo = () => (
  <svg width="44" height="44" viewBox="0 0 44 44" fill="none" xmlns="http://www.w3.org/2000/svg">
    <g clipPath="url(#clip0)">
      {/* Background Circle */}
      <circle cx="22" cy="22" r="22" fill="#5367FF" />

      {/* Turquoise Wavy Section (Bottom) */}
      <path
        d="M0 22L7 28L14 24L20 18L28 22L36 28L44 22V44H0V22Z"
        fill="#00D09C"
      />

      {/* High-fidelity wave/graph line */}
      <path
        d="M0 22L7 28L14 24L20 18L28 22L36 28L44 22"
        stroke="#00D09C"
        strokeWidth="1.5"
        strokeLinejoin="round"
      />
    </g>
    <defs>
      <clipPath id="clip0">
        <circle cx="22" cy="22" r="22" />
      </clipPath>
    </defs>
  </svg>
);

const App: React.FC = () => {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      type: 'bot',
      text: "Welcome to the Mutual Fund Facts Assistant. I can provide factual data like NAV, expense ratios, and historical returns from Groww. How can I help you today?",
    }
  ]);
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    if (!query.trim() || loading) return;

    const userMessage: Message = {
      id: Date.now(),
      type: 'user',
      text: query
    };

    setMessages(prev => [...prev, userMessage]);
    setQuery('');
    setLoading(true);

    try {
      const baseUrl = import.meta.env.VITE_API_URL?.replace(/\/$/, '') || '';
      const response = await axios.post(`${baseUrl}/ask`, {
        question: userMessage.text
      });


      const botMessage: Message = {
        id: Date.now() + 1,
        type: 'bot',
        text: response.data.answer,
        sources: response.data.sources
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error: any) {
      console.error("Chat error:", error);
      const serverError = error.response?.data?.detail || "Information currently unavailable. Please check if the backend service is active.";
      const errorMessage: Message = {
        id: Date.now() + 1,
        type: 'bot',
        text: `Error: ${serverError}`,
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  // Helper removed as we now use ReactMarkdown

  return (
    <>
      <header>
        <div className="logo-container">
          <GrowwLogo />
          <span className="logo-text">Groww</span>
        </div>
        <div style={{ marginLeft: '12px', height: '24px', width: '1px', background: '#E5E7EB' }}></div>
        <h1 style={{ fontSize: '18px', fontWeight: 600, color: '#1E1E1E' }}>Mutual Fund Facts Assistant</h1>
      </header>

      <div className="chat-container" ref={scrollRef}>
        {messages.map((m) => (
          <div key={m.id} className={`message ${m.type}`}>
            <div className="markdown-body">
              {m.type === 'bot' ? (
                <ReactMarkdown>
                  {m.text}
                </ReactMarkdown>
              ) : (
                m.text
              )}
            </div>
            {m.sources && m.sources.length > 0 && (
              <div className="sources-container" style={{ marginTop: '16px', paddingTop: '12px', borderTop: '1px solid #E5E7EB' }}>
                <div style={{ fontSize: '12px', fontWeight: 600, color: '#374151', marginBottom: '8px' }}>Sources:</div>
                <ul style={{ listStyleType: 'disc', paddingLeft: '20px', margin: 0 }}>
                  {m.sources.map((src, idx) => (
                    <li key={idx} style={{ marginBottom: '4px' }}>
                      <a 
                        href={src.url} 
                        target="_blank" 
                        rel="noopener noreferrer" 
                        style={{ color: '#5367FF', textDecoration: 'none', fontSize: '13px', fontWeight: 500 }}
                        onMouseOver={(e) => (e.currentTarget.style.textDecoration = 'underline')}
                        onMouseOut={(e) => (e.currentTarget.style.textDecoration = 'none')}
                      >
                        {src.scheme_name} — {src.url}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            )}

          </div>
        ))}
        {loading && (
          <div className="typing-indicator">
            <Info size={14} className="animate-pulse" />
            Assistant is retrieving facts...
          </div>
        )}
      </div>

      <div className="input-area-wrapper">
        <div className="input-container">
          <input
            type="text"
            placeholder="Search mutual fund facts (e.g. SBI Bluechip NAV)"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          />
          <button className="send-btn" onClick={handleSend} disabled={loading || !query.trim()}>
            <Send size={18} />
          </button>
        </div>
        <p style={{ marginTop: '12px', fontSize: '11px', color: '#6B7280', textAlign: 'center' }}>
          This assistant provides factual data only. Not intended as investment advice.
        </p>
      </div>
    </>
  );
};

export default App;
