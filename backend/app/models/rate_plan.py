from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class RatePlan(Base):
    """Rate plan model for pricing strategies"""
    __tablename__ = "rate_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    discount_percentage = Column(Float, default=0.0)  # 0-100
    one_way_fee = Column(Float, default=0.0)
    insurance_daily_rate = Column(Float, default=0.0)
    min_days = Column(Integer, default=1)
    max_days = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    reservations = relationship("Reservation", back_populates="rate_plan")
