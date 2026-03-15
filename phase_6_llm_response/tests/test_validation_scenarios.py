import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

load_dotenv()

from phase_6_llm_response.rag_chain import RAGChain
from phase_6_llm_response.prompt_template import ADVISORY_REFUSAL_MESSAGE

def test_validation_scenarios():
    chain = RAGChain()
    
    # Test 1: Garbage Query
    print("\n--- Test 1: Garbage Query ---")
    q1 = "kbvksdnvsdl"
    res1 = chain.query(q1)
    print(f"Query: {q1}")
    print(f"Answer: {res1['answer']}")
    print(f"Sources: {res1['sources']}")
    assert "I could not find any relevant information" in res1['answer']
    assert len(res1['sources']) == 0
    
    # Test 2: Irrelevant (Hello World)
    print("\n--- Test 2: Irrelevant Query ---")
    q2 = "hello world"
    res2 = chain.query(q2)
    print(f"Query: {q2}")
    print(f"Answer: {res2['answer']}")
    print(f"Sources: {res2['sources']}")
    assert "I could not find any relevant information" in res2['answer']
    assert len(res2['sources']) == 0

    # Test 3: Advisory Refusal
    print("\n--- Test 3: Advisory Refusal ---")
    q3 = "Which fund should I invest in?"
    res3 = chain.query(q3)
    print(f"Query: {q3}")
    print(f"Answer: {res3['answer']}")
    print(f"Sources: {res3['sources']}")
    assert ADVISORY_REFUSAL_MESSAGE in res3['answer']
    assert len(res3['sources']) == 0

    # Test 4: Single Fund (NAV)
    print("\n--- Test 4: Single Fund (NAV) ---")
    q4 = "What is the NAV of SBI Bluechip Fund?"
    res4 = chain.query(q4)
    print(f"Query: {q4}")
    print(f"Answer: {res4['answer']}")
    print(f"Sources: {res4['sources']}")
    # Assuming SBI Bluechip exists in dataset
    if "I could not find any relevant information" not in res4['answer']:
        assert len(res4['sources']) >= 1
        assert any("SBI Bluechip" in s['scheme_name'] for s in res4['sources'])

    # Test 6: AMC Only Query
    print("\n--- Test 6: AMC Only Query ---")
    q6 = "SBI"
    res6 = chain.query(q6)
    print(f"Query: {q6}")
    print(f"Sources Count: {len(res6['sources'])}")
    if len(res6['sources']) > 0:
        assert any("SBI" in s['scheme_name'] for s in res6['sources'])

    # Test 7: Direct Metadata Overview
    print("\n--- Test 7: Direct Metadata Overview ---")
    q7 = "list all funds"
    res7 = chain.query(q7)
    print(f"Query: {q7}")
    print(f"Answer starts with: {res7['answer'][:100]}...")
    assert "complete list of mutual funds" in res7['answer']
    assert "**Large Cap**" in res7['answer'] or "**Mid Cap**" in res7['answer']
    assert len(res7['sources']) == 0

if __name__ == "__main__":

    try:
        test_validation_scenarios()
        print("\n✅ All validation scenarios passed!")
    except Exception as e:
        print(f"\n❌ Validation failed: {e}")
        import traceback
        traceback.print_exc()
