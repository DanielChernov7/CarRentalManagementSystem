from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app.models.damage_report import DamageReport, DamageReportStatus
from app.models.user import User
from app.schemas.damage_report import DamageReportCreate, DamageReportUpdate, DamageReportResponse
from app.auth import get_current_admin_or_clerk, get_current_user

router = APIRouter(prefix="/damage-reports", tags=["Damage Reports"])


@router.get("/", response_model=List[DamageReportResponse])
def get_damage_reports(
    skip: int = 0,
    limit: int = 100,
    status: DamageReportStatus = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_clerk)
):
    """Get all damage reports (admin/clerk only)"""
    query = db.query(DamageReport)

    if status:
        query = query.filter(DamageReport.status == status)

    reports = query.offset(skip).limit(limit).all()
    return reports


@router.get("/{report_id}", response_model=DamageReportResponse)
def get_damage_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_clerk)
):
    """Get damage report by ID"""
    report = db.query(DamageReport).filter(DamageReport.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Damage report not found"
        )
    return report


@router.get("/reservation/{reservation_id}", response_model=List[DamageReportResponse])
def get_damage_reports_by_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get damage reports for a reservation"""
    reports = db.query(DamageReport).filter(
        DamageReport.reservation_id == reservation_id
    ).all()
    return reports


@router.get("/vehicle/{vehicle_id}", response_model=List[DamageReportResponse])
def get_damage_reports_by_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_clerk)
):
    """Get damage reports for a vehicle"""
    reports = db.query(DamageReport).filter(
        DamageReport.vehicle_id == vehicle_id
    ).all()
    return reports


@router.post("/", response_model=DamageReportResponse, status_code=status.HTTP_201_CREATED)
def create_damage_report(
    report: DamageReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_clerk)
):
    """Create new damage report (clerk/admin only)"""
    db_report = DamageReport(**report.model_dump())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


@router.put("/{report_id}", response_model=DamageReportResponse)
def update_damage_report(
    report_id: int,
    report: DamageReportUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_clerk)
):
    """Update damage report (clerk/admin only)"""
    db_report = db.query(DamageReport).filter(DamageReport.id == report_id).first()
    if not db_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Damage report not found"
        )

    update_data = report.model_dump(exclude_unset=True)

    # If marking as resolved, set resolved_at
    if update_data.get("status") == DamageReportStatus.RESOLVED:
        update_data["resolved_at"] = datetime.utcnow()

    for field, value in update_data.items():
        setattr(db_report, field, value)

    db.commit()
    db.refresh(db_report)
    return db_report


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_damage_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_clerk)
):
    """Delete damage report (admin only)"""
    db_report = db.query(DamageReport).filter(DamageReport.id == report_id).first()
    if not db_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Damage report not found"
        )

    db.delete(db_report)
    db.commit()
    return None
