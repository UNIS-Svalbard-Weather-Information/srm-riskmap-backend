# Svalbard Risk Event Mapping API

A FastAPI-based API for mapping risk events in Svalbard using PostGIS for geographic data storage.



## Table of Contents
1. [Description](#description)
2. [Project Structure](#project-structure)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
   - [Option 1: Quick Start with Docker (Recommended)](#option-1-quick-start-with-docker-recommended)
   - [Option 2: Manual Database Setup](#option-2-manual-database-setup)
5. [Environment Variables](#environment-variables)
6. [Alembic](#alembic)
7. [Running the Application](#running-the-application)
8. [Adding New Models](#adding-new-models)
9. [Docker Development](#docker-development)
10. [Troubleshooting](#troubleshooting)
11. [Contributing](#contributing)
12. [License](#license)



## Description
This API allows you to map risk events in Svalbard using FastAPI and PostGIS for geospatial data management.



## Project Structure

```
srm-riskmap-backend/
├── src/
│   ├── main.py                  # Main FastAPI application
│   ├── database/
│   │   ├── session.py           # Database session management
│   │   └── config.py            # Database configuration
│   ├── models/
│   │   └── position.py          # Pydantic models (request/response)
│   ├── schemas_db/
│   │   └── position.py          # SQLAlchemy database models
│   └── routes/
│       └── positions.py         # API routes for positions
├── alembic/
│   ├── env.py                   # Alembic configuration
│   └── versions/                # Migration scripts
├── docker-compose.yml           # Docker development setup
├── alembic.ini                  # Alembic configuration file
├── .env.example                 # Example environment variables file
├── .env                         # Environment variables (ignored by Git)
└── README.md                    # This file
```



## Prerequisites
- Python 3.8+
- Docker (for development database)
- UV (Python package manager)



## Installation

### Option 1: Quick Start with Docker (Recommended)
1. **Rename and configure the `.env` file:**
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file to set your environment variables (e.g., `DATABASE_URL`).

2. **Start the database, create a virtual environment, and install dependencies:**
   ```bash
   docker-compose up -d
   uv venv
   uv sync
   ```

3. **Activate the virtual environment:**
   - Linux/MacOS:
     ```bash
     source .venv/bin/activate
     ```
   - Windows (PowerShell):
     ```bash
     .\.venv\Scripts\Activate.ps1
     ```
   - Windows (CMD):
     ```bash
     .venv\Scripts\activate.bat
     ```

4. **Run migrations and start the API:**
   ```bash
   alembic upgrade head
   uvicorn src.main:app --reload
   ```

### Option 2: Manual Database Setup
1. **Install PostgreSQL and PostGIS:**
   - **Windows**: Download from [PostgreSQL official site](https://www.postgresql.org/download/windows/)
   - **Mac**: `brew install postgresql postgis`
   - **Linux**: `sudo apt-get install postgresql postgis`

2. **Create the database and enable PostGIS:**
   ```sql
   psql -U postgres
   CREATE DATABASE svalbard_risk_map;
   \c svalbard_risk_map
   CREATE EXTENSION postgis;
   ```

3. **Configure the `.env` file:**
   ```env
   DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/svalbard_risk_map
   ```



## Environment Variables
- **Docker setup**: Use the provided `.env.example` as a template and rename it to `.env`.
  ```env
  DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/svalbard_risk_map
  ```
- **Manual setup**: Update the `.env` file with your PostgreSQL credentials.



## Alembic
Alembic is used for database migrations in this project. It allows you to manage changes to your database schema over time.



- **Create a new migration** (after modifying your models):
  ```bash
  alembic revision --autogenerate -m "Description of the migration"
  ```

- **Apply migrations** to update your database schema:
  ```bash
  alembic upgrade head
  ```

- **Downgrade migrations** (if needed):
  ```bash
  alembic downgrade -1
  ```

- **View migration history**:
  ```bash
  alembic history
  ```

- **Reset migrations** (use with caution):
  ```bash
  alembic stamp head
  ```



## Running the Application
- **Development mode**:
  ```bash
  uvicorn src.main:app --reload
  ```
  The API will be available at [http://localhost:8000](http://localhost:8000).

- **Production mode**:
  ```bash
  uvicorn src.main:app --host 0.0.0.0 --port 8000
  ```


## Adding New Models
1. **Create a new model file** in `src/models/` (e.g., `event.py`).
2. **Define your SQLAlchemy model class**.
3. **Import the model** in `src/main.py`.
4. **Create and run a migration**:
   ```bash
   alembic revision --autogenerate -m "Add event model"
   alembic upgrade head
   ```

### Example Model
```python
from sqlalchemy import Column, Integer, String, DateTime, Text
from src.database.session import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, unique=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    event_date = Column(DateTime)
    severity = Column(String)
```



## Docker Development

### Database Management
- **Start/Stop the database**:
  ```bash
  docker-compose up -d
  docker-compose down
  ```
- **View logs**:
  ```bash
  docker-compose logs -f
  ```
- **Connect to the database**:
  ```bash
  docker exec -it svalbard_postgis_dev psql -U postgres -d svalbard_risk_map
  ```
- **Check PostGIS**:
  ```sql
  SELECT PostGIS_version();
  ```

### Backup/Restore
- **Backup**:
  ```bash
  docker exec svalbard_postgis_dev pg_dump -U postgres svalbard_risk_map > backup.sql
  ```
- **Restore**:
  ```bash
  docker exec -i svalbard_postgis_dev psql -U postgres svalbard_risk_map < backup.sql
  ```



## Troubleshooting
- **PostGIS not found**: Ensure the PostGIS extension is enabled in your database.
- **Connection refused**: Verify PostgreSQL is running and your credentials are correct.
- **Migration errors**: Reset migrations with `alembic stamp head`.
- **Docker connection issues**: Check container status with `docker ps`.



## Contributing
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes.
4. Create a migration if database changes are needed.
5. Submit a pull request.



## License
This project is licensed under the **European Union Public Licence v. 1.2** – see [LICENSE.md](LICENSE.md) for details.

