from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class DamageSeverity(enum.Enum):
    MINOR = "minor"
    MODERATE = "moderate"
    SEVERE = "severe"
    TOTAL_LOSS = "total_loss"


class DamageReportStatus(enum.Enum):
    REPORTED = "reported"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    RESOLVED = "resolved"


class DamageReport(Base):
    """Damage report model for documenting vehicle damages"""
    __tablename__ = "damage_reports"

    id = Column(Integer, primary_key=True, index=True)
    reservation_id = Column(Integer, ForeignKey("reservations.id"), nullable=False, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, index=True)

    damage_description = Column(Text, nullable=False)
    damage_severity = Column(Enum(DamageSeverity), nullable=False)
    status = Column(Enum(DamageReportStatus), default=DamageReportStatus.REPORTED, nullable=False, index=True)

    estimated_repair_cost = Column(Float, default=0.0)
    actual_repair_cost = Column(Float, nullable=True)

    customer_liable = Column(Boolean, default=True)
    insurance_claim_filed = Column(Boolean, default=False)

    photos_url = Column(String(500))  # JSON array of photo URLs
    notes = Column(Text)

    reported_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    reservation = relationship("Reservation", back_populates="damage_reports")
    vehicle = relationship("Vehicle")
