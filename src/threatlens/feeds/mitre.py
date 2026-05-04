import requests
from langchain_core.documents import Document

MITRE_ATTACK_URL = (
    "https://raw.githubusercontent.com/mitre/cti/master"
    "/enterprise-attack/enterprise-attack.json"
)


def load_mitre_techniques() -> list[Document]:
    response = requests.get(MITRE_ATTACK_URL, timeout=60)
    response.raise_for_status()
    data = response.json()

    docs = []
    for obj in data["objects"]:
        if obj.get("type") != "attack-pattern" or obj.get("revoked"):
            continue

        technique_id = ""
        for ref in obj.get("external_references", []):
            if ref.get("source_name") == "mitre-attack":
                technique_id = ref.get("external_id", "")
                break

        tactics = [phase["phase_name"] for phase in obj.get("kill_chain_phases", [])]

        content = (
            f"Technique: {obj['name']}\n"
            f"ID: {technique_id}\n"
            f"Tactics: {', '.join(tactics)}\n\n"
            f"Description: {obj.get('description', '')}"
        )

        docs.append(Document(
            page_content=content,
            metadata={
                "source": "mitre-attack",
                "technique_id": technique_id,
                "name": obj["name"],
                "tactics": ", ".join(tactics),
            },
        ))

    return docs
