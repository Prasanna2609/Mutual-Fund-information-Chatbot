"""
vector_store.py
Manages the FAISS vector database: initialization, storage, and persistence.
"""

import os
import sys
from pathlib import Path
import torch
import torch.nn as nn
import sys
import builtins
builtins.nn = nn
sys.modules['torch'] = torch
sys.modules['torch.nn'] = nn
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from phase_1_project_setup.config import FAISS_INDEX_PATH, EMBEDDING_MODEL_NAME

def get_embedding_model():
    """Initializes and returns the HuggingFace embedding model."""
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={'device': 'cpu'}
    )

def create_and_save_vector_store(texts, metadatas):
    """
    Creates a FAISS index from texts and metadata, then persists it locally.
    """
    embeddings = get_embedding_model()
    
    # Initialize FAISS from documents
    vector_store = FAISS.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas
    )
    
    # Persist the index
    # Ensure directory exists
    FAISS_INDEX_PATH.mkdir(parents=True, exist_ok=True)
    vector_store.save_local(str(FAISS_INDEX_PATH))
    print(f"✓ FAISS index saved successfully to {FAISS_INDEX_PATH}")
    return vector_store

def load_vector_store():
    """Loads the persisted FAISS index from local storage."""
    if not FAISS_INDEX_PATH.exists():
        raise FileNotFoundError(f"FAISS index not found at {FAISS_INDEX_PATH}")
        
    embeddings = get_embedding_model()
    return FAISS.load_local(str(FAISS_INDEX_PATH), embeddings, allow_dangerous_deserialization=True)
