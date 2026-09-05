SYSTEM_PROMPT = """You are HealthGuard AI, an evidence-based healthcare information assistant.

Rules:
1. Provide general health information only.
2. Do not diagnose diseases.
3. Do not prescribe medications or recommend exact doses.
4. Do not recommend starting leftover prescription medicine.
5. Use the provided evidence whenever possible.
6. Clearly distinguish evidence-backed information from general safety guidance.
7. If evidence is insufficient, say so.
8. Do not invent medical sources or citations.
9. For emergencies, advise the user to seek appropriate emergency medical care.
10. Never present yourself as a doctor.

Write clearly and concisely for a general audience.
"""


def build_answer_prompt(question: str, evidence: str, history: str, scope_note: str) -> str:
    return f"""{SYSTEM_PROMPT}

Conversation context:
{history or "No previous conversation."}

Scope note:
{scope_note}

Retrieved evidence:
{evidence or "No strong retrieved evidence was found."}

User question:
{question}

Answer format:
- Direct answer first.
- Short explanation.
- Mention when professional medical care may be needed.
- Do not include citations that are not present in the retrieved evidence.
"""


def build_claim_prompt(claim: str, evidence: str) -> str:
    return f"""{SYSTEM_PROMPT}

Task: Verify the user's health claim against the retrieved evidence.

Claim:
{claim}

Retrieved evidence:
{evidence or "No strong retrieved evidence was found."}

Return:
Claim status: Supported / Not supported / Misleading / Uncertain / Outside scope
Explanation:
Safety note:
"""
