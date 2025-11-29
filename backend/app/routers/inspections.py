from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app.models.inspection import Inspection, InspectionStatus
from app.models.user import User
from app.schemas.inspection import InspectionCreate, InspectionUpdate, InspectionResponse
from app.auth import get_current_admin_or_clerk, get_current_user

router = APIRouter(prefix="/inspections", tags=["Inspections"])


@router.get("/", response_model=List[InspectionResponse])
def get_inspections(
    skip: int = 0,
    limit: int = 100,
    status: InspectionStatus = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_clerk)
):
    """Get all inspections (admin/clerk only)"""
    query = db.query(Inspection)

    if status:
        query = query.filter(Inspection.status == status)

    inspections = query.offset(skip).limit(limit).all()
    return inspections


@router.get("/{inspection_id}", response_model=InspectionResponse)
def get_inspection(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_clerk)
):
    """Get inspection by ID"""
    inspection = db.query(Inspection).filter(Inspection.id == inspection_id).first()
    if not inspection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inspection not found"
        )
    return inspection


@router.get("/reservation/{reservation_id}", response_model=List[InspectionResponse])
def get_inspections_by_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get inspections for a reservation"""
    inspections = db.query(Inspection).filter(
        Inspection.reservation_id == reservation_id
    ).all()
    return inspections


@router.get("/vehicle/{vehicle_id}", response_model=List[InspectionResponse])
def get_inspections_by_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_clerk)
):
    """Get inspections for a vehicle"""
    inspections = db.query(Inspection).filter(
        Inspection.vehicle_id == vehicle_id
    ).all()
    return inspections


@router.post("/", response_model=InspectionResponse, status_code=status.HTTP_201_CREATED)
def create_inspection(
    inspection: InspectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_clerk)
):
    """Create new inspection (clerk/admin only)"""
    # Override clerk_id with current user
    inspection.clerk_id = current_user.id

    db_inspection = Inspection(**inspection.model_dump())
    db.add(db_inspection)
    db.commit()
    db.refresh(db_inspection)
    return db_inspection


@router.put("/{inspection_id}", response_model=InspectionResponse)
def update_inspection(
    inspection_id: int,
    inspection: InspectionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_clerk)
):
    """Update inspection (clerk/admin only)"""
    db_inspection = db.query(Inspection).filter(Inspection.id == inspection_id).first()
    if not db_inspection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inspection not found"
        )

    update_data = inspection.model_dump(exclude_unset=True)

    # If marking as completed, set inspected_at
    if update_data.get("status") == InspectionStatus.COMPLETED:
        update_data["inspected_at"] = datetime.utcnow()

    for field, value in update_data.items():
        setattr(db_inspection, field, value)

    db.commit()
    db.refresh(db_inspection)
    return db_inspection


@router.delete("/{inspection_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inspection(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_clerk)
):
    """Delete inspection (admin only)"""
    db_inspection = db.query(Inspection).filter(Inspection.id == inspection_id).first()
    if not db_inspection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inspection not found"
        )

    db.delete(db_inspection)
    db.commit()
    return None
