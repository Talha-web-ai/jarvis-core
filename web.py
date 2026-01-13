# web.py

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>JARVIS Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #0f172a;
            color: #e5e7eb;
            padding: 40px;
        }
        h1 { color: #38bdf8; }
        textarea {
            width: 100%;
            height: 80px;
            padding: 10px;
            background: #020617;
            color: white;
            border-radius: 6px;
            border: none;
        }
        button {
            padding: 10px 20px;
            margin-top: 10px;
            margin-right: 10px;
            background: #38bdf8;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }
        button:hover { background: #0ea5e9; }
        pre {
            background: #020617;
            padding: 20px;
            margin-top: 20px;
            border-radius: 6px;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <h1>🤖 JARVIS Dashboard</h1>

    <textarea id="goal" placeholder="Enter your goal for JARVIS..."></textarea><br>

    <button onclick="execute()">Execute</button>
    <button onclick="continueTask()">Continue</button>

    <pre id="output">Waiting for input...</pre>

<script>
async function execute() {
    const goal = document.getElementById("goal").value;
    const res = await fetch("/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ goal })
    });
    const data = await res.json();
    render(data);
}

async function continueTask() {
    const res = await fetch("/continue", { method: "POST" });
    const data = await res.json();
    render(data);
}

function render(data) {
    let text = "";

    if (data.confidence === "low") {
        text += "⚠️ LOW CONFIDENCE\\n\\n";
    }
    if (data.status === "failed") {
        text += "❌ FAILED\\n\\n";
    }

    text += data.result;
    document.getElementById("output").textContent = text;
}
</script>
</body>
</html>
"""

@router.get("/ui", response_class=HTMLResponse)
def ui():
    return HTML_PAGE
