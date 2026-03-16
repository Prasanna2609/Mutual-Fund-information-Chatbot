import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables early
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Debugging print and startup check
api_key = os.getenv("GROQ_API_KEY")
if not api_key or "your_" in api_key:
    print("⚠️ WARNING: GROQ_API_KEY is missing or contains a placeholder!")
else:
    # Print prefix/suffix for verification
    prefix = api_key[:6]
    suffix = api_key[-4:]
    print(f"✅ Loaded GROQ_API_KEY: {prefix}...{suffix}")

if not api_key:
    raise ValueError("GROQ_API_KEY is not set. Check your .env file.")

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from phase_6_llm_response.rag_chain import RAGChain
from phase_5_retrieval_pipeline.search_pipeline import run_retrieval_pipeline

app = FastAPI(title="Mutual Fund RAG Chatbot API")

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with your Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str


class SourceItem(BaseModel):
    scheme_name: str
    url: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceItem] = []

# Initialize RAG Chain
chain = RAGChain()

@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    query_text = request.question
    if not query_text:

        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        # Get the structured answer and sources from the RAG chain
        result = chain.query(query_text)
        
        return QueryResponse(answer=result["answer"], sources=result["sources"])
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
