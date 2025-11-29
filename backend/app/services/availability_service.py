from datetime import date
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from app.models.vehicle import Vehicle, VehicleStatus
from app.models.reservation import Reservation, ReservationStatus


class AvailabilityService:
    """Service for checking vehicle availability - implements abstraction"""

    @staticmethod
    def check_vehicle_availability(
        db: Session,
        vehicle_id: int,
        start_date: date,
        end_date: date,
        exclude_reservation_id: int = None
    ) -> bool:
        """
        Check if a vehicle is available for the given date range

        Args:
            db: Database session
            vehicle_id: Vehicle ID to check
            start_date: Rental start date
            end_date: Rental end date
            exclude_reservation_id: Optional reservation ID to exclude from check (for updates)

        Returns:
            True if available, False otherwise
        """
        # Get vehicle
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            return False

        # Check vehicle status
        if vehicle.status not in [VehicleStatus.AVAILABLE, VehicleStatus.RESERVED]:
            return False

        # Check for overlapping reservations
        query = db.query(Reservation).filter(
            and_(
                Reservation.vehicle_id == vehicle_id,
                Reservation.status.in_([
                    ReservationStatus.PENDING,
                    ReservationStatus.CONFIRMED,
                    ReservationStatus.ACTIVE
                ]),
                or_(
                    # New reservation starts during existing reservation
                    and_(
                        Reservation.start_date <= start_date,
                        Reservation.end_date > start_date
                    ),
                    # New reservation ends during existing reservation
                    and_(
                        Reservation.start_date < end_date,
                        Reservation.end_date >= end_date
                    ),
                    # New reservation completely contains existing reservation
                    and_(
                        Reservation.start_date >= start_date,
                        Reservation.end_date <= end_date
                    )
                )
            )
        )

        # Exclude current reservation if updating
        if exclude_reservation_id:
            query = query.filter(Reservation.id != exclude_reservation_id)

        overlapping_count = query.count()
        return overlapping_count == 0

    @staticmethod
    def get_available_vehicles(
        db: Session,
        start_date: date,
        end_date: date,
        location_id: int = None,
        vehicle_type: str = None
    ) -> list[Vehicle]:
        """
        Get list of available vehicles for given criteria

        Args:
            db: Database session
            start_date: Rental start date
            end_date: Rental end date
            location_id: Optional location filter
            vehicle_type: Optional vehicle type filter

        Returns:
            List of available vehicles
        """
        # Base query for available vehicles
        query = db.query(Vehicle).filter(
            Vehicle.status.in_([VehicleStatus.AVAILABLE, VehicleStatus.RESERVED])
        )

        # Apply filters
        if location_id:
            query = query.filter(Vehicle.base_location_id == location_id)

        if vehicle_type:
            query = query.filter(Vehicle.vehicle_type == vehicle_type)

        vehicles = query.all()

        # Filter out vehicles with overlapping reservations
        available_vehicles = []
        for vehicle in vehicles:
            if AvailabilityService.check_vehicle_availability(
                db, vehicle.id, start_date, end_date
            ):
                available_vehicles.append(vehicle)

        return available_vehicles
