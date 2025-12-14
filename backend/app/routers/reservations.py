from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.reservation import Reservation, ReservationStatus
from app.models.user import User, UserRole
from app.schemas.reservation import (
    ReservationCreate,
    ReservationUpdate,
    ReservationResponse,
    PriceCalculationRequest,
    PriceCalculationResponse
)
from app.auth import get_current_user, get_current_admin_or_clerk
from app.services.reservation_service import ReservationService
from app.services.pricing_service import PricingService

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.get("/", response_model=List[ReservationResponse])
def get_reservations(
    skip: int = 0,
    limit: int = 100,
    status: Optional[ReservationStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get reservations (customers see their own, staff see all)"""
    query = db.query(Reservation)

    # Customers can only see their own reservations
    if current_user.role == UserRole.CUSTOMER:
        query = query.filter(Reservation.customer_id == current_user.id)

    if status:
        query = query.filter(Reservation.status == status)

    reservations = query.offset(skip).limit(limit).all()
    return reservations


@router.get("/my-reservations", response_model=List[ReservationResponse])
def get_my_reservations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's reservations"""
    reservations = db.query(Reservation).filter(
        Reservation.customer_id == current_user.id
    ).offset(skip).limit(limit).all()
    return reservations


@router.get("/{reservation_id}", response_model=ReservationResponse)
def get_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get reservation by ID"""
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )

    # Check authorization
    if current_user.role == UserRole.CUSTOMER and reservation.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this reservation"
        )

    return reservation


@router.post("/calculate-price", response_model=PriceCalculationResponse)
def calculate_price(
    request: PriceCalculationRequest,
    db: Session = Depends(get_db)
):
    """Calculate price for a potential reservation"""
    try:
        pricing = PricingService.calculate_price(
            db=db,
            vehicle_id=request.vehicle_id,
            rate_plan_id=request.rate_plan_id,
            pickup_location_id=request.pickup_location_id,
            dropoff_location_id=request.dropoff_location_id,
            start_date=request.start_date,
            end_date=request.end_date,
            include_insurance=request.include_insurance
        )
        return pricing
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
def create_reservation(
    reservation: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new reservation"""
    # Set customer_id based on user role
    if current_user.role == UserRole.CUSTOMER:
        # Customer can only create reservations for themselves
        reservation.customer_id = current_user.id
    elif not reservation.customer_id:
        # Admin/Clerk must provide customer_id
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="customer_id is required for admin/clerk users"
        )

    try:
        db_reservation, error = ReservationService.create_reservation(
            db=db,
            customer_id=reservation.customer_id,
            vehicle_id=reservation.vehicle_id,
            rate_plan_id=reservation.rate_plan_id,
            pickup_location_id=reservation.pickup_location_id,
            dropoff_location_id=reservation.dropoff_location_id,
            start_date=reservation.start_date,
            end_date=reservation.end_date,
            include_insurance=reservation.include_insurance,
            special_requests=reservation.special_requests
        )
        return db_reservation
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{reservation_id}", response_model=ReservationResponse)
def update_reservation(
    reservation_id: int,
    reservation: ReservationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update reservation"""
    db_reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )

    # Check authorization
    if current_user.role == UserRole.CUSTOMER and db_reservation.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this reservation"
        )

    update_data = reservation.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_reservation, field, value)

    db.commit()
    db.refresh(db_reservation)
    return db_reservation


@router.post("/{reservation_id}/activate", response_model=dict)
def activate_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_clerk)
):
    """Activate reservation (pickup)"""
    success, message = ReservationService.activate_reservation(db, reservation_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    return {"message": message}


@router.post("/{reservation_id}/complete", response_model=dict)
def complete_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_clerk)
):
    """Complete reservation (return)"""
    success, message = ReservationService.complete_reservation(db, reservation_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    return {"message": message}


@router.post("/{reservation_id}/cancel", response_model=dict)
def cancel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cancel reservation"""
    # Get reservation
    db_reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )

    # Check authorization
    if current_user.role == UserRole.CUSTOMER and db_reservation.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to cancel this reservation"
        )

    success, message = ReservationService.cancel_reservation(db, reservation_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    return {"message": message}


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_clerk)
):
    """Delete reservation (admin/clerk only)"""
    db_reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )

    db.delete(db_reservation)
    db.commit()
    return None
