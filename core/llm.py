# core/llm.py
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral:7b"

def llm_complete(system_prompt: str, user_prompt: str) -> str:
    prompt = f"""
SYSTEM:
{system_prompt}

USER:
{user_prompt}
"""

    resp = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=180
    )

    data = resp.json()

    # DEBUG SAFETY
    if "response" not in data:
        return f"[LLM ERROR] {data}"

    return data["response"].strip()
