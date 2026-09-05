import os

import requests

from config import GEMINI_MODEL


GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def ask_gemini(prompt: str, model: str = GEMINI_MODEL) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Gemini is selected, but GEMINI_API_KEY is not set. Set it in your terminal, then restart Streamlit."
        )

    try:
        response = requests.post(
            GEMINI_API_URL.format(model=model),
            headers={"x-goog-api-key": api_key, "Content-Type": "application/json"},
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=120,
        )
    except requests.RequestException as exc:
        raise RuntimeError(
            "Gemini could not be reached from this machine. Windows or the network blocked the HTTPS "
            "connection to generativelanguage.googleapis.com. The app can still use Ollama locally."
        ) from exc

    if response.status_code == 400:
        raise RuntimeError(
            f"Gemini rejected model '{model}'. Change GEMINI_MODEL in config.py to a model enabled for your key."
        )
    if response.status_code in {401, 403}:
        raise RuntimeError("Gemini API key was rejected. Check or rotate the key, then set GEMINI_API_KEY again.")

    try:
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"Gemini request failed: {response.status_code} {response.text[:300]}") from exc
    payload = response.json()
    candidates = payload.get("candidates", [])
    if not candidates:
        raise RuntimeError("Gemini returned no answer.")
    parts = candidates[0].get("content", {}).get("parts", [])
    return "\n".join(part.get("text", "") for part in parts).strip()
