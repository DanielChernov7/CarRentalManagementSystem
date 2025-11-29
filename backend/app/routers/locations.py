from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.location import Location
from app.models.user import User
from app.schemas.location import LocationCreate, LocationUpdate, LocationResponse
from app.auth import get_current_admin, get_current_user

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.get("/", response_model=List[LocationResponse])
def get_all_locations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all locations (public endpoint)"""
    locations = db.query(Location).offset(skip).limit(limit).all()
    return locations


@router.get("/{location_id}", response_model=LocationResponse)
def get_location(location_id: int, db: Session = Depends(get_db)):
    """Get location by ID"""
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )
    return location


@router.post("/", response_model=LocationResponse, status_code=status.HTTP_201_CREATED)
def create_location(
    location: LocationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Create new location (admin only)"""
    db_location = Location(**location.model_dump())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


@router.put("/{location_id}", response_model=LocationResponse)
def update_location(
    location_id: int,
    location: LocationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Update location (admin only)"""
    db_location = db.query(Location).filter(Location.id == location_id).first()
    if not db_location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )

    update_data = location.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_location, field, value)

    db.commit()
    db.refresh(db_location)
    return db_location


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Delete location (admin only)"""
    db_location = db.query(Location).filter(Location.id == location_id).first()
    if not db_location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )

    db.delete(db_location)
    db.commit()
    return None
