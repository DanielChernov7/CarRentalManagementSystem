from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class UserRole(enum.Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    CLERK = "clerk"


class User(Base):
    """Base user model implementing inheritance pattern"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(50))
    role = Column(Enum(UserRole), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": role,
    }


class Customer(User):
    """Customer user type - inherits from User"""
    __mapper_args__ = {
        "polymorphic_identity": UserRole.CUSTOMER,
    }

    # Relationship to reservations
    reservations = relationship("Reservation", back_populates="customer", cascade="all, delete-orphan")


class Admin(User):
    """Admin user type - inherits from User"""
    __mapper_args__ = {
        "polymorphic_identity": UserRole.ADMIN,
    }


class Clerk(User):
    """Clerk user type - inherits from User"""
    __mapper_args__ = {
        "polymorphic_identity": UserRole.CLERK,
    }

    # Relationship to inspections
    inspections = relationship("Inspection", back_populates="clerk")
