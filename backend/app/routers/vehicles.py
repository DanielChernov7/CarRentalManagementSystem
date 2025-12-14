from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.database import get_db
from app.models.vehicle import Vehicle, VehicleStatus, VehicleType
from app.models.user import User
from app.schemas.vehicle import VehicleCreate, VehicleUpdate, VehicleResponse
from app.auth import get_current_admin, get_current_user
from app.services.availability_service import AvailabilityService

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])


@router.get("/", response_model=List[VehicleResponse])
def get_all_vehicles(
    skip: int = 0,
    limit: int = 100,
    status: Optional[VehicleStatus] = None,
    vehicle_type: Optional[VehicleType] = None,
    location_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all vehicles with optional filters"""
    query = db.query(Vehicle)

    if status:
        query = query.filter(Vehicle.status == status)
    if vehicle_type:
        query = query.filter(Vehicle.vehicle_type == vehicle_type)
    if location_id:
        query = query.filter(Vehicle.base_location_id == location_id)

    vehicles = query.offset(skip).limit(limit).all()
    return vehicles


@router.get("/available", response_model=List[VehicleResponse])
def get_available_vehicles(
    start_date: date = Query(...),
    end_date: date = Query(...),
    location_id: Optional[int] = None,
    vehicle_type: Optional[VehicleType] = None,
    db: Session = Depends(get_db)
):
    """Get available vehicles for specific date range"""
    vehicles = AvailabilityService.get_available_vehicles(
        db=db,
        start_date=start_date,
        end_date=end_date,
        location_id=location_id,
        vehicle_type=vehicle_type.value if vehicle_type else None
    )
    return vehicles


@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    """Get vehicle by ID"""
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    return vehicle


@router.get("/{vehicle_id}/availability", response_model=dict)
def check_vehicle_availability(
    vehicle_id: int,
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db)
):
    """Check if specific vehicle is available"""
    available = AvailabilityService.check_vehicle_availability(
        db=db,
        vehicle_id=vehicle_id,
        start_date=start_date,
        end_date=end_date
    )
    return {"vehicle_id": vehicle_id, "available": available}


@router.post("/", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Create new vehicle (admin only)"""
    print(f"DEBUG: Received vehicle data: {vehicle.model_dump()}")
    # Check for duplicate license plate or VIN
    existing = db.query(Vehicle).filter(
        (Vehicle.license_plate == vehicle.license_plate) |
        (Vehicle.vin == vehicle.vin)
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vehicle with this license plate or VIN already exists"
        )

    db_vehicle = Vehicle(**vehicle.model_dump())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


@router.put("/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(
    vehicle_id: int,
    vehicle: VehicleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Update vehicle (admin only)"""
    db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not db_vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )

    update_data = vehicle.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_vehicle, field, value)

    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Delete vehicle (admin only)"""
    db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not db_vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )

    db.delete(db_vehicle)
    db.commit()
    return None
