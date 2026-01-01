# Svalbard Risk Event Mapping API

A FastAPI-based API for mapping risk events in Svalbard using PostGIS for geographic data storage.

## Project Structure

```
srm-riskmap-backend/
├── src/
│   ├── main.py                  # Main FastAPI application
│   ├── database/
│   │   ├── session.py           # Database session management
│   │   ├── config.py            # Database configuration
│   ├── models/
│   │   └── position.py          # Pydantic models (request/response)
│   ├── schemas_db/
│   │   └── position.py          # SQLAlchemy database models
│   └── routes/
│       └── positions.py        # API routes for positions
├── alembic/
│   ├── env.py                  # Alembic configuration
│   └── versions/               # Migration scripts
├── docker-compose.yml          # Docker development setup
├── alembic.ini                 # Alembic configuration file
├── .env                        # Environment variables
└── README.md                   # This file
```

## Prerequisites

- Python 3.8+
- Docker (for development database)
- UV (Python package manager)

## Setup Instructions

### Option 1: Quick Start with Docker (Recommended for Development)

```bash
# Start PostgreSQL with PostGIS
docker-compose up -d

# Install Python dependencies
uv venv
uv sync
```
# Activate the virtual environment
# On Linux/MacOS:
```bash
source .venv/bin/activate
```
# On Windows (PowerShell):
```bash
.\.venv\Scripts\Activate.ps1
```
# On Windows (CMD):
```bash
.venv\Scripts\activate.bat
```

```bash
# Run migrations
alembic upgrade head

# Start the API
uvicorn src.main:app --reload
```



```bash
# Start PostgreSQL with PostGIS
docker-compose up -d

# Install Python dependencies
uv venv
uv sync

# Run migrations
alembic upgrade head

# Start the API
uvicorn src.main:app --reload
```

### Option 2: Manual Database Setup

#### Install PostgreSQL and PostGIS

- **Windows**: Download from [PostgreSQL official site](https://www.postgresql.org/download/windows/)
- **Mac**: `brew install postgresql postgis`
- **Linux**: `sudo apt-get install postgresql postgis`

#### Create Database and Enable PostGIS

```sql
-- Connect to PostgreSQL as admin
psql -U postgres

-- Create database
CREATE DATABASE svalbard_risk_map;

-- Connect to the new database
\c svalbard_risk_map

-- Enable PostGIS extension
CREATE EXTENSION postgis;
```

### 3. Configure Environment Variables

For **Docker setup**, the `.env` file should point to the Docker container:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/svalbard_risk_map
```

For **manual setup**, replace with your PostgreSQL credentials:

```env
DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/svalbard_risk_map
```

### 4. Initialize Alembic

```bash
alembic init alembic
```

This will create the alembic directory structure. You can replace the generated files with the ones provided in this project.

### 5. Create Initial Migration

```bash
alembic revision --autogenerate -m "Create positions table"
```

This will create a migration script in `alembic/versions/`.

### 6. Run Migrations

```bash
alembic upgrade head
```

This will create the database tables based on your models.

## Running the Application

### Development Mode

```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

### Production Mode

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Positions

- **POST /positions/** - Create a new position
  ```json
  {
    "event_id": "string",
    "latitude": 78.2232,
    "longitude": 15.6468
  }
  ```

- **GET /positions/** - Get all positions

- **GET /positions/{event_id}** - Get a specific position by event ID

## Database Schema

### Positions Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key (auto-incremented) |
| event_id | String | Unique identifier for the event |
| geometry | Geometry(POINT, 4326) | Geographic location (latitude, longitude) in WGS84 |

### Geographic Data

- The `geometry` column uses PostGIS to store geographic points
- Coordinates are stored in WGS84 (SRID 4326) format
- Latitude and longitude are converted to Point geometry automatically

## Adding New Models

To add new database models:

1. Create a new file in `src/models/` (e.g., `event.py`)
2. Define your SQLAlchemy model class
3. Import the model in `src/main.py`
4. Create a migration:
   ```bash
   alembic revision --autogenerate -m "Add event model"
   ```
5. Run the migration:
   ```bash
   alembic upgrade head
   ```

## Example Model

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

### Starting the Database

```bash
# Start PostgreSQL with PostGIS
docker-compose up -d

# Stop the database
docker-compose down

# View logs
docker-compose logs -f
```

### Connecting to the Database

```bash
# Connect using psql
docker exec -it svalbard_postgis_dev psql -U postgres -d svalbard_risk_map

# Check PostGIS is working
SELECT PostGIS_version();
```

### Database Management

```bash
# Reset database (development only)
docker-compose down -v && docker-compose up -d

# Backup database
docker exec svalbard_postgis_dev pg_dump -U postgres svalbard_risk_map > backup.sql

# Restore database
docker exec -i svalbard_postgis_dev psql -U postgres svalbard_risk_map < backup.sql
```

## Troubleshooting

### Common Issues

1. **PostGIS not found**: Make sure you've enabled the PostGIS extension in your database
2. **Connection refused**: Check that PostgreSQL is running and your credentials are correct
3. **Migration errors**: Try resetting migrations with `alembic stamp head`
4. **Docker connection issues**: Make sure the container is running (`docker ps`)

### Debugging

- Check database connection: `psql -U username -d svalbard_risk_map`
- View tables: `\dt` in psql
- Check PostGIS version: `SELECT PostGIS_version();`
- Docker container status: `docker ps`

## Contributing

1. Fork the repository
2. Create a new branch: `git checkout -b feature-name`
3. Make your changes
4. Create a migration if database changes are needed
5. Submit a pull request

## License

This project is licensed under the European Union Public Licence v. 1.2 - see [LICENSE.md](LICENSE.md) for details.