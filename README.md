![image](https://github.com/tidbocode/ThreatLens/blob/main/TL-SystemArchitecture.jpg)
# ThreatLens
LangChain-powered threat intelligence Q&A agent — runs fully locally via Ollama.

Pulls live threat feeds (MITRE ATT&CK, ThreatFox, AlienVault OTX), indexes them into a local vector store, and answers natural-language questions about threat actors, TTPs, IOCs, CVEs, and malware.

## Prerequisites

- [Ollama](https://ollama.com) running locally (`ollama serve`)
- Required models pulled:
  ```bash
  ollama pull mistral:7b
  ollama pull nomic-embed-text
  ```

## Setup

**Local**
```bash
pip install -r requirements.txt
cp .env.example .env          # optionally add OTX_API_KEY
```

**Docker**
```bash
cp .env.example .env          # optionally add OTX_API_KEY
docker compose build
```

## Usage

**Ingest live threat feeds** (MITRE ATT&CK + ThreatFox + OTX if key set):
```bash
# local
python main.py ingest

# docker
docker compose run --rm threatlens ingest
```

**Ask a single question:**
```bash
# local
python main.py ask "What TTPs does APT29 use?"

# docker
docker compose run --rm threatlens ask "What TTPs does APT29 use?"
```

**Interactive chat:**
```bash
# local
python main.py chat

# docker
docker compose run --rm threatlens chat
```

## Project structure

```
ThreatLens/
├── chroma_db/               # vector store (auto-created on first ingest)
├── src/threatlens/
│   ├── feeds/
│   │   ├── mitre.py         # MITRE ATT&CK techniques
│   │   ├── abusech.py       # ThreatFox IOCs (last 7 days)
│   │   └── otx.py           # AlienVault OTX pulses (optional)
│   ├── config.py            # env-based configuration
│   ├── ingest.py            # feed ingestion and embedding
│   └── agent.py             # RAG chain (Ollama + Chroma)
├── main.py                  # CLI entry point
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

## Configuration

All settings can be overridden in `.env`:

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `CHAT_MODEL` | `mistral:7b` | Chat model (must be pulled in Ollama) |
| `EMBED_MODEL` | `nomic-embed-text` | Embedding model (must be pulled in Ollama) |
| `OTX_API_KEY` | — | AlienVault OTX key (optional, free at otx.alienvault.com) |
| `CHROMA_PATH` | `./chroma_db` | Vector store path |
| `CHUNK_SIZE` | `500` | Characters per chunk |
| `CHUNK_OVERLAP` | `50` | Overlap between chunks |
| `RETRIEVAL_K` | `5` | Documents retrieved per query |
