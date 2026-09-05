from src.citations import evidence_status, format_evidence, unique_sources
from src.llm_client import ask_llm, llm_available
from src.memory import format_history
from src.prompts import build_answer_prompt
from src.rag import retrieve
from src.safety import classify_safety
from src.scope import detect_scope


def answer_question(question: str, messages: list[dict] | None = None) -> dict:
    safety = classify_safety(question)
    scope = detect_scope(question)
    chunks = retrieve(question)
    sources = unique_sources(chunks)
    status = evidence_status(chunks)

    if safety["level"] in {"emergency", "unsafe_medication"}:
        return {"answer": safety["message"], "sources": sources, "evidence_status": status}

    history = format_history(messages or [])
    prompt = build_answer_prompt(question, format_evidence(chunks), history, scope["note"])

    if not llm_available():
        return {
            "answer": (
                "The selected local LLM provider is not available. Based on local safety rules: "
                + (safety["message"] or "I can answer once the local model is available.")
            ),
            "sources": sources,
            "evidence_status": status,
        }

    if safety["level"] == "medical_advice":
        prompt += "\n\nAdditional safety instruction: Start by saying you cannot prescribe medication or dosage."

    try:
        answer = ask_llm(prompt)
    except RuntimeError as exc:
        answer = str(exc)
    return {"answer": answer, "sources": sources, "evidence_status": status}
