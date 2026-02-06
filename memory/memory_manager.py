# memory/memory_manager.py

from datetime import datetime, timedelta


DECAY_DAYS = 7
MIN_IMPORTANCE = 0.1


def decay_importance(memory: dict) -> float:
    """
    Decays importance over time.
    Safe against malformed memory entries.
    """

    # 🚨 Guard clause
    if not isinstance(memory, dict):
        return MIN_IMPORTANCE

    timestamp = memory.get("timestamp")
    importance = memory.get("importance", 0.5)

    if not timestamp:
        return importance

    try:
        ts = datetime.fromisoformat(timestamp)
    except Exception:
        return importance

    days_passed = (datetime.utcnow() - ts).days
    decay_factor = max(0.0, 1 - (days_passed / DECAY_DAYS))

    return max(MIN_IMPORTANCE, round(importance * decay_factor, 3))
