"""
Tests for Phase 4 Embeddings and Vector Store
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from phase_4_embeddings_vectorstore.vector_store import load_vector_store, get_embedding_model
from phase_1_project_setup.config import PROCESSED_CHUNKS_PATH, FAISS_INDEX_PATH
import json

def test_embeddings_generation():
    print("Testing embedding model initialization...")
    model = get_embedding_model()
    test_text = "Mutual fund investment is subject to market risks."
    embedding = model.embed_query(test_text)
    
    assert isinstance(embedding, list), "Embedding should be a list"
    assert len(embedding) > 0, "Embedding should not be empty"
    print(f"✓ Embeddings model works (vector dimension: {len(embedding)})")

def test_vector_store_persistence():
    print("Testing FAISS index loading and integrity...")
    
    # 1. Check if files exist
    assert FAISS_INDEX_PATH.exists(), "FAISS index directory does not exist"
    assert (FAISS_INDEX_PATH / "index.faiss").exists(), "index.faiss file missing"
    assert (FAISS_INDEX_PATH / "index.pkl").exists(), "index.pkl file missing"
    
    # 2. Load the store
    vector_store = load_vector_store()
    
    # 3. Verify counts
    with open(PROCESSED_CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    
    # FAISS LangChain implementation uses index.ntotal
    vector_count = vector_store.index.ntotal
    assert vector_count == len(chunks), f"Vector count mismatch! FAISS: {vector_count}, JSON: {len(chunks)}"
    print(f"✓ FAISS index count ({vector_count}) matches chunk count exactly.")

    # 4. Verify metadata retrieval (brief check)
    # Perform a dummy search
    results = vector_store.similarity_search("SBI Large Cap", k=1)
    assert len(results) > 0, "Similarity search returned no results"
    assert "scheme_name" in results[0].metadata, "Metadata missing in retrieved results"
    print(f"✓ Metadata retrieval verified for: {results[0].metadata['scheme_name']}")

if __name__ == "__main__":
    print("--- Running Phase 4 Tests ---")
    try:
        test_embeddings_generation()
        test_vector_store_persistence()
        print("--- Phase 4 Testing Complete ---")
    except Exception as e:
        print(f"✗ Tests failed: {e}")
        sys.exit(1)
