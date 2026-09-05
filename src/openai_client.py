import os

import requests

from config import OPENAI_MODEL


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


def ask_openai(prompt: str, model: str = OPENAI_MODEL) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OpenAI is selected, but OPENAI_API_KEY is not set. Paste it in the sidebar or set it in your terminal."
        )

    try:
        response = requests.post(
            OPENAI_RESPONSES_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={"model": model, "input": prompt},
            timeout=120,
        )
    except requests.RequestException as exc:
        raise RuntimeError(
            "OpenAI could not be reached from this machine. Check internet access, firewall, antivirus, or proxy settings."
        ) from exc

    if response.status_code in {401, 403}:
        raise RuntimeError("OpenAI API key was rejected. Check or rotate the key, then set OPENAI_API_KEY again.")
    if response.status_code == 400:
        raise RuntimeError(
            f"OpenAI rejected model '{model}'. Change OPENAI_MODEL in config.py to a model enabled for your key."
        )

    try:
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"OpenAI request failed: {response.status_code} {response.text[:300]}") from exc

    payload = response.json()
    if payload.get("output_text"):
        return payload["output_text"].strip()

    texts = []
    for item in payload.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                texts.append(content.get("text", ""))
    answer = "\n".join(texts).strip()
    if not answer:
        raise RuntimeError("OpenAI returned no answer text.")
    return answer
