from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.vehicle import VehicleStatus, VehicleType


class VehicleBase(BaseModel):
    make: str = Field(..., min_length=1, max_length=100)
    model: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., ge=1900, le=2100)
    license_plate: str = Field(..., min_length=1, max_length=50)
    vin: str = Field(..., min_length=1, max_length=100)
    color: Optional[str] = Field(None, max_length=50)
    vehicle_type: VehicleType
    daily_rate: float = Field(..., gt=0)
    base_location_id: int


class VehicleCreate(VehicleBase):
    mileage: int = Field(0, ge=0)
    status: VehicleStatus = VehicleStatus.AVAILABLE


class VehicleUpdate(BaseModel):
    make: Optional[str] = Field(None, min_length=1, max_length=100)
    model: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=1900, le=2100)
    color: Optional[str] = Field(None, max_length=50)
    vehicle_type: Optional[VehicleType] = None
    status: Optional[VehicleStatus] = None
    mileage: Optional[int] = Field(None, ge=0)
    daily_rate: Optional[float] = Field(None, gt=0)
    base_location_id: Optional[int] = None


class VehicleResponse(VehicleBase):
    id: int
    status: VehicleStatus
    mileage: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
