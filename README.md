# RAG Mutual Fund Information Chatbot

A comprehensive RAG (Retrieval-Augmented Generation) based chatbot designed to provide accurate information about mutual funds, including NAV, returns, AUM, and more.

## Architecture Overview

The project is structured into 9 logical phases:

- **Phase 1: Project Setup**: Environment configuration and core dependencies.
- **Phase 2: Data Collection**: Web scraper for mutual fund data from Groww.
- **Phase 3: Document Processing**: Cleaning and chunking of scraped HTML content.
- **Phase 4: Embeddings & Vector Store**: Semantic embedding generation and FAISS index management.
- **Phase 5: Retrieval Pipeline**: Contextual search and scheme detection logic.
- **Phase 6: LLM Response**: Query classification, prompt engineering, and RAG orchestration.
- **Phase 7: Backend API**: FastAPI server for the chatbot backend.
- **Phase 8: Frontend Web**: React-based user interface with premium design.
- **Phase 9: Data Refresh Scheduler**: Daily automation for dataset updates and re-indexing.

## Setup & Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Prasanna2609/Mutual-Fund-information-Chatbot.git
   cd Mutual-Fund-information-Chatbot
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   Create a `.env` file in the root with your credentials:
   ```env
   GROQ_API_KEY=your_key_here
   ```

4. **Run the Backend**:
   ```bash
   python phase_7_backend_api/api_server.py
   ```

5. **Run the Frontend**:
   ```bash
   cd phase_8_frontend_web
   npm install
   npm run dev
   ```

## Key Features
- **Strict Query Routing**: Prevents hallucination on irrelevant queries.
- **Direct Overviews**: Metadata-based fund listings for maximum accuracy.
- **Automated Refresh**: Daily data updates via cron.
- **Premium UI**: Modern, responsive design with source citations.
