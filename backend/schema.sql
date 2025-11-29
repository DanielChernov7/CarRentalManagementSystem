-- Car Rental Management System Database Schema
-- MySQL/MariaDB

-- Create database
CREATE DATABASE IF NOT EXISTS car_rental_db;
USE car_rental_db;

-- Drop existing tables (in correct order due to foreign keys)
DROP TABLE IF EXISTS damage_reports;
DROP TABLE IF EXISTS inspections;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS reservations;
DROP TABLE IF EXISTS vehicles;
DROP TABLE IF EXISTS rate_plans;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS users;

-- Users table (with inheritance for Customer, Admin, Clerk)
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    role ENUM('customer', 'admin', 'clerk') NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Locations table
CREATE TABLE locations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    zip_code VARCHAR(20) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    email VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_city (city)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Rate plans table
CREATE TABLE rate_plans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    discount_percentage FLOAT DEFAULT 0.0,
    one_way_fee FLOAT DEFAULT 0.0,
    insurance_daily_rate FLOAT DEFAULT 0.0,
    min_days INT DEFAULT 1,
    max_days INT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Vehicles table
CREATE TABLE vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    make VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    year INT NOT NULL,
    license_plate VARCHAR(50) NOT NULL UNIQUE,
    vin VARCHAR(100) NOT NULL UNIQUE,
    color VARCHAR(50),
    vehicle_type ENUM('sedan', 'suv', 'truck', 'van', 'luxury', 'economy') NOT NULL,
    status ENUM('available', 'reserved', 'rented', 'maintenance', 'out_of_service') NOT NULL DEFAULT 'available',
    mileage INT DEFAULT 0,
    daily_rate FLOAT NOT NULL,
    base_location_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (base_location_id) REFERENCES locations(id),
    INDEX idx_license_plate (license_plate),
    INDEX idx_status (status),
    INDEX idx_vehicle_type (vehicle_type),
    INDEX idx_base_location (base_location_id),
    INDEX idx_status_type (status, vehicle_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Reservations table
CREATE TABLE reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    rate_plan_id INT NOT NULL,
    pickup_location_id INT NOT NULL,
    dropoff_location_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    base_price FLOAT NOT NULL,
    discount_amount FLOAT DEFAULT 0.0,
    one_way_fee_amount FLOAT DEFAULT 0.0,
    insurance_amount FLOAT DEFAULT 0.0,
    total_price FLOAT NOT NULL,
    status ENUM('pending', 'confirmed', 'active', 'completed', 'cancelled') NOT NULL DEFAULT 'pending',
    include_insurance BOOLEAN DEFAULT FALSE,
    special_requests VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    confirmed_at DATETIME,
    cancelled_at DATETIME,
    FOREIGN KEY (customer_id) REFERENCES users(id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id),
    FOREIGN KEY (rate_plan_id) REFERENCES rate_plans(id),
    FOREIGN KEY (pickup_location_id) REFERENCES locations(id),
    FOREIGN KEY (dropoff_location_id) REFERENCES locations(id),
    CONSTRAINT check_end_after_start CHECK (end_date > start_date),
    INDEX idx_customer (customer_id),
    INDEX idx_vehicle (vehicle_id),
    INDEX idx_rate_plan (rate_plan_id),
    INDEX idx_pickup_location (pickup_location_id),
    INDEX idx_dropoff_location (dropoff_location_id),
    INDEX idx_start_date (start_date),
    INDEX idx_end_date (end_date),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at),
    INDEX idx_reservation_dates (vehicle_id, start_date, end_date),
    INDEX idx_reservation_status_dates (status, start_date, end_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Payments table
CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reservation_id INT NOT NULL,
    amount FLOAT NOT NULL,
    payment_method ENUM('credit_card', 'debit_card', 'cash', 'paypal') NOT NULL,
    status ENUM('pending', 'processing', 'completed', 'failed', 'refunded') NOT NULL DEFAULT 'pending',
    transaction_id VARCHAR(255) UNIQUE,
    payment_details VARCHAR(500),
    processed_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (reservation_id) REFERENCES reservations(id),
    INDEX idx_reservation (reservation_id),
    INDEX idx_transaction (transaction_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Inspections table
CREATE TABLE inspections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reservation_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    clerk_id INT NOT NULL,
    inspection_type ENUM('pre_rental', 'post_rental') NOT NULL,
    status ENUM('pending', 'in_progress', 'completed') NOT NULL DEFAULT 'pending',
    exterior_condition VARCHAR(50),
    interior_condition VARCHAR(50),
    tire_condition VARCHAR(50),
    fuel_level INT,
    mileage INT NOT NULL,
    has_damages BOOLEAN DEFAULT FALSE,
    notes TEXT,
    inspected_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (reservation_id) REFERENCES reservations(id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id),
    FOREIGN KEY (clerk_id) REFERENCES users(id),
    INDEX idx_reservation (reservation_id),
    INDEX idx_vehicle (vehicle_id),
    INDEX idx_clerk (clerk_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Damage reports table
CREATE TABLE damage_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reservation_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    damage_description TEXT NOT NULL,
    damage_severity ENUM('minor', 'moderate', 'severe', 'total_loss') NOT NULL,
    status ENUM('reported', 'under_review', 'approved', 'rejected', 'resolved') NOT NULL DEFAULT 'reported',
    estimated_repair_cost FLOAT DEFAULT 0.0,
    actual_repair_cost FLOAT,
    customer_liable BOOLEAN DEFAULT TRUE,
    insurance_claim_filed BOOLEAN DEFAULT FALSE,
    photos_url VARCHAR(500),
    notes TEXT,
    reported_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    resolved_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (reservation_id) REFERENCES reservations(id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id),
    INDEX idx_reservation (reservation_id),
    INDEX idx_vehicle (vehicle_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
