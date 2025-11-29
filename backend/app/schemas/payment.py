from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.payment import PaymentMethod, PaymentStatus


class PaymentBase(BaseModel):
    reservation_id: int
    amount: float = Field(..., gt=0)
    payment_method: PaymentMethod


class PaymentCreate(PaymentBase):
    payment_details: Optional[str] = Field(None, max_length=500)


class PaymentUpdate(BaseModel):
    status: Optional[PaymentStatus] = None


class PaymentResponse(BaseModel):
    id: int
    reservation_id: int
    amount: float
    payment_method: PaymentMethod
    status: PaymentStatus
    transaction_id: Optional[str]
    processed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
