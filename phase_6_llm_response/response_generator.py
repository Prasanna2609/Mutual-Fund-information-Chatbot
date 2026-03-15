import os
import sys
from pathlib import Path
from groq import Groq

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from phase_6_llm_response.prompt_template import SYSTEM_PROMPT, FALLBACK_MESSAGE

class ResponseGenerator:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set. Check your .env file.")
        
        self.client = Groq(api_key=api_key)
        self.model = os.getenv("LLM_MODEL_NAME", "llama3-8b-8192")

    def generate_response(self, query: str, context_chunks: list) -> str:
        """
        Formats the context and query, then calls Groq LLM.
        """
        if not context_chunks:
            return FALLBACK_MESSAGE

        # Prepare context
        context_text = "\n\n".join([c["chunk_text"] for c in context_chunks])


        # Format full prompt
        prompt = SYSTEM_PROMPT.format(context=context_text, query=query)

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                temperature=0.0, # Keep it factual
                max_tokens=256
            )
            
            answer = chat_completion.choices[0].message.content.strip()
            
            return answer
        except Exception as e:
            return f"Error generating response: {e}"
