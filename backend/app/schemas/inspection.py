from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.inspection import InspectionType, InspectionStatus


class InspectionBase(BaseModel):
    reservation_id: int
    vehicle_id: int
    inspection_type: InspectionType
    exterior_condition: Optional[str] = Field(None, max_length=50)
    interior_condition: Optional[str] = Field(None, max_length=50)
    tire_condition: Optional[str] = Field(None, max_length=50)
    fuel_level: Optional[int] = Field(None, ge=0, le=100)
    mileage: int = Field(..., ge=0)
    has_damages: bool = False
    notes: Optional[str] = None


class InspectionCreate(InspectionBase):
    clerk_id: int


class InspectionUpdate(BaseModel):
    status: Optional[InspectionStatus] = None
    exterior_condition: Optional[str] = Field(None, max_length=50)
    interior_condition: Optional[str] = Field(None, max_length=50)
    tire_condition: Optional[str] = Field(None, max_length=50)
    fuel_level: Optional[int] = Field(None, ge=0, le=100)
    mileage: Optional[int] = Field(None, ge=0)
    has_damages: Optional[bool] = None
    notes: Optional[str] = None


class InspectionResponse(InspectionBase):
    id: int
    clerk_id: int
    status: InspectionStatus
    inspected_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
