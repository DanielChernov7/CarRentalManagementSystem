from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.payment import Payment, PaymentStatus
from app.models.reservation import Reservation
from app.models.user import User, UserRole
from app.schemas.payment import PaymentCreate, PaymentUpdate, PaymentResponse
from app.auth import get_current_user, get_current_admin
from app.services.payment_service import PaymentService

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.get("/", response_model=List[PaymentResponse])
def get_payments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get payments (customers see their own, admins see all)"""
    query = db.query(Payment)

    if current_user.role == UserRole.CUSTOMER:
        # Get customer's payment IDs through reservations
        customer_reservation_ids = db.query(Reservation.id).filter(
            Reservation.customer_id == current_user.id
        ).all()
        reservation_ids = [r[0] for r in customer_reservation_ids]
        query = query.filter(Payment.reservation_id.in_(reservation_ids))

    payments = query.offset(skip).limit(limit).all()
    return payments


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get payment by ID"""
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )

    # Check authorization
    if current_user.role == UserRole.CUSTOMER:
        reservation = db.query(Reservation).filter(
            Reservation.id == payment.reservation_id
        ).first()
        if reservation and reservation.customer_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this payment"
            )

    return payment


@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create and process payment"""
    # Verify reservation exists and belongs to customer
    reservation = db.query(Reservation).filter(
        Reservation.id == payment.reservation_id
    ).first()

    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )

    if current_user.role == UserRole.CUSTOMER and reservation.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to make payment for this reservation"
        )

    # Verify payment amount matches reservation total
    if payment.amount != reservation.total_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Payment amount must be {reservation.total_price}"
        )

    # Create payment
    db_payment = Payment(**payment.model_dump())
    db.add(db_payment)
    db.flush()

    # Process payment and confirm reservation
    success, message = PaymentService.process_payment_and_confirm_reservation(db, db_payment)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

    db.refresh(db_payment)
    return db_payment


@router.post("/{payment_id}/refund", response_model=dict)
def refund_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Refund payment (admin only)"""
    success, message = PaymentService.refund_payment(db, payment_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    return {"message": message}


@router.get("/reservation/{reservation_id}", response_model=List[PaymentResponse])
def get_payments_by_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all payments for a reservation"""
    # Check authorization
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )

    if current_user.role == UserRole.CUSTOMER and reservation.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view payments for this reservation"
        )

    payments = db.query(Payment).filter(Payment.reservation_id == reservation_id).all()
    return payments
