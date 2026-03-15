"""
Tests for Phase 2 Data Collection
"""
import sys
import os
from pathlib import Path
import json
import requests

# Add project root to python path to allow imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from phase_1_project_setup.config import RAW_DATA_PATH
from phase_2_data_collection.page_loader import extract_readable_text
from phase_2_data_collection.scrape_groww_pages import load_urls, HEADERS

def test_page_loader():
    print("Testing page loader...")
    dummy_html = """
    <html>
        <head><title>Test Page</title><style>body { color: red; }</style></head>
        <body>
            <nav>Menu Items</nav>
            <main>
                <h1>Groww Mutual Fund</h1>
                <p>This is a test mutual fund description.</p>
                <script>console.log("Ignore me");</script>
            </main>
            <footer>Footer Links</footer>
        </body>
    </html>
    """
    text = extract_readable_text(dummy_html)
    
    assert "Ignore me" not in text, "Script tags were not stripped"
    assert "body { color: red; }" not in text, "Style tags were not stripped"
    assert "Groww Mutual Fund" in text, "Main content missing"
    assert "Menu Items" not in text, "Nav tags were not stripped"
    print("✓ page_loader extracts readable text correctly")

def test_url_loading():
    print("Testing CSV loading...")
    csv_path = Path(__file__).resolve().parent.parent / "groww_urls.csv"
    urls = load_urls(str(csv_path))
    
    assert len(urls) > 0, "No URLs were loaded from CSV"
    
    first = urls[0]
    assert "scheme_name" in first, "Missing scheme_name"
    assert "amc" in first, "Missing amc"
    assert "category" in first, "Missing category"
    assert "url" in first, "Missing url"
    assert "http" in first["url"], "URL does not appear to be valid"
    print(f"✓ Successfully loaded {len(urls)} URLs with amc and category fields")

def test_live_request():
    print("Testing live HTTP request with headers...")
    csv_path = Path(__file__).resolve().parent.parent / "groww_urls.csv"
    urls = load_urls(str(csv_path))
    if not urls:
        print("⚠ Skipping live request test: No URLs found.")
        return

    success = False
    for item in urls:
        try:
            response = requests.get(item["url"], headers=HEADERS, timeout=15)
            if response.status_code == 200:
                text = extract_readable_text(response.text)
                if len(text) > 100:
                    print(f"✓ Live request succeeded for {item['url']}! Extracted {len(text)} characters.")
                    success = True
                    break
        except Exception:
            continue
            
    assert success, "All live HTTP requests failed or returned empty text. Groww might be blocking completely."

def test_json_saving():
    print(f"Testing local JSON structure at {RAW_DATA_PATH}...")
    if RAW_DATA_PATH.exists():
        try:
            with open(RAW_DATA_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            assert isinstance(data, list), "raw_documents.json should contain a list of objects"
            
            if len(data) > 0:
                first = data[0]
                assert "scheme_name" in first, "scheme_name missing"
                assert "amc" in first, "amc missing"
                assert "category" in first, "category missing"
                assert "source_url" in first, "source_url missing"
                assert "text" in first, "text missing"
                assert len(first["text"]) > 0, "text shouldn't be empty"
                
            print(f"✓ JSON validation passed! File exists with {len(data)} documents and all 5 required fields.")
        except Exception as e:
            print(f"✗ Failed JSON validation: {e}")
            sys.exit(1)
    else:
        print("⚠ raw_documents.json does not exist yet. Run scrape_groww_pages.py first.")

if __name__ == "__main__":
    print("--- Running Strict Phase 2 Tests ---")
    test_page_loader()
    test_url_loading()
    test_live_request()
    test_json_saving()
    print("--- Phase 2 Testing Complete ---")
