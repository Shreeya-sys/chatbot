HEALTH_TERMS = {
    "antibiotic", "virus", "viral", "flu", "cold", "infection", "dehydration", "medicine",
    "medication", "tablet", "dose", "fever", "cough", "pain", "doctor", "prescription",
    "bacteria", "bacterial", "covid", "health", "symptom", "disease", "treatment",
}

AGRICULTURE_TERMS = {"soil", "salinity", "farmer", "crop", "irrigation", "agriculture"}


def detect_scope(query: str) -> dict:
    words = set(query.lower().replace("?", " ").replace(".", " ").split())
    if words & HEALTH_TERMS:
        return {"scope": "healthcare", "note": "The question is within the healthcare information scope."}
    if words & AGRICULTURE_TERMS:
        return {
            "scope": "outside_healthcare",
            "note": (
                "This is outside HealthGuard AI's primary healthcare scope. Provide only brief general "
                "educational information and be clear that it is not medical content."
            ),
        }
    return {
        "scope": "uncertain",
        "note": "The topic is not clearly healthcare. Answer cautiously and state scope limits if needed.",
    }
