import requests

from config import OLLAMA_BASE_URL, OLLAMA_MODEL


def ask_ollama(prompt: str, model: str = OLLAMA_MODEL) -> str:
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=120,
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except requests.RequestException as exc:
        raise RuntimeError(
            f"Ollama could not generate with model '{model}'. Pull it with `ollama pull {model}` "
            "or change OLLAMA_MODEL in config.py."
        ) from exc


def ollama_available() -> bool:
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=4)
        return response.ok
    except requests.RequestException:
        return False
