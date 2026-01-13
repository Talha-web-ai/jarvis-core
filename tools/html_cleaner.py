# tools/html_cleaner.py

import re

def html_to_text(html: str) -> str:
    """
    Very lightweight HTML → text cleaner.
    No JS, no rendering, no heavy deps.
    """

    # Remove scripts and styles
    html = re.sub(r"<script.*?>.*?</script>", "", html, flags=re.S)
    html = re.sub(r"<style.*?>.*?</style>", "", html, flags=re.S)

    # Remove all tags
    text = re.sub(r"<[^>]+>", "", html)

    # Decode common HTML entities
    text = text.replace("&nbsp;", " ")
    text = text.replace("&amp;", "&")
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")

    # Normalize whitespace
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()
