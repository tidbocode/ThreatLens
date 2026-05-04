import requests
from langchain_core.documents import Document

THREATFOX_API_URL = "https://threatfox-api.abuse.ch/api/v1/"


def load_threatfox_iocs(days: int = 7) -> list[Document]:
    payload = {"query": "get_iocs", "days": days}
    response = requests.post(THREATFOX_API_URL, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()

    if data.get("query_status") != "ok":
        return []

    docs = []
    for ioc in data.get("data", []):
        content = (
            f"IOC: {ioc.get('ioc_value')}\n"
            f"Type: {ioc.get('ioc_type')}\n"
            f"Malware: {ioc.get('malware_printable', 'Unknown')}\n"
            f"Confidence: {ioc.get('confidence_level', 0)}%\n"
            f"Tags: {', '.join(ioc.get('tags') or [])}\n"
            f"First seen: {ioc.get('first_seen')}\n"
            f"Comment: {ioc.get('comment', '')}"
        )

        docs.append(Document(
            page_content=content,
            metadata={
                "source": "threatfox",
                "ioc_type": ioc.get("ioc_type", ""),
                "malware": ioc.get("malware_printable", ""),
                "ioc_id": str(ioc.get("id", "")),
            },
        ))

    return docs
