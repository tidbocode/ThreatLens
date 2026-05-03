from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from .config import CHROMA_PATH, EMBEDDING_MODEL, MODEL_NAME, RETRIEVAL_K

_SYSTEM_PROMPT = """You are ThreatLens, a specialized threat intelligence analyst assistant.
Answer questions about threat actors, TTPs (tactics, techniques, and procedures), IOCs
(indicators of compromise), malware, CVEs, and cyber incidents using only the provided context.
Be precise and cite specific details when available. If the context is insufficient, say so
rather than speculating.

Context:
{context}"""


def build_chain():
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": RETRIEVAL_K})

    llm = ChatOpenAI(model=MODEL_NAME, temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("system", _SYSTEM_PROMPT),
        ("human", "{input}"),
    ])

    return create_retrieval_chain(retriever, create_stuff_documents_chain(llm, prompt))


def ask(question: str, chain=None) -> dict:
    if chain is None:
        chain = build_chain()
    result = chain.invoke({"input": question})
    sources = list({doc.metadata.get("source", "unknown") for doc in result.get("context", [])})
    return {"answer": result["answer"], "sources": sources}
