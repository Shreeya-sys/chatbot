from src.ollama_client import ask_ollama, ollama_available


def llm_available() -> bool:
    return ollama_available()


def ask_llm(prompt: str) -> str:
    return ask_ollama(prompt)
