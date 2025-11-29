from datetime import date
from sqlalchemy.orm import Session
from app.models.vehicle import Vehicle
from app.models.rate_plan import RatePlan
from app.models.location import Location


class PricingService:
    """Service for calculating rental prices - implements abstraction"""

    @staticmethod
    def calculate_price(
        db: Session,
        vehicle_id: int,
        rate_plan_id: int,
        pickup_location_id: int,
        dropoff_location_id: int,
        start_date: date,
        end_date: date,
        include_insurance: bool = False
    ) -> dict:
        """
        Calculate total rental price including all fees

        Returns:
            dict with base_price, discount_amount, one_way_fee_amount,
            insurance_amount, total_price, rental_days
        """
        # Get vehicle
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            raise ValueError(f"Vehicle {vehicle_id} not found")

        # Get rate plan
        rate_plan = db.query(RatePlan).filter(RatePlan.id == rate_plan_id).first()
        if not rate_plan:
            raise ValueError(f"Rate plan {rate_plan_id} not found")

        if not rate_plan.is_active:
            raise ValueError(f"Rate plan {rate_plan.name} is not active")

        # Calculate rental days
        rental_days = (end_date - start_date).days
        if rental_days < 1:
            raise ValueError("Rental must be at least 1 day")

        # Validate rental days against rate plan constraints
        if rental_days < rate_plan.min_days:
            raise ValueError(f"Minimum rental period is {rate_plan.min_days} days for this rate plan")
        if rate_plan.max_days and rental_days > rate_plan.max_days:
            raise ValueError(f"Maximum rental period is {rate_plan.max_days} days for this rate plan")

        # Calculate base price
        base_price = vehicle.daily_rate * rental_days

        # Calculate discount
        discount_amount = base_price * (rate_plan.discount_percentage / 100)

        # Calculate one-way fee
        one_way_fee_amount = 0.0
        if pickup_location_id != dropoff_location_id:
            one_way_fee_amount = rate_plan.one_way_fee

        # Calculate insurance
        insurance_amount = 0.0
        if include_insurance:
            insurance_amount = rate_plan.insurance_daily_rate * rental_days

        # Calculate total
        total_price = base_price - discount_amount + one_way_fee_amount + insurance_amount

        return {
            "base_price": round(base_price, 2),
            "discount_amount": round(discount_amount, 2),
            "one_way_fee_amount": round(one_way_fee_amount, 2),
            "insurance_amount": round(insurance_amount, 2),
            "total_price": round(total_price, 2),
            "rental_days": rental_days
        }
