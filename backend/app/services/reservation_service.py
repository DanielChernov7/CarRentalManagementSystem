from datetime import date
from sqlalchemy.orm import Session
from app.models.reservation import Reservation, ReservationStatus
from app.models.vehicle import Vehicle, VehicleStatus
from app.services.pricing_service import PricingService
from app.services.availability_service import AvailabilityService


class ReservationService:
    """Service for managing reservations with business logic"""

    @staticmethod
    def create_reservation(
        db: Session,
        customer_id: int,
        vehicle_id: int,
        rate_plan_id: int,
        pickup_location_id: int,
        dropoff_location_id: int,
        start_date: date,
        end_date: date,
        include_insurance: bool = False,
        special_requests: str = None
    ) -> tuple[Reservation, str]:
        """
        Create a new reservation with validation

        Returns:
            tuple of (reservation: Reservation, error: str or None)
        """
        # Check availability
        if not AvailabilityService.check_vehicle_availability(
            db, vehicle_id, start_date, end_date
        ):
            raise ValueError("Vehicle is not available for the selected dates")

        # Calculate pricing
        try:
            pricing = PricingService.calculate_price(
                db=db,
                vehicle_id=vehicle_id,
                rate_plan_id=rate_plan_id,
                pickup_location_id=pickup_location_id,
                dropoff_location_id=dropoff_location_id,
                start_date=start_date,
                end_date=end_date,
                include_insurance=include_insurance
            )
        except ValueError as e:
            raise ValueError(f"Pricing calculation failed: {str(e)}")

        # Create reservation
        reservation = Reservation(
            customer_id=customer_id,
            vehicle_id=vehicle_id,
            rate_plan_id=rate_plan_id,
            pickup_location_id=pickup_location_id,
            dropoff_location_id=dropoff_location_id,
            start_date=start_date,
            end_date=end_date,
            base_price=pricing["base_price"],
            discount_amount=pricing["discount_amount"],
            one_way_fee_amount=pricing["one_way_fee_amount"],
            insurance_amount=pricing["insurance_amount"],
            total_price=pricing["total_price"],
            include_insurance=include_insurance,
            special_requests=special_requests,
            status=ReservationStatus.PENDING
        )

        db.add(reservation)
        db.commit()
        db.refresh(reservation)

        return reservation, None

    @staticmethod
    def activate_reservation(db: Session, reservation_id: int) -> tuple[bool, str]:
        """
        Activate a reservation when customer picks up vehicle

        Returns:
            tuple of (success: bool, message: str)
        """
        reservation = db.query(Reservation).filter(
            Reservation.id == reservation_id
        ).first()

        if not reservation:
            return False, "Reservation not found"

        if not reservation.activate():
            return False, f"Cannot activate reservation in {reservation.status.value} status"

        # Update vehicle status
        vehicle = db.query(Vehicle).filter(
            Vehicle.id == reservation.vehicle_id
        ).first()

        if vehicle:
            vehicle.status = VehicleStatus.RENTED

        db.commit()
        return True, "Reservation activated successfully"

    @staticmethod
    def complete_reservation(db: Session, reservation_id: int) -> tuple[bool, str]:
        """
        Complete a reservation when vehicle is returned

        Returns:
            tuple of (success: bool, message: str)
        """
        reservation = db.query(Reservation).filter(
            Reservation.id == reservation_id
        ).first()

        if not reservation:
            return False, "Reservation not found"

        if not reservation.complete():
            return False, f"Cannot complete reservation in {reservation.status.value} status"

        # Update vehicle status
        vehicle = db.query(Vehicle).filter(
            Vehicle.id == reservation.vehicle_id
        ).first()

        if vehicle:
            vehicle.status = VehicleStatus.AVAILABLE

        db.commit()
        return True, "Reservation completed successfully"

    @staticmethod
    def cancel_reservation(db: Session, reservation_id: int) -> tuple[bool, str]:
        """
        Cancel a reservation

        Returns:
            tuple of (success: bool, message: str)
        """
        reservation = db.query(Reservation).filter(
            Reservation.id == reservation_id
        ).first()

        if not reservation:
            return False, "Reservation not found"

        if not reservation.cancel():
            return False, f"Cannot cancel reservation in {reservation.status.value} status"

        # Update vehicle status if it was reserved
        vehicle = db.query(Vehicle).filter(
            Vehicle.id == reservation.vehicle_id
        ).first()

        if vehicle and vehicle.status == VehicleStatus.RESERVED:
            vehicle.status = VehicleStatus.AVAILABLE

        db.commit()
        return True, "Reservation cancelled successfully"
