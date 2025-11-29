-- Seed Data for Car Rental Management System
USE car_rental_db;

-- Insert sample users
-- Password for all users: "password123" (hashed with bcrypt)
INSERT INTO users (email, hashed_password, full_name, phone, role) VALUES
('admin@carrental.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7TK7E1Qyze', 'Admin User', '555-0001', 'admin'),
('clerk@carrental.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7TK7E1Qyze', 'Clerk User', '555-0002', 'clerk'),
('john.doe@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7TK7E1Qyze', 'John Doe', '555-1001', 'customer'),
('jane.smith@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7TK7E1Qyze', 'Jane Smith', '555-1002', 'customer'),
('bob.johnson@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7TK7E1Qyze', 'Bob Johnson', '555-1003', 'customer');

-- Insert locations
INSERT INTO locations (name, address, city, state, zip_code, phone, email) VALUES
('Downtown Branch', '123 Main Street', 'New York', 'NY', '10001', '555-2001', 'downtown@carrental.com'),
('Airport Branch', '456 Airport Road', 'New York', 'NY', '10002', '555-2002', 'airport@carrental.com'),
('Suburban Branch', '789 Oak Avenue', 'Brooklyn', 'NY', '11201', '555-2003', 'suburban@carrental.com'),
('Los Angeles Downtown', '321 Sunset Blvd', 'Los Angeles', 'CA', '90001', '555-3001', 'la@carrental.com'),
('LAX Airport', '654 Airport Blvd', 'Los Angeles', 'CA', '90045', '555-3002', 'lax@carrental.com');

-- Insert rate plans
INSERT INTO rate_plans (name, description, discount_percentage, one_way_fee, insurance_daily_rate, min_days, max_days, is_active) VALUES
('Standard Plan', 'Basic rental plan with no discounts', 0.0, 50.00, 15.00, 1, NULL, TRUE),
('Weekend Special', '10% discount for weekend rentals', 10.0, 50.00, 15.00, 2, 3, TRUE),
('Weekly Saver', '15% discount for weekly rentals', 15.0, 75.00, 12.00, 7, 14, TRUE),
('Monthly Premium', '25% discount for monthly rentals', 25.0, 100.00, 10.00, 30, NULL, TRUE),
('Corporate Plan', '20% discount for business customers', 20.0, 50.00, 10.00, 1, NULL, TRUE);

-- Insert vehicles
INSERT INTO vehicles (make, model, year, license_plate, vin, color, vehicle_type, status, mileage, daily_rate, base_location_id) VALUES
-- Location 1 (Downtown Branch)
('Toyota', 'Camry', 2023, 'ABC-1001', '1HGBH41JXMN109186', 'Silver', 'sedan', 'available', 12500, 45.00, 1),
('Honda', 'Civic', 2023, 'ABC-1002', '2HGFG12838H543210', 'Blue', 'sedan', 'available', 8900, 40.00, 1),
('Ford', 'Explorer', 2023, 'ABC-1003', '1FMCU9GD5KUA12345', 'Black', 'suv', 'available', 15200, 65.00, 1),
('Chevrolet', 'Malibu', 2022, 'ABC-1004', '1G1ZD5ST5MF123456', 'White', 'sedan', 'available', 22100, 42.00, 1),

-- Location 2 (Airport Branch)
('Nissan', 'Altima', 2023, 'XYZ-2001', '1N4AL3AP5JC123456', 'Red', 'sedan', 'available', 9500, 43.00, 2),
('Toyota', 'RAV4', 2023, 'XYZ-2002', '2T3BFREV5HW123456', 'Gray', 'suv', 'available', 11200, 60.00, 2),
('Honda', 'CR-V', 2023, 'XYZ-2003', '2HKRM3H74NH123456', 'Green', 'suv', 'available', 13400, 58.00, 2),
('BMW', '3 Series', 2023, 'XYZ-2004', 'WBA8E1C55HK123456', 'Black', 'luxury', 'available', 7800, 95.00, 2),

-- Location 3 (Suburban Branch)
('Ford', 'F-150', 2023, 'DEF-3001', '1FTEW1E50MFB12345', 'Blue', 'truck', 'available', 18900, 70.00, 3),
('Chevrolet', 'Silverado', 2023, 'DEF-3002', '1GC4YPE74NF123456', 'Silver', 'truck', 'available', 16700, 72.00, 3),
('Dodge', 'Grand Caravan', 2022, 'DEF-3003', '2C4RDGCG5LR123456', 'White', 'van', 'available', 21300, 55.00, 3),
('Hyundai', 'Elantra', 2023, 'DEF-3004', '5NPD84LF5NH123456', 'Gray', 'economy', 'available', 6200, 35.00, 3),

