"""
Tests for Phase 3 Document Processing
"""
import sys
import json
from pathlib import Path

# Add project root to python path to allow imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from phase_1_project_setup.config import PROCESSED_CHUNKS_PATH, CHUNK_SIZE
from phase_3_document_processing.document_cleaner import clean_text

def test_clean_text():
    print("Testing document cleaner...")
    dirty_text = "This   has \n\n\n\n\n way too    many           spaces\x00. NAV is 145.2. Exit Load is 1%."
    clean = clean_text(dirty_text)
    
    assert "   " not in clean, "Multiple spaces not stripped"
    assert "\n\n\n" not in clean, "Multiple newlines not stripped"
    assert "\x00" not in clean, "Non-printable characters not stripped"
    assert "This has" in clean, "Text was mangled"
    assert "NAV is 145.2." in clean, "NAV information was incorrectly stripped"
    assert "Exit Load is 1%." in clean, "Exit load info was incorrectly stripped"
    
    print("✓ document_cleaner cleans redundant whitespace successfully while preserving meaning")

def test_json_structure():
    print(f"Testing processed JSON structure at {PROCESSED_CHUNKS_PATH}...")
    if PROCESSED_CHUNKS_PATH.exists():
        try:
            with open(PROCESSED_CHUNKS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            assert isinstance(data, list), "processed_chunks.json should contain a list of objects"
            
            if len(data) > 0:
                first = data[0]
                assert "doc_id" in first, "doc_id missing in JSON"
                assert "chunk_id" in first, "chunk_id missing in JSON"
                assert "scheme_name" in first, "scheme_name missing in JSON"
                assert "amc" in first, "amc missing in JSON"
                assert "category" in first, "category missing in JSON"
                assert "source_url" in first, "source_url missing in JSON"
                assert "text" in first, "text missing in JSON"
                
                # Verify chunk length constraints roughly (might be slightly over depending on the language boundary)
                # But LangChain should strictly enforce this
                for c in data:
                    assert len(c["text"]) <= CHUNK_SIZE + 200, f"Chunk was significantly larger than max configuration limit: {len(c['text'])}"
                
            print(f"✓ JSON validation passed! File exists with {len(data)} chunks and all required metadata fields.")
            
        except Exception as e:
            print(f"✗ Failed JSON validation: {e}")
            sys.exit(1)
    else:
        print(f"⚠ {PROCESSED_CHUNKS_PATH} does not exist yet. Run chunk_documents.py first.")

if __name__ == "__main__":
    print("--- Running Phase 3 Tests ---")
    test_clean_text()
    test_json_structure()
    print("--- Phase 3 Testing Complete ---")
