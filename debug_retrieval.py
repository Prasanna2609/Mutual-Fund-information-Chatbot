import os
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from phase_6_llm_response.rag_chain import RAGChain

def test_debug():
    chain = RAGChain()
    query = "info about SBI funds"
    print(f"Testing query: {query}")
    answer = chain.query(query)
    print(f"Result: {answer}")

if __name__ == "__main__":
    try:
        test_debug()
    except Exception as e:
        import traceback
        traceback.print_exc()
