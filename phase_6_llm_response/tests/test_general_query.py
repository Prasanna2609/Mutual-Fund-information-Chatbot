import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from phase_6_llm_response.rag_chain import RAGChain
from phase_5_retrieval_pipeline.search_pipeline import run_retrieval_pipeline

query = "list all funds"
print(f"User: {query}\n")

# Let's peek at the retrieved context
results = run_retrieval_pipeline(query)
print("\n--- Retrieved Schemes ---")
for r in results:
    print(f"- {r['scheme_name']}")

chain = RAGChain()
print(f"\nBot:\n{chain.query(query)}\n")
