from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class LocationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    address: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=1, max_length=100)
    zip_code: str = Field(..., min_length=1, max_length=20)
    phone: str = Field(..., min_length=1, max_length=50)
    email: Optional[EmailStr] = None


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    address: Optional[str] = Field(None, min_length=1)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = Field(None, min_length=1, max_length=100)
    zip_code: Optional[str] = Field(None, min_length=1, max_length=20)
    phone: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None


class LocationResponse(LocationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
