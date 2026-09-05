import re


EMERGENCY_PATTERNS = [
    r"\b(chest pain|can't breathe|cannot breathe|difficulty breathing|stroke|heart attack|severe bleeding)\b",
    r"\b(unconscious|seizure|suicidal|overdose|poisoning)\b",
]

PRESCRIPTION_PATTERNS = [
    r"\b(what medicine|which medicine|what tablet|which tablet|prescribe|dose|dosage|how many tablets)\b",
    r"\b(can i take|should i take).*\b(antibiotic|amoxicillin|azithromycin|medicine|tablet)\b",
]

LEFTOVER_PATTERNS = [
    r"\b(leftover|old|friend'?s|someone else'?s).*\b(antibiotic|antibiotics|medicine|medicines|tablet|tablets|prescription)\b",
]


def classify_safety(query: str) -> dict:
    text = query.lower()
    if any(re.search(pattern, text) for pattern in EMERGENCY_PATTERNS):
        return {
            "level": "emergency",
            "message": (
                "I can't diagnose the cause or prescribe medicine. Symptoms like this can sometimes "
                "require urgent medical evaluation. If symptoms are severe, sudden, worsening, or "
                "include trouble breathing, fainting, severe pain, or confusion, seek emergency medical care now."
            ),
        }
    if any(re.search(pattern, text) for pattern in LEFTOVER_PATTERNS):
        return {
            "level": "unsafe_medication",
            "message": (
                "Starting leftover or someone else's prescription medicine is not safe. Antibiotics should only "
                "be used when prescribed for the current illness by a qualified healthcare professional."
            ),
        }
    if any(re.search(pattern, text) for pattern in PRESCRIPTION_PATTERNS):
        return {
            "level": "medical_advice",
            "message": (
                "I can share general health information, but I can't choose a medicine, prescribe treatment, "
                "or recommend a dose. A qualified healthcare professional should guide medication decisions."
            ),
        }
    return {"level": "normal", "message": ""}
