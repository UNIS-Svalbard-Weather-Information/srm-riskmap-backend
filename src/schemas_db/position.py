from sqlalchemy import Column, Integer, String, UniqueConstraint
from geoalchemy2 import Geometry
from src.database.session import Base


class Position(Base):
    __tablename__ = "positions"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, unique=True, index=True, nullable=False)
    geometry = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    
    __table_args__ = (
        UniqueConstraint('event_id', name='uq_position_event_id'),
    )