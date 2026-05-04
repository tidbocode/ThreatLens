from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .config import CHROMA_PATH, CHUNK_OVERLAP, CHUNK_SIZE, EMBED_MODEL, OLLAMA_BASE_URL, OTX_API_KEY
from .feeds.mitre import load_mitre_techniques
from .feeds.abusech import load_threatfox_iocs
from .feeds.otx import load_otx_pulses


def ingest(_path: str | None = None) -> int:
    print("Loading MITRE ATT&CK techniques...")
    mitre_docs = load_mitre_techniques()
    print(f"  {len(mitre_docs)} techniques loaded")

    print("Loading ThreatFox IOCs (last 7 days)...")
    threatfox_docs = load_threatfox_iocs()
    print(f"  {len(threatfox_docs)} IOCs loaded")

    all_docs = mitre_docs + threatfox_docs

    if OTX_API_KEY:
        print("Loading OTX pulses...")
        otx_docs = load_otx_pulses(OTX_API_KEY)
        print(f"  {len(otx_docs)} pulses loaded")
        all_docs += otx_docs

    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = splitter.split_documents(all_docs)
    print(f"\nIndexing {len(chunks)} chunks...")

    embeddings = OllamaEmbeddings(model=EMBED_MODEL, base_url=OLLAMA_BASE_URL)
    Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_PATH)
    print(f"Stored {len(chunks)} chunks in {CHROMA_PATH}.")
    return len(chunks)
