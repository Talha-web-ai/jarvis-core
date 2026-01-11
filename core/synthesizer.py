# core/synthesizer.py
from core.llm import llm_complete

SYSTEM_PROMPT = """
You are a response synthesizer.
Given intermediate outputs, produce ONE clear, concise final answer for the user.
Do NOT repeat raw data.
"""

def synthesize(outputs: list[str]) -> str:
    joined = "\n".join(outputs)
    return llm_complete(SYSTEM_PROMPT, joined)
