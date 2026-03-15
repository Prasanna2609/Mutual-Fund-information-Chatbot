# Phase 9 Scheduler Configuration

The data refresh pipeline ensures the chatbot always uses the most recent Mutual Fund data (NAV, returns, AUM).

## Recommended Schedule
Mutual fund companies (AMCs) and platforms like Groww typically update factual data like NAV after market hours, once the day's prices are settled.

- **Time**: 22:30 IST (10:30 PM)
- **Frequency**: Daily

## Cron Job Setup

To automate this on a Linux/macOS server, add the following to your crontab (`crontab -e`):

```bash
# Refresh Mutual Fund Data daily at 22:30 IST
30 22 * * * cd /path/to/RAG\ based\ MF\ Chat\ bot && /usr/bin/python3 phase_9_scheduler/refresh_pipeline.py >> logs/cron_output.log 2>&1
```

## Pipeline Flow
1. **Scraper**: Pulls latest HTML content and metrics from list of Groww URLs.
2. **Processor**: Cleans UI noise and breaks documents into searchable chunks.
3. **Indexer**: Re-generates semantic embeddings and updates the local FAISS vector index.

## Logs
Logs for the scheduled runs can be found in `logs/refresh_pipeline.log`.
