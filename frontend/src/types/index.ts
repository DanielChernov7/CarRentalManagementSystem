export type UserRole = 'customer' | 'admin' | 'clerk';

export type VehicleStatus = 'available' | 'reserved' | 'rented' | 'maintenance' | 'out_of_service';

export type VehicleType = 'sedan' | 'suv' | 'truck' | 'van' | 'luxury' | 'economy';

export type ReservationStatus = 'pending' | 'confirmed' | 'active' | 'completed' | 'cancelled';

export type PaymentMethod = 'credit_card' | 'debit_card' | 'cash' | 'paypal';

export type PaymentStatus = 'pending' | 'processing' | 'completed' | 'failed' | 'refunded';

export interface User {
  id: number;
  email: string;
  full_name: string;
  phone?: string;
  role: UserRole;
  created_at: string;
  updated_at: string;
}

export interface Location {
  id: number;
  name: string;
  address: string;
  city: string;
  state: string;
  zip_code: string;
  phone: string;
  email?: string;
  created_at: string;
  updated_at: string;
}

export interface Vehicle {
  id: number;
  make: string;
  model: string;
  year: number;
  license_plate: string;
  vin: string;
  color?: string;
  vehicle_type: VehicleType;
  status: VehicleStatus;
  mileage: number;
  daily_rate: number;
  base_location_id: number;
  created_at: string;
  updated_at: string;
}

export interface RatePlan {
  id: number;
  name: string;
  description?: string;
  discount_percentage: number;
  one_way_fee: number;
  insurance_daily_rate: number;
  min_days: number;
  max_days?: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Reservation {
  id: number;
  customer_id: number;
  vehicle_id: number;
  rate_plan_id: number;
  pickup_location_id: number;
  dropoff_location_id: number;
  start_date: string;
  end_date: string;
  base_price: number;
  discount_amount: number;
  one_way_fee_amount: number;
  insurance_amount: number;
  total_price: number;
  status: ReservationStatus;
  include_insurance: boolean;
  special_requests?: string;
  created_at: string;
  updated_at: string;
  confirmed_at?: string;
  cancelled_at?: string;
}

export interface Payment {
  id: number;
  reservation_id: number;
  amount: number;
  payment_method: PaymentMethod;
  status: PaymentStatus;
  transaction_id?: string;
  processed_at?: string;
  created_at: string;
  updated_at: string;
}

export interface PriceCalculation {
  base_price: number;
  discount_amount: number;
  one_way_fee_amount: number;
  insurance_amount: number;
  total_price: number;
  rental_days: number;
}

export interface CreateReservationData {
  customer_id?: number;
  vehicle_id: number;
  rate_plan_id: number;
  pickup_location_id: number;
  dropoff_location_id: number;
  start_date: string;
  end_date: string;
  include_insurance: boolean;
  special_requests?: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  full_name: string;
  phone?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}
