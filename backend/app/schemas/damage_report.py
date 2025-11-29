from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.damage_report import DamageSeverity, DamageReportStatus


class DamageReportBase(BaseModel):
    reservation_id: int
    vehicle_id: int
    damage_description: str = Field(..., min_length=1)
    damage_severity: DamageSeverity
    estimated_repair_cost: float = Field(0.0, ge=0)
    customer_liable: bool = True
    insurance_claim_filed: bool = False
    photos_url: Optional[str] = Field(None, max_length=500)
    notes: Optional[str] = None


class DamageReportCreate(DamageReportBase):
    pass


class DamageReportUpdate(BaseModel):
    damage_description: Optional[str] = Field(None, min_length=1)
    damage_severity: Optional[DamageSeverity] = None
    status: Optional[DamageReportStatus] = None
    estimated_repair_cost: Optional[float] = Field(None, ge=0)
    actual_repair_cost: Optional[float] = Field(None, ge=0)
    customer_liable: Optional[bool] = None
    insurance_claim_filed: Optional[bool] = None
    photos_url: Optional[str] = Field(None, max_length=500)
    notes: Optional[str] = None


class DamageReportResponse(DamageReportBase):
    id: int
    status: DamageReportStatus
    actual_repair_cost: Optional[float]
    reported_at: datetime
    resolved_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
