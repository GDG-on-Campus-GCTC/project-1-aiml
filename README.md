# AIML Teacher Assistant - Study Portal

A powerful AI-driven tutor system built with CrewAI and FastAPI, featuring real-time response streaming via Redis. This system supports both high-level agent orchestration (Pro Mode) and high-performance direct streaming (Lite Mode).

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10 to 3.13
- Redis Server (running locally on port 6379)
- Google Gemini API Key

### 1. Installation

**All commands MUST be run from the `teachers/` directory.**

```powershell
# 1. Navigate to the project directory
cd teachers

# 2. Install dependencies (using uv - recommended)
uv sync

# OR using standard pip
pip install -r requirements.txt
```

### 2. Environment Setup
The project uses environment variables for credentials. Ensure your `.env` is correctly configured in the `teachers/` directory (you can use `.env.example` as a template):

```env
GOOGLE_API_KEY=your_gemini_api_key_here
REDIS_HOST=localhost
REDIS_PORT=6379
```

### 3. Running the Server

Run this command from inside the `teachers/` folder:

```powershell
uv run uvicorn teachers.app:app --reload
```

---

## 🏗️ Project Structure

- `src/teachers/` - Main source code directory.
  - `app.py` - FastAPI entry point and Redis listener setup.
  - `redis_service.py` - Handles asynchronous Pub/Sub communication with Redis.
  - `request_handler.py` - Orchestrates incoming requests to either Lite or Pro modes.
  - `lite_harness.py` - Core logic for **Lite Mode**: direct Gemini 2.5 Flash streaming with RAG tools.
  - `crew.py` - Contains the **Pro Mode** CrewAI agent and crew definitions.
  - `config/` - YAML configuration files for agents and tasks.
- `memory/` - Local vector database and agent memory storage (ignored by git).
- `requirements.txt` - Python dependency list.
- `pyproject.toml` - Modern Python project configuration.

---

## 🛠️ Performance Modes

### 1. Lite Mode (Default for Streaming)
- **Speed**: Ultra-fast, direct streaming.
- **Model**: Gemini 2.5 Flash.
- **How it works**: Bypasses full agent orchestration to provide token-by-token answers immediately while still using RAG tools for context.
- **Channel**: Uses `aiml:requests` and streams to `aiml:responses:{chatId}`.

### 2. Pro Mode
- **Complexity**: High. Uses full CrewAI agentic workflows.
- **Logic**: Agents reason, use multiple tools, and cross-verify answers.
- **Usage**: Recommended for complex, multi-step academic queries.

---

## 📡 Redis Integration

The project communicates with the Node.js backend using Redis Pub/Sub:
1. **Listen**: Subscribes to `aiml:requests` for incoming questions.
2. **Respond**: Publishes token streams to `aiml:responses:{chatId}`.
3. **Control**: Signals completion with a `done: true` flag.

---

## 🔒 Security
- Always keep your `.env` file secret.
- `.gitignore` is configured to exclude local databases (`.bin`, `.sqlite`), credentials, and virtual environments.
