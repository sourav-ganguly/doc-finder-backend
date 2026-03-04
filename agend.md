# How to Run Doc Finder Backend

## 1) Prerequisites
- Python 3.10+
- uv (`uv --version` to verify)
- PostgreSQL running locally (or a reachable remote PostgreSQL)

## 2) Install dependencies
```bash
uv sync
```

## 3) Configure environment
Create/update `.env` in project root.

Minimum required values:
```env
DATABASE_URL=postgresql://app_user:<PASSWORD>@localhost:5432/doc_finder_db
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
ADMIN_PASSWORD=<YOUR_ADMIN_PASSWORD>
```

## 4) Run the server
```bash
uv run uvicorn app.main:app --reload
```

Server URL:
- http://127.0.0.1:8000

## 5) Verify app is running
```bash
curl http://127.0.0.1:8000/health
```

Expected response:
```json
{"status":"ok","debug_value":84}
```

## 6) API docs
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
