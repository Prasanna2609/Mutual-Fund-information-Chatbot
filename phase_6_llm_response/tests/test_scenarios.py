import sys
import json
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from phase_6_llm_response.rag_chain import RAGChain

def test_scenarios():
    chain = RAGChain()
    
    scenarios = [
        ("Test 1: Garbage Query", "kbvksdnvsdl"),
        ("Test 2: Single-Fund Query", "What is the NAV of SBI Bluechip Fund?"),
        ("Test 3: Multi-Fund Query", "Show me all SBI mutual funds"),
        ("Test 4: Advisory Query", "Which fund should I invest in?")
    ]

    for name, query in scenarios:
        print(f"\n{'-'*50}")
        print(f"{name}")
        print(f"Query: {query}")
        result = chain.query(query)
        print(f"\nAnswer:\n{result['answer']}")
        print("\nSources:")
        if not result['sources']:
            print("  (No sources returned)")
        else:
            for src in result['sources']:
                print(f"  - {src['scheme_name']} -> {src['url']}")
        print(f"{'-'*50}")

if __name__ == "__main__":
    test_scenarios()
