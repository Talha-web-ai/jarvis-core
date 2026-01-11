# JARVIS 🤖  
**A Local, Autonomous AI Assistant with Memory, Self-Review, and Tool Execution**

JARVIS is a full-stack autonomous AI assistant inspired by the idea of a true AI operating layer — not just a chatbot.

Unlike typical AI demos, JARVIS is designed as a **real system** that can:
- Understand high-level goals
- Plan tasks using an LLM
- Execute actions using tools
- Review its own output
- Persist memory across runs
- Operate fully **offline** using a **local LLM (Ollama)**

---

## 🚀 Key Features

### 🧠 Autonomous Reasoning
- Goal-based planning using a local LLM
- Breaks vague goals into ordered, executable steps

### 🧑‍🤝‍🧑 Multi-Agent Architecture
- **Planner Agent** – decomposes goals into steps  
- **Executor Agent** – executes steps and tools  
- **Reviewer Agent** – validates output quality before acceptance  

### 💾 Memory System
- **Short-term memory** (per execution)
- **Long-term memory** (persistent across runs)
- Approved results are automatically stored

### 🛠️ Tool Execution (Safe by Design)
- LLM decides **which tool to use**
- Strictly sandboxed tools:
  - File reading (project directory only)
  - Shell commands (allow-listed only)
- Hard safety guardrails (no arbitrary execution)

### 🔁 Reliability
- Retry logic on failed steps
- Defensive handling of LLM errors
- No crashes on malformed responses

### 🔒 Privacy-First
- Runs **entirely locally**
- No OpenAI / paid APIs
- Uses Ollama + open-source models (Mistral, LLaMA, etc.)

---

## 🏗️ Architecture Overview

User Goal
↓
JARVIS Agent
├── Planner Agent (LLM)
├── Executor Agent
│ └── Tool Router (LLM)
│ ├── File Tool
│ └── Shell Tool
├── Reviewer Agent (LLM)
└── Memory System
├── Short-Term
└── Long-Term


---

## 📂 Project Structure

jarvis/
├── core/
│ ├── agent.py # Main control loop
│ ├── planner.py # LLM-based planning
│ ├── executor.py # Step execution + tool usage
│ ├── reviewer.py # LLM-based self-review
│ ├── router.py # Tool selection logic
│ └── llm.py # Local LLM abstraction (Ollama)
│
├── tools/
│ ├── registry.py # Tool registry
│ ├── file_tool.py # Safe file reader
│ └── shell_tool.py # Safe shell execution
│
├── memory/
│ ├── short_term.py # Session memory
│ └── long_term.py # Persistent memory
│
├── security/ # Reserved for future guardrails
├── main.py # Entry point
├── requirements.txt
└── README.md


---

## 🧠 Local LLM Setup (Required)

JARVIS uses **Ollama** for local LLM inference.

### Install Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh

## Pull a Model (Recommended)
ollama pull mistral:7b

