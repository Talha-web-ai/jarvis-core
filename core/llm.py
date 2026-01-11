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

    try:
        resp = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 300  # ⛔ prevent token explosion
                }
            },
            timeout=90  # ⛔ prevent CPU death
        )

        data = resp.json()

        if "response" not in data:
            return f"[LLM ERROR] {data}"

        return data["response"].strip()

    except requests.exceptions.RequestException as e:
        return f"[LLM TIMEOUT] {str(e)}"
