"""
refresh_pipeline.py
Orchestrates the full data refresh process from scraping to re-indexing.
Designed to be run as a daily cron job.
"""

import sys
import logging
from pathlib import Path
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# Import logic from other phases
from phase_1_project_setup.config import RAW_DATA_PATH
from phase_2_data_collection.scrape_groww_pages import scrape_and_save
from phase_3_document_processing.chunk_documents import process_and_chunk
from phase_4_embeddings_vectorstore.create_embeddings import run_embeddings_pipeline

# Configure Logging
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "refresh_pipeline.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

def run_refresh_pipeline():
    start_time = datetime.now()
    logging.info("Starting Data Refresh Pipeline...")

    try:
        # Step 1: Phase 2 - Scraping
        logging.info("--- Step 1: Phase 2 - Scraping Groww Pages ---")
        csv_file_path = str(PROJECT_ROOT / "phase_2_data_collection" / "groww_urls.csv")
        scrape_and_save(csv_file_path, str(RAW_DATA_PATH))
        logging.info("Scraping completed successfully.")

        # Step 2: Phase 3 - Document Processing & Chunking
        logging.info("--- Step 2: Phase 3 - Document Processing & Chunking ---")
        process_and_chunk()
        logging.info("Document processing and chunking completed successfully.")

        # Step 3: Phase 4 - Embeddings & FAISS Index Update
        logging.info("--- Step 3: Phase 4 - Generating Embeddings & Updating Index ---")
        run_embeddings_pipeline()
        logging.info("Index update completed successfully.")

        end_time = datetime.now()
        duration = end_time - start_time
        logging.info(f"Full Data Refresh Pipeline completed in {duration}.")
        print(f"\n✅ Refresh successful! Pipeline duration: {duration}")

    except Exception as e:
        logging.error(f"Pipeline failed at step {logging.getLogger().name}: {e}")
        logging.exception("Detailed Traceback:")
        print(f"\n❌ Refresh failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_refresh_pipeline()
