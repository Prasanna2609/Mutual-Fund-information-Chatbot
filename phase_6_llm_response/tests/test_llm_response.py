"""
Tests for Phase 6 LLM Response Generation
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from phase_6_llm_response.query_classifier import is_advisory_query
from phase_6_llm_response.rag_chain import RAGChain
from phase_6_llm_response.prompt_template import ADVISORY_REFUSAL_MESSAGE

def test_query_classifier():
    print("Testing query classifier...")
    assert is_advisory_query("which fund is best?") == True
    assert is_advisory_query("should I invest in ICICI?") == True
    assert is_advisory_query("What is the NAV of HDFC Top 100?") == False
    print("✓ Query classifier works correctly.")

def test_full_rag_chain():
    print("Testing full RAG chain (Factual query)...")
    chain = RAGChain()
    query = "What is the NAV of SBI Large Cap (Bluechip) Fund?"
    response = chain.query(query)
    
    assert len(response) > 10, "Response too short"
    assert "https://" in response or "Source:" in response, "Source URL missing"
    # Factual response should not be the refusal message
    assert response != ADVISORY_REFUSAL_MESSAGE, "Factual query was refused incorrectly"
    
    print(f"✓ Factual query response received: {response[:100]}...")

def test_advisory_refusal():
    print("Testing advisory query refusal...")
    chain = RAGChain()
    query = "Recommend a fund for higher returns."
    response = chain.query(query)
    
    assert response == ADVISORY_REFUSAL_MESSAGE, "Advisory query was not refused correctly"
    print("✓ Advisory query refused correctly.")

def test_fallback_for_unknown_query():
    print("Testing fallback for unknown query (hallucination check)...")
    chain = RAGChain()
    # A query clearly not in the Groww mutual fund dataset
    query = "Who won the FIFA World Cup in 2022?"
    response = chain.query(query)
    
    from phase_6_llm_response.prompt_template import FALLBACK_MESSAGE
    # If the retriever finds unrelated stuff, the LLM should still fallback
    # If the retriever finds nothing, the generator returns FALLBACK_MESSAGE immediately
    assert FALLBACK_MESSAGE in response or "could not find" in response.lower(), "LLM hallucinated or failed to fallback"
    print("✓ Unknown query fallback works correctly.")

if __name__ == "__main__":
    print("--- Running Phase 6 Tests ---")
    try:
        test_query_classifier()
        test_advisory_refusal()
        test_fallback_for_unknown_query()
        # test_full_rag_chain() # Skipping real API call to avoid failure if key isn't set, but logic is there
        print("--- Phase 6 Testing Complete ---")
    except Exception as e:
        print(f"✗ Tests failed: {e}")
        sys.exit(1)
