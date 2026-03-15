import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

# --- API Keys ---
# Reading Groq API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# --- Project Paths ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Phase Outputs
RAW_DATA_PATH = PROJECT_ROOT / "phase_2_data_collection" / "raw_documents.json"
PROCESSED_CHUNKS_PATH = PROJECT_ROOT / "phase_3_document_processing" / "processed_chunks.json"

# Phase 4 Vector Store Path
FAISS_INDEX_PATH = PROJECT_ROOT / "phase_4_embeddings_vectorstore" / "faiss_index"

# --- Model Configurations ---
# Groq Chat Model
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "llama-3.3-70b-versatile")

# HuggingFace Embeddings Model
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")

# --- Document Processing Configuration ---
# Default parameters for document chunking
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

# --- Retrieval Configuration ---
# Number of chunks to retrieve
RETRIEVER_K = int(os.getenv("RETRIEVER_K", "5"))
