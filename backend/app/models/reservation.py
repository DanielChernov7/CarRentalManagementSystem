from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Date, Boolean, Index, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, date
import enum
from app.database import Base


class ReservationStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Reservation(Base):
    """Reservation model with business logic encapsulation"""
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, index=True)
    rate_plan_id = Column(Integer, ForeignKey("rate_plans.id"), nullable=False, index=True)
    pickup_location_id = Column(Integer, ForeignKey("locations.id"), nullable=False, index=True)
    dropoff_location_id = Column(Integer, ForeignKey("locations.id"), nullable=False, index=True)

    start_date = Column(Date, nullable=False, index=True)
    end_date = Column(Date, nullable=False, index=True)

    base_price = Column(Float, nullable=False)
    discount_amount = Column(Float, default=0.0)
    one_way_fee_amount = Column(Float, default=0.0)
    insurance_amount = Column(Float, default=0.0)
    total_price = Column(Float, nullable=False)

    status = Column(
        Enum(
            ReservationStatus,
            name="reservationstatus",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        default=ReservationStatus.PENDING,
        nullable=False,
        index=True,
    )

    include_insurance = Column(Boolean, default=False)
    special_requests = Column(String(500))

    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    confirmed_at = Column(DateTime, nullable=True)
    cancelled_at = Column(DateTime, nullable=True)

    # Relationships
    customer = relationship("Customer", back_populates="reservations")
    vehicle = relationship("Vehicle", back_populates="reservations")
    rate_plan = relationship("RatePlan", back_populates="reservations")
    pickup_location = relationship("Location", back_populates="pickup_reservations", foreign_keys=[pickup_location_id])
    dropoff_location = relationship("Location", back_populates="dropoff_reservations", foreign_keys=[dropoff_location_id])
    payments = relationship("Payment", back_populates="reservation", cascade="all, delete-orphan")
    inspections = relationship("Inspection", back_populates="reservation", cascade="all, delete-orphan")
    damage_reports = relationship("DamageReport", back_populates="reservation", cascade="all, delete-orphan")

    # Constraints and indexes
    __table_args__ = (
        CheckConstraint('end_date > start_date', name='check_end_after_start'),
        Index('idx_reservation_dates', 'vehicle_id', 'start_date', 'end_date'),
        Index('idx_reservation_status_dates', 'status', 'start_date', 'end_date'),
    )

    # Business logic methods (encapsulation)
    def confirm(self):
        """Confirm reservation after successful payment"""
        if self.status == ReservationStatus.PENDING:
            self.status = ReservationStatus.CONFIRMED
            self.confirmed_at = datetime.utcnow()
            return True
        return False

    def activate(self):
        """Activate reservation when customer picks up vehicle"""
        if self.status == ReservationStatus.CONFIRMED:
            self.status = ReservationStatus.ACTIVE
            return True
        return False

    def complete(self):
        """Complete reservation when vehicle is returned"""
        if self.status == ReservationStatus.ACTIVE:
            self.status = ReservationStatus.COMPLETED
            return True
        return False

    def cancel(self):
        """Cancel reservation"""
        if self.status in [ReservationStatus.PENDING, ReservationStatus.CONFIRMED]:
            self.status = ReservationStatus.CANCELLED
            self.cancelled_at = datetime.utcnow()
            return True
        return False

    @property
    def rental_days(self) -> int:
        """Calculate number of rental days"""
        return (self.end_date - self.start_date).days

    @property
    def is_one_way(self) -> bool:
        """Check if this is a one-way rental"""
        return self.pickup_location_id != self.dropoff_location_id
