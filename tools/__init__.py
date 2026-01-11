# tools/__init__.py
from tools.registry import register_tool
from tools.file_tool import read_file
from tools.shell_tool import run_shell

register_tool(
    "read_file",
    "Read the contents of a specific text file. Requires a file path like README.md",
    read_file
)

register_tool(
    "run_shell",
    "Run simple shell commands ONLY for listing or checking directories (ls, pwd, whoami). NOT for reading files.",
    run_shell
)