-- Location 4 (LA Downtown)
('Mercedes-Benz', 'E-Class', 2023, 'CAL-4001', 'WDDZF4JB5LA123456', 'Silver', 'luxury', 'available', 9100, 110.00, 4),
('Audi', 'A4', 2023, 'CAL-4002', 'WAUFFAFL8DN123456', 'Black', 'luxury', 'available', 8300, 100.00, 4),
('Toyota', 'Corolla', 2023, 'CAL-4003', '5YFS4RCE8NP123456', 'White', 'economy', 'available', 7500, 38.00, 4),

-- Location 5 (LAX Airport)
('Jeep', 'Wrangler', 2023, 'LAX-5001', '1C4HJXDG5NW123456', 'Orange', 'suv', 'available', 14200, 68.00, 5),
('GMC', 'Yukon', 2023, 'LAX-5002', '1GKS1BKC5NR123456', 'Black', 'suv', 'available', 12800, 85.00, 5),
('Mazda', 'CX-5', 2023, 'LAX-5003', 'JM3KFBCM5N0123456', 'Red', 'suv', 'available', 10900, 56.00, 5);

-- Insert sample reservations
INSERT INTO reservations (customer_id, vehicle_id, rate_plan_id, pickup_location_id, dropoff_location_id, start_date, end_date, base_price, discount_amount, one_way_fee_amount, insurance_amount, total_price, status, include_insurance) VALUES
-- Confirmed reservation
(3, 3, 1, 1, 1, '2025-11-01', '2025-11-05', 260.00, 0.00, 0.00, 60.00, 320.00, 'confirmed', TRUE),
-- Pending reservation
(4, 5, 2, 2, 2, '2025-11-10', '2025-11-13', 129.00, 12.90, 0.00, 45.00, 161.10, 'pending', TRUE),
-- Active reservation
(5, 1, 1, 1, 2, '2025-11-15', '2025-11-18', 135.00, 0.00, 50.00, 0.00, 185.00, 'active', FALSE),
-- Completed reservation
(3, 8, 3, 2, 2, '2025-10-20', '2025-10-27', 665.00, 99.75, 0.00, 84.00, 649.25, 'completed', TRUE);

-- Insert sample payments
INSERT INTO payments (reservation_id, amount, payment_method, status, transaction_id, processed_at) VALUES
(1, 320.00, 'credit_card', 'completed', 'TXN-A1B2C3D4E5F6G7H8', '2025-10-25 14:30:00'),
(3, 185.00, 'credit_card', 'completed', 'TXN-H8G7F6E5D4C3B2A1', '2025-11-14 09:15:00'),
(4, 649.25, 'debit_card', 'completed', 'TXN-1234567890ABCDEF', '2025-10-19 11:45:00');

-- Insert sample inspections
INSERT INTO inspections (reservation_id, vehicle_id, clerk_id, inspection_type, status, exterior_condition, interior_condition, tire_condition, fuel_level, mileage, has_damages, notes, inspected_at) VALUES
-- Pre-rental inspection
(1, 3, 2, 'pre_rental', 'completed', 'excellent', 'excellent', 'good', 100, 15200, FALSE, 'Vehicle in great condition', '2025-10-31 10:00:00'),
-- Post-rental inspection
(4, 8, 2, 'post_rental', 'completed', 'good', 'good', 'good', 50, 8100, FALSE, 'Minor dirt, cleaned. No damages.', '2025-10-27 16:30:00'),
-- Active rental pre-inspection
(3, 1, 2, 'pre_rental', 'completed', 'excellent', 'excellent', 'excellent', 100, 12500, FALSE, 'Ready for rental', '2025-11-14 08:00:00');

-- Insert sample damage report
INSERT INTO damage_reports (reservation_id, vehicle_id, damage_description, damage_severity, status, estimated_repair_cost, customer_liable, insurance_claim_filed, notes) VALUES
(4, 8, 'Small scratch on rear bumper', 'minor', 'resolved', 150.00, TRUE, FALSE, 'Customer accepted responsibility. Repair completed.');
