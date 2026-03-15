"""
Tests for Phase 5 Retrieval Pipeline
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from phase_5_retrieval_pipeline.retriever import MutualFundRetriever
from phase_5_retrieval_pipeline.search_pipeline import run_retrieval_pipeline
from phase_5_retrieval_pipeline.scheme_detector import detect_scheme, ALIAS_MAPPING
from phase_1_project_setup.config import RETRIEVER_K

def test_retriever_initialization():
    print("Testing retriever initialization...")
    try:
        retriever = MutualFundRetriever()
        assert retriever.vector_store is not None, "Vector store failed to load"
        print("✓ Retriever initialized and index loaded.")
    except Exception as e:
        print(f"✗ Initialization failed: {e}")
        assert False

def test_semantic_search():
    print(f"Testing semantic search (returning top {RETRIEVER_K} results)...")
    query = "performance of Nippon India Small Cap"
    results = run_retrieval_pipeline(query)
    
    # 1. Check count
    assert len(results) == RETRIEVER_K, f"Expected {RETRIEVER_K} results, got {len(results)}"
    
    # 2. Check metadata preservation
    first_result = results[0]
    required_fields = ["chunk_text", "scheme_name", "amc", "category", "source_url"]
    for field in required_fields:
        assert field in first_result, f"Field '{field}' missing in retrieval result"
    
    assert "Nippon India Small Cap" in first_result["scheme_name"], "Retrieved result does not match query scheme"
    
    print(f"✓ Semantic search returned relevant results for: {first_result['scheme_name']}")
    print(f"✓ All required metadata fields are present: {required_fields}")

def test_scheme_aware_retrieval():
    print("Testing scheme-aware retrieval...")
    query = "What is the NAV of SBI Bluechip Fund?"
    results = run_retrieval_pipeline(query)

    assert len(results) > 0, "No results returned for SBI Bluechip Fund query"

    # Every result must belong to SBI Bluechip Fund
    for i, res in enumerate(results):
        assert res["scheme_name"] == "SBI Bluechip Fund Direct Growth", \
            f"Result {i+1} has wrong scheme: '{res['scheme_name']}' (expected 'SBI Bluechip Fund Direct Growth')"

    print(f"✓ All {len(results)} results correctly belong to 'SBI Bluechip Fund Direct Growth'")

def test_alias_detection():
    print("Testing alias detection...")
    known_schemes = [
        "SBI Bluechip Fund Direct Growth",
        "HDFC Top 100 Fund Direct Growth",
        "Nippon India Small Cap Fund Direct Growth"
    ]
    
    # 1. Test exact alias match
    query1 = "What is the NAV for SBI Large Cap?"
    scheme1 = detect_scheme(query1, known_schemes)
    assert scheme1 == "SBI Bluechip Fund Direct Growth", f"Expected SBI Bluechip Fund Direct Growth, got {scheme1}"
    
    # 2. Test another alias match
    query2 = "Tell me about hdfc large cap performance"
    scheme2 = detect_scheme(query2, known_schemes)
    assert scheme2 == "HDFC Top 100 Fund Direct Growth", f"Expected HDFC Top 100 Fund Direct Growth, got {scheme2}"
    
    # 3. Test conventional matching still works
    query3 = "What is the NAV of Nippon India Small Cap?"
    scheme3 = detect_scheme(query3, known_schemes)
    assert scheme3 == "Nippon India Small Cap Fund Direct Growth", f"Expected Nippon India Small Cap Fund Direct Growth, got {scheme3}"

    print("✓ Alias detection works correctly")
    print("✓ Conventional matching fallback works correctly")
    
if __name__ == "__main__":
    print("--- Running Phase 5 Tests ---")
    try:
        test_retriever_initialization()
        test_semantic_search()
        test_scheme_aware_retrieval()
        test_alias_detection()
        print("--- Phase 5 Testing Complete ---")
    except Exception as e:
        print(f"✗ Tests failed: {e}")
        sys.exit(1)

