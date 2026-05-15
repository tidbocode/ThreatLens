from collections import Counter
from pathlib import Path

import chromadb

from .config import CHROMA_PATH

_COLLECTION_NAME = "langchain"


def _index_exists() -> bool:
    return Path(CHROMA_PATH).exists()


def _collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.get_or_create_collection(_COLLECTION_NAME)


def index_stats() -> dict:
    if not _index_exists():
        return {"total": 0, "by_source": {}}
    data = _collection().get(include=["metadatas"])
    metadatas = data.get("metadatas") or []
    by_source = Counter(m.get("source", "unknown") for m in metadatas)
    return {"total": len(metadatas), "by_source": dict(by_source)}


def get_by_source(source: str, limit: int = 1000) -> list[dict]:
    if not _index_exists():
        return []
    data = _collection().get(
        where={"source": source},
        include=["documents", "metadatas"],
        limit=limit,
    )
    docs = data.get("documents") or []
    metas = data.get("metadatas") or []
    return [{"content": d, **m} for d, m in zip(docs, metas)]
