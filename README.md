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

## Dockerizing the Application

To run the application using Docker:

1. Make sure you have Docker installed on your machine.

2. Create a `docker-compose.yml` file in the project root with the following content:

   ```yaml
   version: '3'
   
   services:
     db:
       image: postgres:13
       environment:
         POSTGRES_DB: doc_finder_db
         POSTGRES_PASSWORD: postgres
       volumes:
         - postgres_data:/var/lib/postgresql/data
   
     web:
       build: .
       command: uvicorn app.main:app --host 0.0.0.0 --port 8000
       volumes:
         - .:/app
       ports:
         - "8000:8000"
       depends_on:
         - db
       environment:
         DATABASE_URL: postgresql://postgres:postgres@db:5432/doc_finder_db
   
   volumes:
     postgres_data:
   ```

   This defines two services:
   - `db`: A PostgreSQL database container
   - `web`: The FastAPI application container, which depends on the `db` service

3. Update your FastAPI code to use the `DATABASE_URL` environment variable for connecting to the database. For example, in `app/database.py`:

   ```python
   DATABASE_URL = os.getenv("DATABASE_URL")
   engine = create_engine(DATABASE_URL)
   ```

4. Build and start the containers:

   ```bash
   docker-compose up --build
   ```

   This will start the FastAPI application and a PostgreSQL database in separate Docker containers, with the FastAPI container able to access the database using the service name `db` as the hostname.

5. The API will be accessible at `http://localhost:8000`

Alternatively, you can use Docker Compose to run the full stack, including the FastAPI service and a PostgreSQL database. See the `docker-compose.yml` file for the configuration.

To start the stack with Docker Compose:
```bash
docker-compose up
``` 