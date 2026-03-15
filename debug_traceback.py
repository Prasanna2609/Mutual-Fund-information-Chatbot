import sys
from pathlib import Path
import traceback

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT))

# Import required tools directly to isolate the issue
try:
    from phase_5_retrieval_pipeline.search_pipeline import run_retrieval_pipeline
    
    query = "info about SBI funds"
    print(f"Testing direct retrieval for: {query}")
    
    # We want the error to bubble up here
    results = run_retrieval_pipeline(query)
    print("Retrieval successful.")
    
except NameError as ne:
    print("\n--- NameError Captured ---")
    traceback.print_exc()
except Exception as e:
    print(f"\n--- Other Error Captured: {type(e).__name__} ---")
    traceback.print_exc()
