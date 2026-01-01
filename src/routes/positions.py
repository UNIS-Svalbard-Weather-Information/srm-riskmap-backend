from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.models.position import PositionCreate, PositionResponse
from src.schemas_db.position import Position
from src.database.session import get_db
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

router = APIRouter(prefix="/positions", tags=["positions"])


@router.post("/", response_model=PositionResponse)
def create_position(position: PositionCreate, db: Session = Depends(get_db)):
    # Check if event_id already exists
    existing = db.query(Position).filter(Position.event_id == position.event_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Event ID already exists")
    
    # Create Point geometry from latitude and longitude
    point = Point(position.longitude, position.latitude)
    
    # Create new position
    db_position = Position(
        event_id=position.event_id,
        geometry=from_shape(point, srid=4326)
    )
    
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    
    return PositionResponse.from_orm_with_geometry(db_position)


@router.get("/", response_model=List[PositionResponse])
def get_positions(db: Session = Depends(get_db)):
    positions = db.query(Position).all()
    return [PositionResponse.from_orm_with_geometry(pos) for pos in positions]


@router.get("/{event_id}", response_model=PositionResponse)
def get_position(event_id: str, db: Session = Depends(get_db)):
    position = db.query(Position).filter(Position.event_id == event_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    return PositionResponse.from_orm_with_geometry(position)