# 🤖 AI Research Assistant
### Multi-Agent AI System | Built by Piyush Seth | BCA Final Year Student

---

## 📌 Project Overview

AI Research Assistant is a **Multi-Agent AI System** that automatically researches any topic and generates a professional report. It works in **both Online and Offline mode** — no constant internet dependency required.

---

## 🚀 What This Project Can Do (That ChatGPT Cannot)

| Feature | AI Research Assistant | ChatGPT |
|---|---|---|
| **Works Offline** | ✅ Yes (Ollama) | ❌ Always needs internet |
| **Runs on Your Device** | ✅ Local AI on laptop | ❌ Cloud only |
| **Your Data is Private** | ✅ Never leaves your laptop | ❌ Sent to OpenAI servers |
| **Multi-Agent System** | ✅ 2 AI agents collaborate | ❌ Single AI response |
| **Auto Saves Reports** | ✅ .txt files saved automatically | ❌ Manual copy-paste |
| **Free Forever** | ✅ No subscription needed | ❌ Paid after free limit |
| **Custom API Integration** | ✅ Groq + Ollama both | ❌ Fixed to OpenAI |
| **Report History** | ✅ All reports saved & viewable | ❌ No auto-save |
| **Beautiful Web UI** | ✅ Custom built interface | ❌ Generic interface |

---


## ✅ Advantages

- **100% Free** — No subscription, no credit card
- **Privacy First** — Offline mode data never leaves your device
- **Multi-Agent** — Two AI agents (Researcher + Writer) collaborate for better output
- **Auto Report Saving** — Every report saved as .txt file automatically
- **Dual Mode** — Automatically switches between Groq (online) and Ollama (offline)
- **Beautiful UI** — Dark/Light mode, saved reports sidebar, topic suggestions
- **Portable** — Run anywhere, WiFi or no WiFi

---

## ⚠️ Limitations

- Offline mode is slower than online (CPU, no dedicated GPU)
- Ollama requires ~1-2 GB storage for AI model
- Cannot access real-time data (stock prices, live news) in offline mode
- Requires Python + Ollama pre-installed to run locally

---

## ❌ What This Project Cannot Do

- Cannot browse the internet for real-time news (offline mode)
- Cannot generate or edit images
- Cannot process audio or video files
- Offline mode response may take 20-30 seconds (CPU limitation)
- Cannot remember previous conversations across sessions


---

## 🛠️ Technologies & Tools Used

| Tool | Version | Purpose |
|---|---|---|
| **Python** | 3.11.9 | Main programming language |
| **CrewAI** | Latest | Multi-Agent AI framework |
| **FastAPI** | Latest | Web server & API backend |
| **Uvicorn** | Latest | ASGI server for FastAPI |
| **Ollama** | 0.24.0 | Run AI models locally (offline) |
| **LLaMA 3.2 / Qwen2** | 0.5B | Offline AI model |
| **Groq API** | Free | Fast online AI (LLaMA 3.1) |
| **LiteLLM** | Latest | LLM provider abstraction |
| **python-dotenv** | Latest | Environment variable management |
| **HTML/CSS/JS** | - | Frontend web interface |

---

## 📁 Project Structure

```
ai_research_assistant/
│
├── app.py              ← FastAPI web server (main entry)
├── main.py             ← CLI version (terminal only)
├── agents.py           ← AI Agents definition
├── tasks.py            ← Agent tasks definition
├── requirements.txt    ← Python dependencies list
├── .env                ← API keys (secret)
├── README.md           ← This file
│
├── templates/
│   └── index.html      ← Web UI frontend
│
├── venv/               ← Python virtual environment
│
└── report_*.txt        ← Auto-saved reports
```

---

## ⚙️ Complete Installation Guide

### Step 1 — Install Python 3.11

Download from: https://www.python.org/downloads/release/python-3119/

```
Windows installer (64-bit) → Download → Install
⚠️ IMPORTANT: Check "Add Python to PATH" during install!
```

Verify:
```bash
py -3.11 --version
# Should show: Python 3.11.9
```

---

### Step 2 — Install Ollama (For Offline Mode)

Download from: https://ollama.com/download

```
Download for Windows → Install
```

Verify:
```bash
ollama --version
# Should show: ollama version 0.x.x
```

