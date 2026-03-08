# Doc Finder Backend

Backend service for the Doc Finder mobile app, built with FastAPI and PostgreSQL.

## Prerequisites

- Python 3.10+
- `uv` (verify with `uv --version`)
- PostgreSQL running locally (or reachable remotely)

## Setup

1. Create `.env` from the example:

```bash
cp .env.example .env
```

2. Update required environment values in `.env`:

```env
OPENAI_API_KEY=...
ADMIN_PASSWORD=...
DATABASE_URL=postgresql://app_user:password@localhost:5432/doc_finder_db
```

3. Install dependencies:

```bash
uv sync
```

## Run the API

```bash
uv run uvicorn app.main:app --reload
```

Server URL:
- `http://127.0.0.1:8000`

Health check:

```bash
curl http://127.0.0.1:8000/health
```

## Run tests

```bash
uv run pytest -v
```

## API docs

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`