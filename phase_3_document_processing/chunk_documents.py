"""
chunk_documents.py
Splits each cleaned document into smaller text chunks using the configurations from Phase 1.
Preserves metadata across chunks and outputs them to processed_chunks.json.
"""

import json
import logging
import sys
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from phase_1_project_setup.config import RAW_DATA_PATH, PROCESSED_CHUNKS_PATH, CHUNK_SIZE, CHUNK_OVERLAP
from phase_3_document_processing.document_cleaner import clean_text

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def process_and_chunk():
    """Reads raw JSON, cleans each document, chunks it, and writes chunks with metadata to JSON."""
    if not RAW_DATA_PATH.exists():
        logging.error(f"Raw data file not found at {RAW_DATA_PATH}. Please run Phase 2 first.")
        return

    # 1. Load Data
    try:
        with open(RAW_DATA_PATH, "r", encoding="utf-8") as f:
            raw_documents = json.load(f)
        logging.info(f"Loaded {len(raw_documents)} raw documents.")
    except Exception as e:
        logging.error(f"Failed to load raw documents: {e}")
        return

    # 2. Configure Splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )

    all_chunks = []
    
    # 3. Process each document
    for doc_idx, doc in enumerate(raw_documents):
        scheme_name = doc.get("scheme_name", "Unknown Scheme")
        amc = doc.get("amc", "Unknown AMC")
        category = doc.get("category", "Unknown Category")
        source_url = doc.get("source_url", "Unknown URL")
        raw_text = doc.get("text", "")
        
        # Clean text
        cleaned_text = clean_text(raw_text)
        
        # Split text into chunks
        raw_chunks = text_splitter.split_text(cleaned_text)
        
        for i, chunk_text in enumerate(raw_chunks):
            # Create a base metadata dict from the original document minus the text
            chunk_metadata = {k: v for k, v in doc.items() if k != "text"}
            
            # Add/Override specific chunk tracking fields
            chunk_metadata.update({
                "doc_id": f"doc_{doc_idx}",
                "chunk_id": f"doc_{doc_idx}_chunk_{i}",
                "text": chunk_text
            })
            all_chunks.append(chunk_metadata)

        logging.info(f"Processed '{scheme_name}': generated {len(raw_chunks)} chunks.")

    # 4. Save Chunks
    try:
        # Ensure parent director exists
        Path(PROCESSED_CHUNKS_PATH).parent.mkdir(parents=True, exist_ok=True)
        
        with open(PROCESSED_CHUNKS_PATH, "w", encoding="utf-8") as f:
            json.dump(all_chunks, f, indent=4, ensure_ascii=False)
        logging.info(f"Saved a total of {len(all_chunks)} processed chunks to {PROCESSED_CHUNKS_PATH}")
    except Exception as e:
        logging.error(f"Failed to save processed chunks: {e}")

if __name__ == "__main__":
    process_and_chunk()
