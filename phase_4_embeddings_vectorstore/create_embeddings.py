"""
create_embeddings.py
Loads processed chunks, generates embeddings, and stores them in FAISS.
"""

import json
import sys
from pathlib import Path
import torch
import torch.nn as nn

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from phase_1_project_setup.config import PROCESSED_CHUNKS_PATH
from phase_4_embeddings_vectorstore.vector_store import create_and_save_vector_store

def run_embeddings_pipeline():
    """Main execution function to process chunks into vectors."""
    if not PROCESSED_CHUNKS_PATH.exists():
        print(f"Error: Processed chunks not found at {PROCESSED_CHUNKS_PATH}. Please run Phase 3 first.")
        return

    # 1. Load Chunks
    try:
        with open(PROCESSED_CHUNKS_PATH, "r", encoding="utf-8") as f:
            chunks = json.load(f)
        print(f"Loaded {len(chunks)} chunks from Phase 3.")
    except Exception as e:
        print(f"Failed to load chunks: {e}")
        return

    if not chunks:
        print("No chunks found in the file.")
        return

    # 2. Extract texts and metadata
    texts = [chunk["text"] for chunk in chunks]
    # Remove 'text' from metadata to avoid redundancy in the store
    metadatas = [{k: v for k, v in chunk.items() if k != "text"} for chunk in chunks]

    # 3. Create and Save Vector Store
    print("Generating embeddings and creating FAISS index (this may take a moment)...")
    create_and_save_vector_store(texts, metadatas)
    print("✓ Phase 4 process complete.")

if __name__ == "__main__":
    run_embeddings_pipeline()
