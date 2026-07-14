# Task Tracker API — Module 1

A learning-focused REST API built with **Python** and **FastAPI**.  
Uses in-memory storage (no database) to focus on FastAPI fundamentals,
Pydantic validation, and REST API design.

---

## Project Structure

task-tracker-api/
├── app/
│ ├── init.py
│ └── main.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt

---

## Setup

### 1. Clone / enter the project directory

```bash
cd task-tracker-api
```

### 2. Create and activate a virtual environment

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell)**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` if you need a different port or environment label.

---

## Running the server

```bash
uvicorn app.main:app --reload --port 8000
```

| Flag          | Purpose                                          |
| ------------- | ------------------------------------------------ |
| `--reload`    | Auto-restarts on code changes (development only) |
| `--port 8000` | Matches the default in `.env.example`            |

---

## Test the /health endpoint

```bash
curl -s http://localhost:8000/health | python3 -m json.tool
```

**Expected response shape:**

```json
{
  "status": "ok",
  "timestamp": "2025-01-15T10:30:00.123456+00:00"
}
```

---

## Interactive API docs (Swagger UI)

Open your browser at: http://localhost:8000/docs

ReDoc alternative: http://localhost:8000/redoc
