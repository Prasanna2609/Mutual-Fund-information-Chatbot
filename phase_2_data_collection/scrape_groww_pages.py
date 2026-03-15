"""
scrape_groww_pages.py
Loads URLs from CSV, fetches the pages with browser headers, extracts text, 
and saves to phase_2_data_collection/raw_documents.json.
"""
import csv
import json
import logging
import sys
from pathlib import Path
import requests

# Add project root to path for config import
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# Import config merely for root references if needed, but RAW_DATA_PATH is now inside Phase 2
from phase_1_project_setup.config import RAW_DATA_PATH
from phase_2_data_collection.page_loader import extract_all

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Set robust headers to bypass basic bot protection returning 404s
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

def load_urls(csv_path: str):
    """Reads the groww_urls.csv and returns a list of dictionaries with all fields."""
    urls = []
    try:
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'scheme_name' in row and 'url' in row:
                    urls.append({
                        "scheme_name": row["scheme_name"].strip(),
                        "amc": row.get("amc", "Unknown AMC").strip(),
                        "category": row.get("category", "Unknown Category").strip(),
                        "url": row["url"].strip()
                    })
    except Exception as e:
        logging.error(f"Error reading CSV {csv_path}: {e}")
    return urls

def scrape_and_save(csv_path: str, output_path: str):
    """Main scraping orchestrator."""
    urls = load_urls(csv_path)
    if not urls:
        logging.error("No URLs loaded. Exiting.")
        return

    documents = []
    
    for item in urls:
        scheme_name = item["scheme_name"]
        url = item["url"]
        amc = item["amc"]
        category = item["category"]
        
        logging.info(f"Fetching: {scheme_name}")
        
        try:
            # Use a slightly longer timeout and standard browser headers
            response = requests.get(url, headers=HEADERS, timeout=15)
            
            if response.status_code == 200:
                # requests automatically handles gzip and brotli if libraries are present
                # response.text should be decoded correctly
                html_content = response.text
                
                # Double check for binary characters that shouldn't be in HTML text
                if '\u0000' in html_content:
                    logging.warning(f"Detected null bytes in {scheme_name}. Attempting fallback decoding.")
                    html_content = response.content.decode('utf-8', errors='ignore')

                text_content, financial_data = extract_all(html_content)
                
                doc_entry = {
                    "scheme_name": scheme_name,
                    "amc": amc,
                    "category": category,
                    "source_url": url,
                    "text": text_content
                }
                # Merge financial data points into the entry
                doc_entry.update(financial_data)
                
                documents.append(doc_entry)
                logging.info(f"Successfully extracted {len(text_content)} characters and {len(financial_data)} financial metrics.")
            else:
                logging.error(f"Failed to fetch {url}. Status code: {response.status_code}")
                
        except requests.RequestException as e:
            logging.error(f"Request error for {url}: {e}")

    # Ensure parent dir exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Save the JSON
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(documents, f, indent=4, ensure_ascii=False)
        logging.info(f"Saved {len(documents)} documents to {output_path}")
    except Exception as e:
        logging.error(f"Failed to save JSON: {e}")

if __name__ == "__main__":
    csv_file_path = str(Path(__file__).parent / "groww_urls.csv")
    scrape_and_save(csv_file_path, str(RAW_DATA_PATH))
