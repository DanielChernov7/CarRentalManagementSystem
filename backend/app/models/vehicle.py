from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Index
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class VehicleStatus(enum.Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    RENTED = "rented"
    MAINTENANCE = "maintenance"
    OUT_OF_SERVICE = "out_of_service"


class VehicleType(enum.Enum):
    SEDAN = "sedan"
    SUV = "suv"
    TRUCK = "truck"
    VAN = "van"
    LUXURY = "luxury"
    ECONOMY = "economy"


class Vehicle(Base):
    """Vehicle model"""
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    license_plate = Column(String(50), unique=True, nullable=False, index=True)
    vin = Column(String(100), unique=True, nullable=False)
    color = Column(String(50))
    vehicle_type = Column(Enum(VehicleType), nullable=False, index=True)
    status = Column(Enum(VehicleStatus), default=VehicleStatus.AVAILABLE, nullable=False, index=True)
    mileage = Column(Integer, default=0)
    daily_rate = Column(Float, nullable=False)
    base_location_id = Column(Integer, ForeignKey("locations.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    base_location = relationship("Location", back_populates="vehicles", foreign_keys=[base_location_id])
    reservations = relationship("Reservation", back_populates="vehicle", cascade="all, delete-orphan")
    inspections = relationship("Inspection", back_populates="vehicle")

    # Indexes
    __table_args__ = (
        Index('idx_vehicle_status_type', 'status', 'vehicle_type'),
    )
