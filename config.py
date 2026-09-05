OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "phi4-mini:latest"

CHROMA_DIR = "vectorstore/chroma"
COLLECTION_NAME = "healthguard_medical_sources"
EMBEDDING_DIMENSIONS = 384

TOP_K = 5
MAX_HISTORY_MESSAGES = 6

TRUSTED_WEB_DOMAINS = [
    "who.int",
    "cdc.gov",
    "nih.gov",
    "medlineplus.gov",
    "nhs.uk",
    "mohfw.gov.in",
]
