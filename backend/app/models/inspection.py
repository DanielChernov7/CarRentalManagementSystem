from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class InspectionType(enum.Enum):
    PRE_RENTAL = "pre_rental"
    POST_RENTAL = "post_rental"


class InspectionStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Inspection(Base):
    """Inspection model for vehicle condition checks"""
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)
    reservation_id = Column(Integer, ForeignKey("reservations.id"), nullable=False, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, index=True)
    clerk_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    inspection_type = Column(Enum(InspectionType), nullable=False)
    status = Column(Enum(InspectionStatus), default=InspectionStatus.PENDING, nullable=False)

    # Inspection checklist items
    exterior_condition = Column(String(50))  # excellent, good, fair, poor
    interior_condition = Column(String(50))
    tire_condition = Column(String(50))
    fuel_level = Column(Integer)  # Percentage 0-100
    mileage = Column(Integer, nullable=False)

    has_damages = Column(Boolean, default=False)
    notes = Column(Text)

    inspected_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    reservation = relationship("Reservation", back_populates="inspections")
    vehicle = relationship("Vehicle", back_populates="inspections")
    clerk = relationship("Clerk", back_populates="inspections")
