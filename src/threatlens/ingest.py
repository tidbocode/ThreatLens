from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

from .config import CHROMA_PATH, CHUNK_OVERLAP, CHUNK_SIZE, DATA_DIR, EMBEDDING_MODEL


def _load_documents(data_dir: str) -> list:
    loaders = [
        DirectoryLoader(data_dir, glob="**/*.pdf", loader_cls=PyPDFLoader, silent_errors=True),
        DirectoryLoader(data_dir, glob="**/*.txt", loader_cls=TextLoader, silent_errors=True),
        DirectoryLoader(data_dir, glob="**/*.md", loader_cls=TextLoader, silent_errors=True),
    ]
    docs = []
    for loader in loaders:
        try:
            docs.extend(loader.load())
        except Exception:
            pass
    return docs


def ingest(data_dir: str | None = None) -> int:
    data_dir = data_dir or DATA_DIR

    print(f"Loading documents from {data_dir} ...")
    docs = _load_documents(data_dir)
    if not docs:
        print("No documents found. Drop .pdf, .txt, or .md files into the data directory.")
        return 0

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(docs)
    print(f"Split {len(docs)} document(s) into {len(chunks)} chunks.")

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_PATH)
    print(f"Stored {len(chunks)} chunks in {CHROMA_PATH}.")
    return len(chunks)
