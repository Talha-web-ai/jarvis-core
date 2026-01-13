# core/tool_evaluator.py

def evaluate_tool_result(result: str) -> dict:
    """
    Returns confidence score and status for a tool result.
    """

    lowered = result.lower()

    # Hard failures
    if any(x in lowered for x in ["error:", "404", "invalid", "not allowed"]):
        return {
            "confidence": 0.0,
            "status": "failed"
        }

    # Weak / partial results
    if len(result.strip()) < 200:
        return {
            "confidence": 0.4,
            "status": "weak"
        }

    # Good result
    return {
        "confidence": 0.9,
        "status": "success"
    }
