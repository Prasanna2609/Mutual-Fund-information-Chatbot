"""
retriever.py
Loads the FAISS vector store and implements the core retrieval function.
"""

import sys
from pathlib import Path
from typing import List
import torch
import torch.nn as nn

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from phase_1_project_setup.config import RETRIEVER_K
from phase_4_embeddings_vectorstore.vector_store import load_vector_store

class MutualFundRetriever:
    """
    Handles the loading of FAISS and semantic search for mutual fund queries.
    """
    def __init__(self):
        self.vector_store = load_vector_store()
        self._known_schemes = None
        print("✓ FAISS Vector Store loaded into retriever.")

    def get_known_schemes(self) -> List[str]:
        """
        Extracts and caches all unique scheme names from the FAISS docstore.
        """
        if self._known_schemes is None:
            schemes = set()
            docstore = self.vector_store.docstore
            for doc_id in docstore._dict:
                doc = docstore._dict[doc_id]
                scheme = doc.metadata.get("scheme_name", "")
                if scheme:
                    schemes.add(scheme)
            self._known_schemes = sorted(schemes)
            print(f"✓ Loaded {len(self._known_schemes)} known scheme names.")
        return self._known_schemes

    def get_known_schemes_with_categories(self) -> dict:
        if not hasattr(self, "_known_schemes_cats") or self._known_schemes_cats is None:
            schemes = {}
            docstore = self.vector_store.docstore
            for doc_id in docstore._dict:
                doc = docstore._dict[doc_id]
                scheme = doc.metadata.get("scheme_name", "")
                cat = doc.metadata.get("category", "Uncategorized")
                if scheme:
                    schemes[scheme] = cat
            self._known_schemes_cats = schemes
        return self._known_schemes_cats

    def get_relevant_chunks(self, query: str, k: int = RETRIEVER_K):
        """
        Accepts a user query and returns the top-k most relevant chunks.
        """
        # FAISS similarity_search handles embedding the query and searching the index
        return self.vector_store.similarity_search(query, k=k)

    def get_relevant_chunks_filtered(self, query: str, scheme_name: str, k: int = RETRIEVER_K):
        """
        Retrieves top-k chunks filtered to a specific scheme_name.
        Over-fetches candidates from FAISS, then filters by metadata match.
        """
        # Over-fetch to have enough candidates after filtering
        candidates = self.vector_store.similarity_search(query, k=k * 3)

        # Filter to only chunks from the target scheme
        filtered = [
            doc for doc in candidates
            if doc.metadata.get("scheme_name") == scheme_name
        ]

        # Return top-k filtered results (may be fewer than k if not enough matches)
        return filtered[:k]
