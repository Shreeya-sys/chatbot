def format_evidence(chunks: list[dict]) -> str:
    evidence_blocks = []
    for index, chunk in enumerate(chunks, start=1):
        meta = chunk.get("metadata", {})
        source = meta.get("source", "Unknown source")
        title = meta.get("title", "Untitled")
        url = meta.get("url", "")
        text = chunk.get("text", "")
        evidence_blocks.append(
            f"[Evidence {index}] Source: {source}\nTitle: {title}\nURL: {url}\nText: {text}"
        )
    return "\n\n".join(evidence_blocks)


def unique_sources(chunks: list[dict]) -> list[dict]:
    seen = set()
    sources = []
    for chunk in chunks:
        meta = chunk.get("metadata", {})
        key = (meta.get("source"), meta.get("url"), meta.get("title"))
        if key in seen:
            continue
        seen.add(key)
        sources.append(
            {
                "source": meta.get("source", "Unknown source"),
                "title": meta.get("title", meta.get("source", "Source")),
                "url": meta.get("url", ""),
            }
        )
    return sources


def evidence_status(chunks: list[dict]) -> str:
    source_count = len(unique_sources(chunks))
    if source_count >= 2:
        return "Strongly supported"
    if source_count == 1:
        return "Limited evidence"
    return "Unable to verify from local sources"
