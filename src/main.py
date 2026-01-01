from fastapi import FastAPI
from src.database.session import engine
from src.schemas_db.position import Base
from src.routes.positions import router as positions_router

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Svalbard Risk Event Mapping API")

# Include routers
app.include_router(positions_router)

@app.get("/")
def read_root():
    return {"message": "Svalbard Risk Event Mapping API"}