from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RatePlanBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    discount_percentage: float = Field(0.0, ge=0, le=100)
    one_way_fee: float = Field(0.0, ge=0)
    insurance_daily_rate: float = Field(0.0, ge=0)
    min_days: int = Field(1, ge=1)
    max_days: Optional[int] = Field(None, ge=1)
    is_active: bool = True


class RatePlanCreate(RatePlanBase):
    pass


class RatePlanUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    discount_percentage: Optional[float] = Field(None, ge=0, le=100)
    one_way_fee: Optional[float] = Field(None, ge=0)
    insurance_daily_rate: Optional[float] = Field(None, ge=0)
    min_days: Optional[int] = Field(None, ge=1)
    max_days: Optional[int] = Field(None, ge=1)
    is_active: Optional[bool] = None


class RatePlanResponse(RatePlanBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
