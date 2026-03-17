"""
search_pipeline.py
Wraps the retriever to return structured retrieval results for any given query.
Supports scheme-aware retrieval when a mutual fund name is detected in the query.
"""

import torch
import torch.nn as nn

import sys
from pathlib import Path
from typing import List, Dict, Any

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from phase_5_retrieval_pipeline.retriever import MutualFundRetriever
from phase_5_retrieval_pipeline.scheme_detector import detect_scheme

# Module-level singleton to avoid re-loading FAISS on every call
_retriever = None

def _get_retriever() -> MutualFundRetriever:
    global _retriever
    if _retriever is None:
        _retriever = MutualFundRetriever()
    return _retriever

def run_retrieval_pipeline(query: str) -> List[Dict[str, Any]]:
    """
    End-to-end retrieval function: query -> scheme detection -> semantic search -> structured results.
    If a scheme name is detected in the query, results are filtered to that scheme.
    """
    retriever = _get_retriever()

    # Step 1: Detect if the query mentions a specific scheme
    known_schemes = retriever.get_known_schemes()
    detected_scheme = detect_scheme(query, known_schemes)

    # Step 2: Retrieve — filtered or unfiltered
    if detected_scheme:
        print(f"🎯 Scheme detected: '{detected_scheme}' — using filtered retrieval.")
        results = retriever.get_relevant_chunks_filtered(query, detected_scheme)
    else:
        print("🔍 No specific scheme detected — using standard retrieval.")
        results = retriever.get_relevant_chunks(query)

    # Step 3: Structure results
    structured_results = []

    for doc in results:
        structured_results.append({
            "chunk_text": doc.page_content,
            "scheme_name": doc.metadata.get("scheme_name"),
            "amc": doc.metadata.get("amc"),
            "category": doc.metadata.get("category"),
            "source_url": doc.metadata.get("source_url"),
            "nav": doc.metadata.get("nav"),
            "expense_ratio": doc.metadata.get("expense_ratio")
        })
        
    return structured_results

if __name__ == "__main__":
    # Quick manual test
    test_query = "What is the NAV of SBI Bluechip Fund?"
    print(f"Testing query: {test_query}")
    results = run_retrieval_pipeline(test_query)
    
    for i, res in enumerate(results):
        print(f"\nResult {i+1}:")
        print(f"Scheme: {res['scheme_name']}")
        print(f"Text Snippet: {res['chunk_text'][:200]}...")

