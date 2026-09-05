from src.citations import evidence_status, format_evidence, unique_sources
from src.llm_client import ask_llm, llm_available
from src.prompts import build_claim_prompt
from src.rag import retrieve
from src.scope import detect_scope


def verify_claim(claim: str) -> dict:
    scope = detect_scope(claim)
    chunks = retrieve(claim)
    sources = unique_sources(chunks)
    status = evidence_status(chunks)

    if scope["scope"] == "outside_healthcare":
        return {
            "answer": (
                "Claim status: Outside scope\n\n"
                "This claim is outside HealthGuard AI's primary healthcare scope. "
                "Use a domain-specific agriculture source for verification."
            ),
            "sources": sources,
            "evidence_status": "Outside healthcare scope",
        }

    prompt = build_claim_prompt(claim, format_evidence(chunks))
    if not llm_available():
        return {
            "answer": (
                "The selected LLM provider is not available, so I can't complete the LLM-based verification yet."
            ),
            "sources": sources,
            "evidence_status": status,
        }

    try:
        answer = ask_llm(prompt)
    except RuntimeError as exc:
        answer = str(exc)
    return {"answer": answer, "sources": sources, "evidence_status": status}