---

### Step 3 — Download AI Model (Offline)

```bash
ollama pull qwen2:0.5b
```

Verify:
```bash
ollama list
# Should show: qwen2:0.5b
```

---

### Step 4 — Clone/Download This Project

Place the project folder on your Desktop or any location.

---

### Step 5 — Open Project in VS Code

```bash
cd Desktop
cd ai_research_assistant
code .
```

---

### Step 6 — Create Virtual Environment

```bash
py -3.11 -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in terminal.

---

### Step 7 — Enable Windows Long Path (One Time Only)

Open PowerShell as Administrator and run:
```bash
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

Then restart your laptop.

---

### Step 8 — Install Dependencies

```bash
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
pip install litellm --trusted-host pypi.org --trusted-host files.pythonhosted.org
pip install fastapi uvicorn jinja2 openai --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

---

### Step 9 — Setup API Keys

Create `.env` file in project root:

```
GROQ_API_KEY=your_groq_api_key_here
OLLAMA_MODEL=ollama/qwen2:0.5b
CREWAI_DISABLE_PROMPT_CACHING=true
OTEL_SDK_DISABLED=true
```

Get FREE Groq API Key from: https://console.groq.com
- Sign up → API Keys → Create API Key → Copy

---

### Step 10 — Run the Project

**Web Interface (Recommended):**
```bash
venv\Scripts\activate
venv\Scripts\python.exe app.py
```
Then open browser: `http://127.0.0.1:8000`

**CLI Version (Terminal only):**
```bash
venv\Scripts\activate
python main.py
```

---

## 🔄 How It Works

```
User enters topic
        ↓
Internet check (automatic)
        ↓
    Online?         Offline?
       ↓                ↓
   Groq API         Ollama
  (Fast, Latest)   (Local, Private)
       ↓                ↓
  Agent 1: Expert Researcher
  (Researches the topic deeply)
       ↓
  Agent 2: Professional Writer
  (Writes structured report)
       ↓
  Report displayed + saved as .txt
```

---

## 📊 Models Used

### Online Mode
- **Model:** `groq/llama-3.1-8b-instant`
- **Provider:** Groq Cloud (Free API)
- **Speed:** 5-10 seconds
- **Requires:** Internet + Groq API key

### Offline Mode
- **Model:** `qwen2:0.5b` (Alibaba's Qwen 2, 0.5 Billion parameters)
- **Provider:** Ollama (Local)
- **Size:** ~350 MB
- **Speed:** 20-30 seconds (CPU dependent)
- **Requires:** Ollama installed + model downloaded

---

## 🌐 API Keys Required

| API | Cost | Link |
|---|---|---|
| **Groq API** | FREE | https://console.groq.com |
| **Ollama** | FREE (local) | https://ollama.com |

---

## 💻 System Requirements

| Component | Minimum | Recommended |
|---|---|---|
| **RAM** | 8 GB | 16 GB |
| **Storage** | 5 GB free | 10 GB free |
| **OS** | Windows 10 | Windows 11 |
| **Python** | 3.11 | 3.11.9 |
| **Internet** | For online mode | WiFi recommended |

---

## 🎯 Quick Commands Reference

```bash
# Activate virtual environment
venv\Scripts\activate

# Run web app
venv\Scripts\python.exe app.py

# Run CLI version
python main.py

# Check Ollama models
ollama list

# Download AI model
ollama pull qwen2:0.5b

# Delete AI model
ollama rm qwen2:0.5b

# Install all dependencies
pip install -r requirements.txt
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---|---|
| `venv not found` | Run `py -3.11 -m venv venv` |
| `python not recognized` | Use `venv\Scripts\python.exe` |
| `ollama not found` | Reinstall Ollama from ollama.com |
| `model not found` | Run `ollama pull qwen2:0.5b` |
| `Groq API error` | Check GROQ_API_KEY in .env file |
| `Port already in use` | Change port in app.py: `port=8001` |
| `OneDrive popup` | Click "Keep items" always |

---

## 👨‍💻 Developer

**Piyush Seth**
BCA Final Year Student
Built as Final Year Project — Multi-Agent AI System

---

## 📄 License

This project is free to use for educational purposes.

---

*Built with using Python, CrewAI, FastAPI, Groq & Ollama*