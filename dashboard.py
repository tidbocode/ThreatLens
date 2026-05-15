import streamlit as st

from src.threatlens.stats import get_by_source, index_stats

st.set_page_config(page_title="ThreatLens", layout="wide")


@st.cache_resource
def _chain():
    from src.threatlens.agent import build_chain
    return build_chain()


def _render_sidebar(stats: dict):
    st.sidebar.title("ThreatLens")
    st.sidebar.caption("Local threat intelligence Q&A")
    st.sidebar.metric("Indexed chunks", stats["total"])

    if stats["by_source"]:
        st.sidebar.subheader("By source")
        for src, count in sorted(stats["by_source"].items()):
            st.sidebar.text(f"{src}: {count}")

    st.sidebar.divider()
    if st.sidebar.button("Refresh index", use_container_width=True):
        from src.threatlens.ingest import ingest
        with st.spinner("Pulling feeds and rebuilding index..."):
            n = ingest()
        st.sidebar.success(f"Indexed {n} chunks")
        st.cache_resource.clear()
        st.rerun()


def _render_chat(stats: dict):
    if stats["total"] == 0:
        st.warning("No index found. Click **Refresh index** in the sidebar to ingest feeds.")
        return

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                st.caption(f"Sources: {', '.join(msg['sources'])}")

    prompt = st.chat_input("Ask about threats, TTPs, IOCs...")
    if not prompt:
        return

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    from src.threatlens.agent import ask
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = ask(prompt, chain=_chain())
        st.markdown(result["answer"])
        if result["sources"]:
            st.caption(f"Sources: {', '.join(result['sources'])}")

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sources": result["sources"],
    })


def _render_iocs():
    iocs = get_by_source("threatfox", limit=2000)
    if not iocs:
        st.info("No IOCs indexed.")
        return

    st.write(f"**{len(iocs)}** IOCs indexed (ThreatFox, last 7 days)")

    col1, col2 = st.columns([1, 2])
    with col1:
        types = sorted({i.get("ioc_type", "") for i in iocs if i.get("ioc_type")})
        type_filter = st.multiselect("Type", types)
    with col2:
        search = st.text_input("Search", placeholder="malware, domain, hash...")

    filtered = iocs
    if type_filter:
        filtered = [i for i in filtered if i.get("ioc_type") in type_filter]
    if search:
        s = search.lower()
        filtered = [i for i in filtered if s in i.get("content", "").lower()]

    table = [
        {
            "Type": i.get("ioc_type", ""),
            "Malware": i.get("malware", ""),
            "Details": i.get("content", "").replace("\n", " | "),
        }
        for i in filtered
    ]
    st.dataframe(table, use_container_width=True, height=600, hide_index=True)


def _render_techniques():
    techniques = get_by_source("mitre-attack", limit=3000)
    if not techniques:
        st.info("No MITRE techniques indexed.")
        return

    st.write(f"**{len(techniques)}** MITRE ATT&CK techniques indexed")

    all_tactics = set()
    for t in techniques:
        for tactic in (t.get("tactics") or "").split(", "):
            if tactic:
                all_tactics.add(tactic)

    col1, col2 = st.columns([1, 2])
    with col1:
        tactic_filter = st.multiselect("Tactic", sorted(all_tactics))
    with col2:
        search = st.text_input("Search techniques", placeholder="lateral movement, credential...")

    filtered = techniques
    if tactic_filter:
        filtered = [
            t for t in filtered
            if any(tac in (t.get("tactics") or "") for tac in tactic_filter)
        ]
    if search:
        s = search.lower()
        filtered = [t for t in filtered if s in t.get("content", "").lower()]

    st.caption(f"Showing {min(len(filtered), 200)} of {len(filtered)}")
    for t in filtered[:200]:
        label = f"{t.get('technique_id', '')} — {t.get('name', '')}"
        with st.expander(label):
            st.text(t.get("content", ""))


def main():
    stats = index_stats()
    _render_sidebar(stats)

    tab_chat, tab_iocs, tab_techniques = st.tabs(["Chat", "IOCs", "Techniques"])
    with tab_chat:
        _render_chat(stats)
    with tab_iocs:
        _render_iocs()
    with tab_techniques:
        _render_techniques()


main()
