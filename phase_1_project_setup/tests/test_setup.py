import sys
from pathlib import Path

# Add project root to python path to allow imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from phase_1_project_setup.config import (
    GROQ_API_KEY,
    DATA_DIR,
    LLM_MODEL_NAME,
    CHUNK_SIZE,
    RETRIEVER_K
)

def test_config_loads():
    print("Testing Phase 1 Configuration...")
    
    # Test Data Directory Creation
    assert DATA_DIR.exists(), f"Data directory {DATA_DIR} was not created!"
    print("✓ Data directory exists")
    
    # Test Constants are loaded
    assert LLM_MODEL_NAME == "llama3-8b-8192", "LLM Model Name is incorrect"
    assert CHUNK_SIZE == 1000, "Chunk size is incorrect"
    assert RETRIEVER_K == 3, "Retriever K is incorrect"
    print("✓ Constants loaded successfully")

    # Warn if API key is not set, but don't fail the project setup test
    if not GROQ_API_KEY:
        print("⚠ WARNING: GROQ_API_KEY is not set in the .env file. Please add it before Phase 6.")
    else:
        print("✓ GROQ_API_KEY is present")
        
    print("\nPhase 1 Setup functionality passed successfully!")

if __name__ == "__main__":
    test_config_loads()
