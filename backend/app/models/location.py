from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Location(Base):
    """Location/Branch model"""
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False, index=True)
    state = Column(String(100), nullable=False)
    zip_code = Column(String(20), nullable=False)
    phone = Column(String(50), nullable=False)
    email = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    vehicles = relationship("Vehicle", back_populates="base_location", foreign_keys="Vehicle.base_location_id")
    pickup_reservations = relationship("Reservation", back_populates="pickup_location", foreign_keys="Reservation.pickup_location_id")
    dropoff_reservations = relationship("Reservation", back_populates="dropoff_location", foreign_keys="Reservation.dropoff_location_id")
