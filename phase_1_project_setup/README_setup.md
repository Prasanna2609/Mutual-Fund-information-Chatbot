# RAG Mutual Fund FAQ Bot - Setup Instructions

This document explains how to prepare your development environment for the RAG Mutual Fund FAQ Chatbot.

## Required Python Version
- Python 3.9 or higher is recommended.

## 1. Create a Virtual Environment (Optional but recommended)
It is best practice to use a virtual environment to manage dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

## 2. Install Dependencies
Install all the core dependencies required for the project (including scraping, embeddings, retrieval, and UI):
```bash
pip install -r phase_1_project_setup/requirements.txt
```

## 3. Configure Environment Variables
This project requires a Groq API key to run the LLM inference.

1. Copy the example environment file:
   ```bash
   cp phase_1_project_setup/.env.example phase_1_project_setup/.env
   ```
2. Open `phase_1_project_setup/.env` in your text editor.
3. Add your Groq API key (which you can get from https://console.groq.com/keys):
   ```env
   GROQ_API_KEY=your_actual_api_key_here
   ```

## Note on Folder Structure
This project is strictly divided into 9 phases. Do not mix files across phases. Each phase is documented in its respective directory. The central configuration for all phases is exported from `phase_1_project_setup/config.py`.

### Architecture Overview
- **Phase 1-4**: Data Ingestion Pipeline (Scraping -> Cleaning -> Embedding -> Indexing)
- **Phase 5-7**: Query Pipeline (Retrieval -> Classification -> LLM Generation -> API)
- **Phase 8**: Frontend Web UI
- **Phase 9**: Data Refresh Scheduler (Daily automation of Phase 2-4)

