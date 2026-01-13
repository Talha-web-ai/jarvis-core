# tools/web_tool.py

import requests
from urllib.parse import urlparse

# 🔒 STRICT ALLOWLIST
ALLOWED_DOMAINS = {
    "docs.python.org",
    "developer.mozilla.org",
    "github.com",
    "raw.githubusercontent.com",
    "requests.readthedocs.io"  # ✅ ADD THIS
}

HEADERS = {
    "User-Agent": "JarvisBot/1.0 (read-only)"
}

def fetch_web(url: str) -> str:
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        return "ERROR: Invalid URL scheme."

    domain = parsed.netloc.lower()
    if domain not in ALLOWED_DOMAINS:
        return f"ERROR: Domain '{domain}' not allowed."

    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()

        text = resp.text

        # 🔒 HARD LIMIT: prevent huge payloads
        return text[:8000]

    except Exception as e:
        return f"ERROR: {str(e)}"
