# How to Run Doc Finder Backend

## 1) Prerequisites
- Python 3.10+
- uv (`uv --version` to verify)
- PostgreSQL running locally (or a reachable remote PostgreSQL)

## 2) Install dependencies
```bash
uv sync
```

## 3) Run the server
```bash
uv run uvicorn app.main:app --reload
```

Server URL:
- http://127.0.0.1:8000

## 4) Verify app is running
```bash
curl http://127.0.0.1:8000/health
```

## 5) Run tests
```bash
uv run pytest -v
```
