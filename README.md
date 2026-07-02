 -# AI Research & Image Assistant 🧠🎨

This is a powerful, modern, and beautiful AI assistant that works in both **Online (Groq)** and **Offline (Ollama)** modes. It can perform deep topic research, converse naturally, parse uploaded documents (PDFs/Text), generate high-quality images, and even edit/replace the background of your photos using state-of-the-art local AI tools.

---

## 🌟 Key Features

1. **Intelligent Router (No Buttons Needed)**: Auto-detects your intent. Whether you ask to chat, write a research report, generate an image, or change a photo's background, the assistant switches modes automatically.
2. **Fast-Path Latency Optimizer**: Bypasses the LLM router for simple greetings or short messages (like *"Hello"*, *"Aap kaise ho"*), delivering responses in under 1 second.
3. **Double Mode (Online & Offline)**:
   - **Online**: Powered by Groq API (Llama-3.1-8b-instant) for superfast speed and Pollinations AI for image generation.
   - **Offline**: Uses Ollama (Qwen2:0.5b) locally when there is no internet connection.
4. **Professional Research Reports**: Automatically writes comprehensive, formatted research papers, which are saved in the project directory and displayed in the **Saved Reports** sidebar.
5. **High-Quality Image Editing (Background Changer)**:
   - Upload any portrait/image and write instructions like *"Change background to sunset"*.
   - Uses `rembg` locally with **Alpha Matting** enabled to produce ultra-smooth, realistic hair and body cutouts.
   - Merges it seamlessly with a photorealistic, 4K-upscaled AI background.
6. **Voice Typing & Read Aloud**: Includes a text-to-speech feature to read reports to you, and speech-to-text for hands-free queries.
7. **Document Parser**: Supports uploading `.txt` and `.pdf` files. It extracts text and lets you research, summarize, or analyze them.
8. **Premium Glassmorphic UI**: Vibrant, responsive dark/light mode interface with responsive scrolling.

---

## 🛠️ Step-by-Step Installation & Setup

Follow these exact steps to set up and run the project from scratch on any Windows machine:

### Step 1: Install Python
Make sure you have **Python 3.10** or **Python 3.11** installed on your system. 
- You can download it from [python.org](https://www.python.org/downloads/).
- *Note:* Make sure to check the box **"Add Python to PATH"** during installation.

### Step 2: Set Up Ollama (For Offline Mode)
1. Download and install Ollama from [ollama.com](https://ollama.com/).
2. Open your terminal (PowerShell or CMD) and run the following command to download the local model:
   ```bash
   ollama run qwen2:0.5b
   ```
3. Once the download completes, you can close the terminal. The Ollama service will run in the background.

### Step 3: Clone/Download the Project & Create Virtual Environment
1. Extract your project files to a folder (e.g., `ai_research_assistant`).
2. Open terminal in the project directory.
3. Create a Python Virtual Environment (`venv`):
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   - **PowerShell (Recommended)**:
     ```bash
     Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
     .\venv\Scripts\Activate.ps1
     ```
   - **Command Prompt (CMD)**:
     ```cmd
     .\venv\Scripts\activate.bat
     ```

### Step 4: Install Dependencies
With the virtual environment active (you will see `(venv)` at the beginning of your terminal line), install all required libraries:
```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment Variables
1. Get a free API Key from [console.groq.com](https://console.groq.com/).
2. Create a new file in the root folder of the project named `.env`.
3. Add the following line to the `.env` file:
   ```env
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```
   *(Replace `your_actual_groq_api_key_here` with the API key you got from Groq).*

---

## 🚀 How to Run the App

1. Activate your virtual environment (if not already active):
   ```bash
   .\venv\Scripts\Activate.ps1
   ```
2. Start the FastAPI application:
   ```bash
   python app.py
   ```
3. Open your web browser and go to:
   ```
   http://127.0.0.1:8000
   ```
4. Enjoy your AI Assistant!

---

## 📁 Project Structure

- `app.py`: Main FastAPI server containing route definitions (`/ask`, `/upload`, `/status`, `/reports`) and the asynchronous streaming generator.
- `agents.py`: Contains agent initialization, local/online internet detection logic, and LLM clients.
- `requirements.txt`: List of all Python packages required.
- `templates/index.html`: Modern, premium glassmorphic UI frontend with real-time SSE (Server-Sent Events) streaming parser.
- `.env`: Holds your secret API Keys.
- `report_*.txt`: Automatically saved research reports and chat histories.

---

## 💡 Troubleshooting & Notes

- **First Time Background Removal**: The first time you ask to change a photo's background, it will take 1-2 minutes because it needs to download the `u2net` background-removal model (approx. 170MB). After the first download, it will process in just a few seconds.
- **Hard Refreshing the UI**: If you make styling changes and they do not reflect in the browser, perform a **Hard Refresh** by pressing `Ctrl + F5` (Windows) or `Cmd + Shift + R` (Mac).
- **Offline fallback**: If your internet goes down, the mode indicator at the top bar will turn red (**Ollama Offline**) and use your local machine to process prompts.
