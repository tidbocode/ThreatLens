# ThreatLens
LangChain-powered threat intelligence Q&A agent.

Ingest threat reports, advisories, and IOC files, then ask natural-language questions about threat actors, TTPs, CVEs, and malware.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env          # add your OPENAI_API_KEY
```

## Usage

**Ingest documents** (PDF, TXT, MD) from the `data/` directory:
```bash
python main.py ingest
python main.py ingest --path /path/to/reports
```

**Ask a single question:**
```bash
python main.py ask "What TTPs does APT29 use?"
python main.py ask "List IOCs associated with Cobalt Strike beacons"
```

**Interactive chat:**
```bash
python main.py chat
```

## Project structure

```
ThreatLens/
├── data/                    # drop threat intel documents here
├── chroma_db/               # vector store (auto-created on first ingest)
├── src/threatlens/
│   ├── config.py            # env-based configuration
│   ├── ingest.py            # document loading and embedding
│   └── agent.py             # RAG chain
├── main.py                  # CLI entry point
├── requirements.txt
└── .env.example
```

## Configuration

All settings can be overridden in `.env`:

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | — | Required |
| `MODEL_NAME` | `gpt-4o` | Chat model |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | Embedding model |
| `CHROMA_PATH` | `./chroma_db` | Vector store path |
| `DATA_DIR` | `./data` | Default ingest directory |
| `CHUNK_SIZE` | `1000` | Characters per chunk |
| `CHUNK_OVERLAP` | `200` | Overlap between chunks |
| `RETRIEVAL_K` | `5` | Documents retrieved per query |
