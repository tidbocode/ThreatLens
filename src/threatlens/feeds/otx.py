import requests
from langchain_core.documents import Document

OTX_API_URL = "https://otx.alienvault.com/api/v1"


def load_otx_pulses(api_key: str, limit: int = 20) -> list[Document]:
    if not api_key:
        return []

    headers = {"X-OTX-API-KEY": api_key}
    response = requests.get(
        f"{OTX_API_URL}/pulses/subscribed",
        headers=headers,
        params={"limit": limit},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    docs = []
    for pulse in data.get("results", []):
        indicators = [ind["indicator"] for ind in pulse.get("indicators", [])[:10]]
        content = (
            f"Threat: {pulse['name']}\n"
            f"Description: {pulse.get('description', '')}\n"
            f"Tags: {', '.join(pulse.get('tags', []))}\n"
            f"Indicators: {', '.join(indicators)}\n"
            f"TLP: {pulse.get('tlp', 'white')}\n"
            f"Modified: {pulse.get('modified')}"
        )

        docs.append(Document(
            page_content=content,
            metadata={
                "source": "otx",
                "pulse_id": pulse["id"],
                "name": pulse["name"],
            },
        ))

    return docs
