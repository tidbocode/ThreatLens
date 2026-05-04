import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
CHAT_MODEL = os.getenv("CHAT_MODEL", "mistral:7b")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")
CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
RETRIEVAL_K = int(os.getenv("RETRIEVAL_K", "5"))
OTX_API_KEY = os.getenv("OTX_API_KEY", "")
