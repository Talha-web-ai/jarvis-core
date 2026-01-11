# tools/shell_tool.py
import subprocess

ALLOWED_COMMANDS = ["ls", "pwd", "whoami"]

def run_shell(command: str):
    base = command.split()[0]
    if base not in ALLOWED_COMMANDS:
        return "Command blocked."

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()
