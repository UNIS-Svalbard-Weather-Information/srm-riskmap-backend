from pydantic import BaseModel
from typing import Optional
from geoalchemy2.shape import to_shape


class PositionBase(BaseModel):
    event_id: str
    latitude: float
    longitude: float


class PositionCreate(PositionBase):
    pass


class PositionResponse(PositionBase):
    id: int
    
    class Config:
        from_attributes = True
        
    @classmethod
    def from_orm_with_geometry(cls, db_position):
        """Convert from SQLAlchemy model with geometry to Pydantic model with lat/lon"""
        geom = to_shape(db_position.geometry)
        return cls(
            id=db_position.id,
            event_id=db_position.event_id,
            latitude=geom.y,
            longitude=geom.x
        )