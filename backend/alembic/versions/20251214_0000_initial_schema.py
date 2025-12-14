"""Initial database schema

Revision ID: 20251214_0000
Revises:
Create Date: 2025-12-14 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20251214_0000'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('role', sa.Enum('customer', 'admin', 'clerk', name='userrole'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # Create locations table
    op.create_table(
        'locations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('address', sa.Text(), nullable=False),
        sa.Column('city', sa.String(length=100), nullable=False),
        sa.Column('state', sa.String(length=100), nullable=False),
        sa.Column('zip_code', sa.String(length=20), nullable=False),
        sa.Column('phone', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_locations_city'), 'locations', ['city'], unique=False)
    op.create_index(op.f('ix_locations_id'), 'locations', ['id'], unique=False)

    # Create rate_plans table
    op.create_table(
        'rate_plans',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('discount_percentage', sa.Float(), nullable=True),
        sa.Column('one_way_fee', sa.Float(), nullable=True),
        sa.Column('insurance_daily_rate', sa.Float(), nullable=True),
        sa.Column('min_days', sa.Integer(), nullable=True),
        sa.Column('max_days', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_rate_plans_id'), 'rate_plans', ['id'], unique=False)
    op.create_index(op.f('ix_rate_plans_is_active'), 'rate_plans', ['is_active'], unique=False)

    # Create vehicles table
    op.create_table(
        'vehicles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('make', sa.String(length=100), nullable=False),
        sa.Column('model', sa.String(length=100), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('license_plate', sa.String(length=50), nullable=False),
        sa.Column('vin', sa.String(length=100), nullable=False),
        sa.Column('color', sa.String(length=50), nullable=True),
        sa.Column('vehicle_type', sa.Enum('sedan', 'suv', 'truck', 'van', 'luxury', 'economy', name='vehicletype'), nullable=False),
        sa.Column('status', sa.Enum('available', 'reserved', 'rented', 'maintenance', 'out_of_service', name='vehiclestatus'), nullable=False),
        sa.Column('mileage', sa.Integer(), nullable=True),
        sa.Column('daily_rate', sa.Float(), nullable=False),
        sa.Column('base_location_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['base_location_id'], ['locations.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('license_plate'),
        sa.UniqueConstraint('vin')
    )
    op.create_index(op.f('ix_vehicles_base_location_id'), 'vehicles', ['base_location_id'], unique=False)
    op.create_index(op.f('ix_vehicles_id'), 'vehicles', ['id'], unique=False)
    op.create_index(op.f('ix_vehicles_license_plate'), 'vehicles', ['license_plate'], unique=False)
    op.create_index(op.f('ix_vehicles_status'), 'vehicles', ['status'], unique=False)
    op.create_index(op.f('ix_vehicles_vehicle_type'), 'vehicles', ['vehicle_type'], unique=False)
    op.create_index('idx_vehicle_status_type', 'vehicles', ['status', 'vehicle_type'], unique=False)

    # Create reservations table
    op.create_table(
        'reservations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('customer_id', sa.Integer(), nullable=False),
        sa.Column('vehicle_id', sa.Integer(), nullable=False),
        sa.Column('rate_plan_id', sa.Integer(), nullable=False),
        sa.Column('pickup_location_id', sa.Integer(), nullable=False),
        sa.Column('dropoff_location_id', sa.Integer(), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('base_price', sa.Float(), nullable=False),
        sa.Column('discount_amount', sa.Float(), nullable=True),
        sa.Column('one_way_fee_amount', sa.Float(), nullable=True),
        sa.Column('insurance_amount', sa.Float(), nullable=True),
        sa.Column('total_price', sa.Float(), nullable=False),
        sa.Column('status', sa.Enum('pending', 'confirmed', 'active', 'completed', 'cancelled', name='reservationstatus'), nullable=False),
        sa.Column('include_insurance', sa.Boolean(), nullable=True),
        sa.Column('special_requests', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('confirmed_at', sa.DateTime(), nullable=True),
        sa.Column('cancelled_at', sa.DateTime(), nullable=True),
        sa.CheckConstraint('end_date > start_date', name='check_end_after_start'),
        sa.ForeignKeyConstraint(['customer_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['dropoff_location_id'], ['locations.id'], ),
        sa.ForeignKeyConstraint(['pickup_location_id'], ['locations.id'], ),
        sa.ForeignKeyConstraint(['rate_plan_id'], ['rate_plans.id'], ),
        sa.ForeignKeyConstraint(['vehicle_id'], ['vehicles.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reservations_created_at'), 'reservations', ['created_at'], unique=False)
    op.create_index(op.f('ix_reservations_customer_id'), 'reservations', ['customer_id'], unique=False)
    op.create_index(op.f('ix_reservations_dropoff_location_id'), 'reservations', ['dropoff_location_id'], unique=False)
    op.create_index(op.f('ix_reservations_end_date'), 'reservations', ['end_date'], unique=False)
    op.create_index(op.f('ix_reservations_id'), 'reservations', ['id'], unique=False)
    op.create_index(op.f('ix_reservations_pickup_location_id'), 'reservations', ['pickup_location_id'], unique=False)
    op.create_index(op.f('ix_reservations_rate_plan_id'), 'reservations', ['rate_plan_id'], unique=False)
    op.create_index(op.f('ix_reservations_start_date'), 'reservations', ['start_date'], unique=False)
    op.create_index(op.f('ix_reservations_status'), 'reservations', ['status'], unique=False)
    op.create_index(op.f('ix_reservations_vehicle_id'), 'reservations', ['vehicle_id'], unique=False)
    op.create_index('idx_reservation_dates', 'reservations', ['vehicle_id', 'start_date', 'end_date'], unique=False)
    op.create_index('idx_reservation_status_dates', 'reservations', ['status', 'start_date', 'end_date'], unique=False)

    # Create payments table
    op.create_table(
        'payments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('reservation_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('payment_method', sa.Enum('credit_card', 'debit_card', 'cash', 'paypal', name='paymentmethod'), nullable=False),
        sa.Column('status', sa.Enum('pending', 'processing', 'completed', 'failed', 'refunded', name='paymentstatus'), nullable=False),
        sa.Column('transaction_id', sa.String(length=255), nullable=True),
        sa.Column('payment_details', sa.String(length=500), nullable=True),
        sa.Column('processed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['reservation_id'], ['reservations.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('transaction_id')
    )
    op.create_index(op.f('ix_payments_id'), 'payments', ['id'], unique=False)
    op.create_index(op.f('ix_payments_reservation_id'), 'payments', ['reservation_id'], unique=False)
    op.create_index(op.f('ix_payments_status'), 'payments', ['status'], unique=False)
    op.create_index(op.f('ix_payments_transaction_id'), 'payments', ['transaction_id'], unique=False)

    # Create inspections table
    op.create_table(
        'inspections',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('reservation_id', sa.Integer(), nullable=False),
        sa.Column('vehicle_id', sa.Integer(), nullable=False),
        sa.Column('clerk_id', sa.Integer(), nullable=False),
        sa.Column('inspection_type', sa.Enum('pre_rental', 'post_rental', name='inspectiontype'), nullable=False),
        sa.Column('status', sa.Enum('pending', 'in_progress', 'completed', name='inspectionstatus'), nullable=False),
        sa.Column('exterior_condition', sa.String(length=50), nullable=True),
        sa.Column('interior_condition', sa.String(length=50), nullable=True),
        sa.Column('tire_condition', sa.String(length=50), nullable=True),
        sa.Column('fuel_level', sa.Integer(), nullable=True),
        sa.Column('mileage', sa.Integer(), nullable=False),
        sa.Column('has_damages', sa.Boolean(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('inspected_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['clerk_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['reservation_id'], ['reservations.id'], ),
        sa.ForeignKeyConstraint(['vehicle_id'], ['vehicles.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_inspections_clerk_id'), 'inspections', ['clerk_id'], unique=False)
    op.create_index(op.f('ix_inspections_id'), 'inspections', ['id'], unique=False)
    op.create_index(op.f('ix_inspections_reservation_id'), 'inspections', ['reservation_id'], unique=False)
    op.create_index(op.f('ix_inspections_vehicle_id'), 'inspections', ['vehicle_id'], unique=False)

    # Create damage_reports table
    op.create_table(
        'damage_reports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('reservation_id', sa.Integer(), nullable=False),
        sa.Column('vehicle_id', sa.Integer(), nullable=False),
        sa.Column('damage_description', sa.Text(), nullable=False),
        sa.Column('damage_severity', sa.Enum('minor', 'moderate', 'severe', 'total_loss', name='damageseverity'), nullable=False),
        sa.Column('status', sa.Enum('reported', 'under_review', 'approved', 'rejected', 'resolved', name='damagereportstatus'), nullable=False),
        sa.Column('estimated_repair_cost', sa.Float(), nullable=True),
        sa.Column('actual_repair_cost', sa.Float(), nullable=True),
        sa.Column('customer_liable', sa.Boolean(), nullable=True),
        sa.Column('insurance_claim_filed', sa.Boolean(), nullable=True),
        sa.Column('photos_url', sa.String(length=500), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('reported_at', sa.DateTime(), nullable=True),
        sa.Column('resolved_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['reservation_id'], ['reservations.id'], ),
        sa.ForeignKeyConstraint(['vehicle_id'], ['vehicles.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_damage_reports_id'), 'damage_reports', ['id'], unique=False)
    op.create_index(op.f('ix_damage_reports_reservation_id'), 'damage_reports', ['reservation_id'], unique=False)
    op.create_index(op.f('ix_damage_reports_status'), 'damage_reports', ['status'], unique=False)
    op.create_index(op.f('ix_damage_reports_vehicle_id'), 'damage_reports', ['vehicle_id'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index(op.f('ix_damage_reports_vehicle_id'), table_name='damage_reports')
    op.drop_index(op.f('ix_damage_reports_status'), table_name='damage_reports')
    op.drop_index(op.f('ix_damage_reports_reservation_id'), table_name='damage_reports')
    op.drop_index(op.f('ix_damage_reports_id'), table_name='damage_reports')
    op.drop_table('damage_reports')

    op.drop_index(op.f('ix_inspections_vehicle_id'), table_name='inspections')
    op.drop_index(op.f('ix_inspections_reservation_id'), table_name='inspections')
    op.drop_index(op.f('ix_inspections_id'), table_name='inspections')
    op.drop_index(op.f('ix_inspections_clerk_id'), table_name='inspections')
    op.drop_table('inspections')

    op.drop_index(op.f('ix_payments_transaction_id'), table_name='payments')
    op.drop_index(op.f('ix_payments_status'), table_name='payments')
    op.drop_index(op.f('ix_payments_reservation_id'), table_name='payments')
    op.drop_index(op.f('ix_payments_id'), table_name='payments')
    op.drop_table('payments')

    op.drop_index('idx_reservation_status_dates', table_name='reservations')
    op.drop_index('idx_reservation_dates', table_name='reservations')
    op.drop_index(op.f('ix_reservations_vehicle_id'), table_name='reservations')
    op.drop_index(op.f('ix_reservations_status'), table_name='reservations')
    op.drop_index(op.f('ix_reservations_start_date'), table_name='reservations')
    op.drop_index(op.f('ix_reservations_rate_plan_id'), table_name='reservations')
    op.drop_index(op.f('ix_reservations_pickup_location_id'), table_name='reservations')
    op.drop_index(op.f('ix_reservations_id'), table_name='reservations')
    op.drop_index(op.f('ix_reservations_end_date'), table_name='reservations')
    op.drop_index(op.f('ix_reservations_dropoff_location_id'), table_name='reservations')
    op.drop_index(op.f('ix_reservations_customer_id'), table_name='reservations')
    op.drop_index(op.f('ix_reservations_created_at'), table_name='reservations')
    op.drop_table('reservations')

    op.drop_index('idx_vehicle_status_type', table_name='vehicles')
    op.drop_index(op.f('ix_vehicles_vehicle_type'), table_name='vehicles')
    op.drop_index(op.f('ix_vehicles_status'), table_name='vehicles')
    op.drop_index(op.f('ix_vehicles_license_plate'), table_name='vehicles')
    op.drop_index(op.f('ix_vehicles_id'), table_name='vehicles')
    op.drop_index(op.f('ix_vehicles_base_location_id'), table_name='vehicles')
    op.drop_table('vehicles')

    op.drop_index(op.f('ix_rate_plans_is_active'), table_name='rate_plans')
    op.drop_index(op.f('ix_rate_plans_id'), table_name='rate_plans')
    op.drop_table('rate_plans')

    op.drop_index(op.f('ix_locations_id'), table_name='locations')
    op.drop_index(op.f('ix_locations_city'), table_name='locations')
    op.drop_table('locations')

    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
