from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime, date
from app.models.reservation import ReservationStatus


class ReservationBase(BaseModel):
    vehicle_id: int
    rate_plan_id: int
    pickup_location_id: int
    dropoff_location_id: int
    start_date: date
    end_date: date
    include_insurance: bool = False
    special_requests: Optional[str] = Field(None, max_length=500)

    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v, info):
        if 'start_date' in info.data and v <= info.data['start_date']:
            raise ValueError('end_date must be after start_date')
        return v


class ReservationCreate(ReservationBase):
    customer_id: int


class ReservationUpdate(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    include_insurance: Optional[bool] = None
    special_requests: Optional[str] = Field(None, max_length=500)
    status: Optional[ReservationStatus] = None

    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v, info):
        if v and 'start_date' in info.data and info.data['start_date'] and v <= info.data['start_date']:
            raise ValueError('end_date must be after start_date')
        return v


class ReservationResponse(BaseModel):
    id: int
    customer_id: int
    vehicle_id: int
    rate_plan_id: int
    pickup_location_id: int
    dropoff_location_id: int
    start_date: date
    end_date: date
    base_price: float
    discount_amount: float
    one_way_fee_amount: float
    insurance_amount: float
    total_price: float
    status: ReservationStatus
    include_insurance: bool
    special_requests: Optional[str]
    created_at: datetime
    updated_at: datetime
    confirmed_at: Optional[datetime]
    cancelled_at: Optional[datetime]

    class Config:
        from_attributes = True


class PriceCalculationRequest(BaseModel):
    vehicle_id: int
    rate_plan_id: int
    pickup_location_id: int
    dropoff_location_id: int
    start_date: date
    end_date: date
    include_insurance: bool = False


class PriceCalculationResponse(BaseModel):
    base_price: float
    discount_amount: float
    one_way_fee_amount: float
    insurance_amount: float
    total_price: float
    rental_days: int
