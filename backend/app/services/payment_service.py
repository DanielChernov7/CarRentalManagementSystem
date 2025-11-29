import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.payment import Payment, PaymentStatus
from app.models.reservation import Reservation, ReservationStatus
from app.models.vehicle import Vehicle, VehicleStatus


class PaymentService:
    """Service for processing payments with transaction management"""

    @staticmethod
    def process_payment_and_confirm_reservation(
        db: Session,
        payment: Payment
    ) -> tuple[bool, str]:
        """
        Process payment and confirm reservation atomically

        This is a transactional operation that ensures:
        1. Payment is processed successfully
        2. Reservation is confirmed
        3. Vehicle status is updated

        If any step fails, the entire transaction is rolled back.

        Returns:
            tuple of (success: bool, message: str)
        """
        try:
            # Start transaction (handled by FastAPI dependency)

            # Generate transaction ID
            payment.transaction_id = f"TXN-{uuid.uuid4().hex[:16].upper()}"

            # Process payment (polymorphic payment processing)
            success = payment.process()

            if not success:
                payment.status = PaymentStatus.FAILED
                db.add(payment)
                db.commit()
                return False, "Payment processing failed"

            # Get associated reservation
            reservation = db.query(Reservation).filter(
                Reservation.id == payment.reservation_id
            ).first()

            if not reservation:
                payment.status = PaymentStatus.FAILED
                db.add(payment)
                db.commit()
                return False, "Reservation not found"

            # Confirm reservation (encapsulated business logic)
            if not reservation.confirm():
                payment.status = PaymentStatus.FAILED
                db.add(payment)
                db.commit()
                return False, "Reservation cannot be confirmed"

            # Update vehicle status
            vehicle = db.query(Vehicle).filter(
                Vehicle.id == reservation.vehicle_id
            ).first()

            if vehicle:
                vehicle.status = VehicleStatus.RESERVED

            # Save all changes
            db.add(payment)
            db.add(reservation)
            if vehicle:
                db.add(vehicle)

            db.commit()

            return True, "Payment processed and reservation confirmed successfully"

        except Exception as e:
            db.rollback()
            return False, f"Transaction failed: {str(e)}"

    @staticmethod
    def refund_payment(db: Session, payment_id: int) -> tuple[bool, str]:
        """
        Refund a payment and cancel associated reservation

        Returns:
            tuple of (success: bool, message: str)
        """
        try:
            payment = db.query(Payment).filter(Payment.id == payment_id).first()

            if not payment:
                return False, "Payment not found"

            if not payment.refund():
                return False, "Payment cannot be refunded"

            # Cancel reservation
            reservation = db.query(Reservation).filter(
                Reservation.id == payment.reservation_id
            ).first()

            if reservation:
                reservation.cancel()

                # Update vehicle status
                vehicle = db.query(Vehicle).filter(
                    Vehicle.id == reservation.vehicle_id
                ).first()

                if vehicle:
                    vehicle.status = VehicleStatus.AVAILABLE

            db.commit()
            return True, "Payment refunded successfully"

        except Exception as e:
            db.rollback()
            return False, f"Refund failed: {str(e)}"
