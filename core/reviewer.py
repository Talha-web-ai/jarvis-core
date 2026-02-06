# core/reviewer.py

def review(text: str) -> str:
    """
    Simple heuristic reviewer.
    Only accepts meaningful textual outputs.
    """

    if not isinstance(text, str):
        return "REJECT"

    cleaned = text.strip()

    if len(cleaned) < 50:
        return "REJECT"

    return "APPROVE"
