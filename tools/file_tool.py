# tools/file_tool.py
from pathlib import Path

BASE_DIR = Path.cwd()

def read_file(path: str):
    file_path = (BASE_DIR / path).resolve()

    if not str(file_path).startswith(str(BASE_DIR)):
        return "Access denied."

    if not file_path.exists():
        return "File not found."

    return file_path.read_text()
