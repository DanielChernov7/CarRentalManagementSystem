"""
Database seeding script for Car Rental Management System

This script populates the database with initial test data including:
- Admin, clerk, and customer users
- Locations (rental offices)
- Rate plans
- Vehicles
- Sample reservations, payments, inspections, and damage reports

Run with: python seed.py
"""

import sys
from datetime import datetime, date
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parent))

from app.database import SessionLocal
from app.auth import get_password_hash
from app.models.user import User, UserRole
from app.models.location import Location
from app.models.rate_plan import RatePlan
from app.models.vehicle import Vehicle, VehicleType, VehicleStatus
from app.models.reservation import Reservation, ReservationStatus
from app.models.payment import Payment, PaymentMethod, PaymentStatus
from app.models.inspection import Inspection, InspectionType, InspectionStatus
from app.models.damage_report import DamageReport, DamageSeverity, DamageReportStatus


def seed_database():
    """Seed the database with initial data"""
    db = SessionLocal()

    try:
        print("Starting database seeding...")

        # Check if data already exists
        if db.query(User).count() > 0:
            print("Database already contains data. Skipping seed.")
            return

        # Password for all users: "password123"
        hashed_password = get_password_hash("password123")

        # Create users
        print("Creating users...")
        users = [
            User(
                email="admin@carrental.com",
                hashed_password=hashed_password,
                full_name="Admin User",
                phone="555-0001",
                role=UserRole.ADMIN
            ),
            User(
                email="clerk@carrental.com",
                hashed_password=hashed_password,
                full_name="Clerk User",
                phone="555-0002",
                role=UserRole.CLERK
            ),
            User(
                email="john.doe@email.com",
                hashed_password=hashed_password,
                full_name="John Doe",
                phone="555-1001",
                role=UserRole.CUSTOMER
            ),
            User(
                email="jane.smith@email.com",
                hashed_password=hashed_password,
                full_name="Jane Smith",
                phone="555-1002",
                role=UserRole.CUSTOMER
            ),
            User(
                email="bob.johnson@email.com",
                hashed_password=hashed_password,
                full_name="Bob Johnson",
                phone="555-1003",
                role=UserRole.CUSTOMER
            ),
        ]
        db.add_all(users)
        db.commit()
        print(f"Created {len(users)} users")

        # Create locations
        print("Creating locations...")
        locations = [
            Location(
                name="Downtown Branch",
                address="123 Main Street",
                city="New York",
                state="NY",
                zip_code="10001",
                phone="555-2001",
                email="downtown@carrental.com"
            ),
            Location(
                name="Airport Branch",
                address="456 Airport Road",
                city="New York",
                state="NY",
                zip_code="10002",
                phone="555-2002",
                email="airport@carrental.com"
            ),
            Location(
                name="Suburban Branch",
                address="789 Oak Avenue",
                city="Brooklyn",
                state="NY",
                zip_code="11201",
                phone="555-2003",
                email="suburban@carrental.com"
            ),
            Location(
                name="Los Angeles Downtown",
                address="321 Sunset Blvd",
                city="Los Angeles",
                state="CA",
                zip_code="90001",
                phone="555-3001",
                email="la@carrental.com"
            ),
            Location(
                name="LAX Airport",
                address="654 Airport Blvd",
                city="Los Angeles",
                state="CA",
                zip_code="90045",
                phone="555-3002",
                email="lax@carrental.com"
            ),
        ]
        db.add_all(locations)
        db.commit()
        print(f"Created {len(locations)} locations")

        # Create rate plans
        print("Creating rate plans...")
        rate_plans = [
            RatePlan(
                name="Standard Plan",
                description="Basic rental plan with no discounts",
                discount_percentage=0.0,
                one_way_fee=50.00,
                insurance_daily_rate=15.00,
                min_days=1,
                max_days=None,
                is_active=True
            ),
            RatePlan(
                name="Weekend Special",
                description="10% discount for weekend rentals",
                discount_percentage=10.0,
                one_way_fee=50.00,
                insurance_daily_rate=15.00,
                min_days=2,
                max_days=3,
                is_active=True
            ),
            RatePlan(
                name="Weekly Saver",
                description="15% discount for weekly rentals",
                discount_percentage=15.0,
                one_way_fee=75.00,
                insurance_daily_rate=12.00,
                min_days=7,
                max_days=14,
                is_active=True
            ),
            RatePlan(
                name="Monthly Premium",
                description="25% discount for monthly rentals",
                discount_percentage=25.0,
                one_way_fee=100.00,
                insurance_daily_rate=10.00,
                min_days=30,
                max_days=None,
                is_active=True
            ),
            RatePlan(
                name="Corporate Plan",
                description="20% discount for business customers",
                discount_percentage=20.0,
                one_way_fee=50.00,
                insurance_daily_rate=10.00,
                min_days=1,
                max_days=None,
                is_active=True
            ),
        ]
        db.add_all(rate_plans)
        db.commit()
        print(f"Created {len(rate_plans)} rate plans")

        # Create vehicles
        print("Creating vehicles...")
        vehicles = [
            # Location 1 (Downtown Branch)
            Vehicle(make="Toyota", model="Camry", year=2023, license_plate="ABC-1001",
                    vin="1HGBH41JXMN109186", color="Silver", vehicle_type=VehicleType.SEDAN,
                    status=VehicleStatus.AVAILABLE, mileage=12500, daily_rate=45.00, base_location_id=1),
            Vehicle(make="Honda", model="Civic", year=2023, license_plate="ABC-1002",
                    vin="2HGFG12838H543210", color="Blue", vehicle_type=VehicleType.SEDAN,
                    status=VehicleStatus.AVAILABLE, mileage=8900, daily_rate=40.00, base_location_id=1),
            Vehicle(make="Ford", model="Explorer", year=2023, license_plate="ABC-1003",
                    vin="1FMCU9GD5KUA12345", color="Black", vehicle_type=VehicleType.SUV,
                    status=VehicleStatus.AVAILABLE, mileage=15200, daily_rate=65.00, base_location_id=1),
            Vehicle(make="Chevrolet", model="Malibu", year=2022, license_plate="ABC-1004",
                    vin="1G1ZD5ST5MF123456", color="White", vehicle_type=VehicleType.SEDAN,
                    status=VehicleStatus.AVAILABLE, mileage=22100, daily_rate=42.00, base_location_id=1),

            # Location 2 (Airport Branch)
            Vehicle(make="Nissan", model="Altima", year=2023, license_plate="XYZ-2001",
                    vin="1N4AL3AP5JC123456", color="Red", vehicle_type=VehicleType.SEDAN,
                    status=VehicleStatus.AVAILABLE, mileage=9500, daily_rate=43.00, base_location_id=2),
            Vehicle(make="Toyota", model="RAV4", year=2023, license_plate="XYZ-2002",
                    vin="2T3BFREV5HW123456", color="Gray", vehicle_type=VehicleType.SUV,
                    status=VehicleStatus.AVAILABLE, mileage=11200, daily_rate=60.00, base_location_id=2),
            Vehicle(make="Honda", model="CR-V", year=2023, license_plate="XYZ-2003",
                    vin="2HKRM3H74NH123456", color="Green", vehicle_type=VehicleType.SUV,
                    status=VehicleStatus.AVAILABLE, mileage=13400, daily_rate=58.00, base_location_id=2),
            Vehicle(make="BMW", model="3 Series", year=2023, license_plate="XYZ-2004",
                    vin="WBA8E1C55HK123456", color="Black", vehicle_type=VehicleType.LUXURY,
                    status=VehicleStatus.AVAILABLE, mileage=7800, daily_rate=95.00, base_location_id=2),

            # Location 3 (Suburban Branch)
            Vehicle(make="Ford", model="F-150", year=2023, license_plate="DEF-3001",
                    vin="1FTEW1E50MFB12345", color="Blue", vehicle_type=VehicleType.TRUCK,
                    status=VehicleStatus.AVAILABLE, mileage=18900, daily_rate=70.00, base_location_id=3),
            Vehicle(make="Chevrolet", model="Silverado", year=2023, license_plate="DEF-3002",
                    vin="1GC4YPE74NF123456", color="Silver", vehicle_type=VehicleType.TRUCK,
                    status=VehicleStatus.AVAILABLE, mileage=16700, daily_rate=72.00, base_location_id=3),
            Vehicle(make="Dodge", model="Grand Caravan", year=2022, license_plate="DEF-3003",
                    vin="2C4RDGCG5LR123456", color="White", vehicle_type=VehicleType.VAN,
                    status=VehicleStatus.AVAILABLE, mileage=21300, daily_rate=55.00, base_location_id=3),
            Vehicle(make="Hyundai", model="Elantra", year=2023, license_plate="DEF-3004",
                    vin="5NPD84LF5NH123456", color="Gray", vehicle_type=VehicleType.ECONOMY,
                    status=VehicleStatus.AVAILABLE, mileage=6200, daily_rate=35.00, base_location_id=3),

            # Location 4 (LA Downtown)
            Vehicle(make="Mercedes-Benz", model="E-Class", year=2023, license_plate="CAL-4001",
                    vin="WDDZF4JB5LA123456", color="Silver", vehicle_type=VehicleType.LUXURY,
                    status=VehicleStatus.AVAILABLE, mileage=9100, daily_rate=110.00, base_location_id=4),
            Vehicle(make="Audi", model="A4", year=2023, license_plate="CAL-4002",
                    vin="WAUFFAFL8DN123456", color="Black", vehicle_type=VehicleType.LUXURY,
                    status=VehicleStatus.AVAILABLE, mileage=8300, daily_rate=100.00, base_location_id=4),
            Vehicle(make="Toyota", model="Corolla", year=2023, license_plate="CAL-4003",
                    vin="5YFS4RCE8NP123456", color="White", vehicle_type=VehicleType.ECONOMY,
                    status=VehicleStatus.AVAILABLE, mileage=7500, daily_rate=38.00, base_location_id=4),

            # Location 5 (LAX Airport)
            Vehicle(make="Jeep", model="Wrangler", year=2023, license_plate="LAX-5001",
                    vin="1C4HJXDG5NW123456", color="Orange", vehicle_type=VehicleType.SUV,
                    status=VehicleStatus.AVAILABLE, mileage=14200, daily_rate=68.00, base_location_id=5),
            Vehicle(make="GMC", model="Yukon", year=2023, license_plate="LAX-5002",
                    vin="1GKS1BKC5NR123456", color="Black", vehicle_type=VehicleType.SUV,
                    status=VehicleStatus.AVAILABLE, mileage=12800, daily_rate=85.00, base_location_id=5),
            Vehicle(make="Mazda", model="CX-5", year=2023, license_plate="LAX-5003",
                    vin="JM3KFBCM5N0123456", color="Red", vehicle_type=VehicleType.SUV,
                    status=VehicleStatus.AVAILABLE, mileage=10900, daily_rate=56.00, base_location_id=5),
        ]
        db.add_all(vehicles)
        db.commit()
        print(f"Created {len(vehicles)} vehicles")

        # Create sample reservations
        print("Creating reservations...")
        reservations = [
            # Confirmed reservation
            Reservation(
                customer_id=3, vehicle_id=3, rate_plan_id=1,
                pickup_location_id=1, dropoff_location_id=1,
                start_date=date(2025, 11, 1), end_date=date(2025, 11, 5),
                base_price=260.00, discount_amount=0.00, one_way_fee_amount=0.00,
                insurance_amount=60.00, total_price=320.00,
                status=ReservationStatus.CONFIRMED, include_insurance=True
            ),
            # Pending reservation
            Reservation(
                customer_id=4, vehicle_id=5, rate_plan_id=2,
                pickup_location_id=2, dropoff_location_id=2,
                start_date=date(2025, 11, 10), end_date=date(2025, 11, 13),
                base_price=129.00, discount_amount=12.90, one_way_fee_amount=0.00,
                insurance_amount=45.00, total_price=161.10,
                status=ReservationStatus.PENDING, include_insurance=True
            ),
            # Active reservation
            Reservation(
                customer_id=5, vehicle_id=1, rate_plan_id=1,
                pickup_location_id=1, dropoff_location_id=2,
                start_date=date(2025, 11, 15), end_date=date(2025, 11, 18),
                base_price=135.00, discount_amount=0.00, one_way_fee_amount=50.00,
                insurance_amount=0.00, total_price=185.00,
                status=ReservationStatus.ACTIVE, include_insurance=False
            ),
            # Completed reservation
            Reservation(
                customer_id=3, vehicle_id=8, rate_plan_id=3,
                pickup_location_id=2, dropoff_location_id=2,
                start_date=date(2025, 10, 20), end_date=date(2025, 10, 27),
                base_price=665.00, discount_amount=99.75, one_way_fee_amount=0.00,
                insurance_amount=84.00, total_price=649.25,
                status=ReservationStatus.COMPLETED, include_insurance=True
            ),
        ]
        db.add_all(reservations)
        db.commit()
        print(f"Created {len(reservations)} reservations")

        # Create sample payments
        print("Creating payments...")
        payments = [
            Payment(
                reservation_id=1, amount=320.00, payment_method=PaymentMethod.CREDIT_CARD,
                status=PaymentStatus.COMPLETED, transaction_id="TXN-A1B2C3D4E5F6G7H8",
                processed_at=datetime(2025, 10, 25, 14, 30, 0)
            ),
            Payment(
                reservation_id=3, amount=185.00, payment_method=PaymentMethod.CREDIT_CARD,
                status=PaymentStatus.COMPLETED, transaction_id="TXN-H8G7F6E5D4C3B2A1",
                processed_at=datetime(2025, 11, 14, 9, 15, 0)
            ),
            Payment(
                reservation_id=4, amount=649.25, payment_method=PaymentMethod.DEBIT_CARD,
                status=PaymentStatus.COMPLETED, transaction_id="TXN-1234567890ABCDEF",
                processed_at=datetime(2025, 10, 19, 11, 45, 0)
            ),
        ]
        db.add_all(payments)
        db.commit()
        print(f"Created {len(payments)} payments")

        # Create sample inspections
        print("Creating inspections...")
        inspections = [
            # Pre-rental inspection
            Inspection(
                reservation_id=1, vehicle_id=3, clerk_id=2,
                inspection_type=InspectionType.PRE_RENTAL, status=InspectionStatus.COMPLETED,
                exterior_condition="excellent", interior_condition="excellent",
                tire_condition="good", fuel_level=100, mileage=15200,
                has_damages=False, notes="Vehicle in great condition",
                inspected_at=datetime(2025, 10, 31, 10, 0, 0)
            ),
            # Post-rental inspection
            Inspection(
                reservation_id=4, vehicle_id=8, clerk_id=2,
                inspection_type=InspectionType.POST_RENTAL, status=InspectionStatus.COMPLETED,
                exterior_condition="good", interior_condition="good",
                tire_condition="good", fuel_level=50, mileage=8100,
                has_damages=False, notes="Minor dirt, cleaned. No damages.",
                inspected_at=datetime(2025, 10, 27, 16, 30, 0)
            ),
            # Active rental pre-inspection
            Inspection(
                reservation_id=3, vehicle_id=1, clerk_id=2,
                inspection_type=InspectionType.PRE_RENTAL, status=InspectionStatus.COMPLETED,
                exterior_condition="excellent", interior_condition="excellent",
                tire_condition="excellent", fuel_level=100, mileage=12500,
                has_damages=False, notes="Ready for rental",
                inspected_at=datetime(2025, 11, 14, 8, 0, 0)
            ),
        ]
        db.add_all(inspections)
        db.commit()
        print(f"Created {len(inspections)} inspections")

        # Create sample damage report
        print("Creating damage reports...")
        damage_reports = [
            DamageReport(
                reservation_id=4, vehicle_id=8,
                damage_description="Small scratch on rear bumper",
                damage_severity=DamageSeverity.MINOR,
                status=DamageReportStatus.RESOLVED,
                estimated_repair_cost=150.00,
                customer_liable=True,
                insurance_claim_filed=False,
                notes="Customer accepted responsibility. Repair completed."
            ),
        ]
        db.add_all(damage_reports)
        db.commit()
        print(f"Created {len(damage_reports)} damage reports")

        print("\n✓ Database seeding completed successfully!")
        print("\nTest credentials:")
        print("  Admin:    admin@carrental.com / password123")
        print("  Clerk:    clerk@carrental.com / password123")
        print("  Customer: john.doe@email.com  / password123")

    except Exception as e:
        print(f"\n✗ Error during seeding: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
