# Doc Finder Backend

This is the backend service for the Doc Finder mobile application, built with FastAPI and PostgreSQL.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installing PostgreSQL

- For macOS, you can install PostgreSQL using Homebrew:
  ```bash
  brew install postgresql
  ```

- For Windows, download the installer from the official PostgreSQL website: https://www.postgresql.org/download/windows/

- For Linux, use your distribution's package manager. For example, on Ubuntu:
  ```bash
  sudo apt update
  sudo apt install postgresql postgresql-contrib
  ```

## Local Development Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL:
   
   - Start the PostgreSQL service if it's not running. 
     - On macOS (if installed via Homebrew): `brew services start postgresql`
     - On Windows: Open the SQL Shell (psql) from the Start menu.
     - On Linux: `sudo service postgresql start`

   - Connect to PostgreSQL as the postgres user:
     ```bash
     psql -U postgres
     ```
   
   - Create the `doc_finder_db` database:
     ```sql
     CREATE DATABASE doc_finder_db;
     ```
   
   - Exit the PostgreSQL shell:
     ```
     \q
     ```

   - Update the `.env` file with your database credentials if different from defaults

4. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## Available Endpoints

- `GET /health` - Health check endpoint
- `GET /documents/` - Get list of documents with pagination support
  - Query Parameters:
    - `skip`: Number of records to skip (default: 0)
    - `limit`: Maximum number of records to return (default: 10)

## Environment Variables

Create a `.env` file in the root directory with the following variables:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/doc_finder_db
API_VERSION=v1
```

Adjust the values according to your local setup. 