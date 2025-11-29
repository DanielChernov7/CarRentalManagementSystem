// User types
export interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'customer';
  phone?: string;
  createdAt: Date;
}

// Car types
export interface Car {
  id: string;
  brand: string;
  model: string;
  year: number;
  color: string;
  licensePlate: string;
  pricePerDay: number;
  category: CarCategory;
  status: CarStatus;
  features: string[];
  imageUrl?: string;
  mileage: number;
  fuelType: 'gasoline' | 'diesel' | 'electric' | 'hybrid';
}

export const CarCategory = {
  ECONOMY: 'economy',
  COMPACT: 'compact',
  MIDSIZE: 'midsize',
  FULLSIZE: 'fullsize',
  SUV: 'suv',
  LUXURY: 'luxury',
  VAN: 'van',
} as const;

export type CarCategory = (typeof CarCategory)[keyof typeof CarCategory];

export const CarStatus = {
  AVAILABLE: 'available',
  RENTED: 'rented',
  MAINTENANCE: 'maintenance',
  RESERVED: 'reserved',
} as const;

export type CarStatus = (typeof CarStatus)[keyof typeof CarStatus];

// Rental types
export interface Rental {
  id: string;
  carId: string;
  userId: string;
  startDate: Date;
  endDate: Date;
  totalCost: number;
  status: RentalStatus;
  pickupLocation: string;
  returnLocation: string;
  insurance: boolean;
  additionalDrivers?: number;
}

export const RentalStatus = {
  PENDING: 'pending',
  CONFIRMED: 'confirmed',
  ACTIVE: 'active',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled',
} as const;

export type RentalStatus = (typeof RentalStatus)[keyof typeof RentalStatus];

// Payment types
export interface Payment {
  id: string;
  rentalId: string;
  amount: number;
  method: PaymentMethod;
  status: PaymentStatus;
  transactionDate: Date;
}

export const PaymentMethod = {
  CREDIT_CARD: 'credit_card',
  DEBIT_CARD: 'debit_card',
  CASH: 'cash',
  BANK_TRANSFER: 'bank_transfer',
} as const;

export type PaymentMethod = (typeof PaymentMethod)[keyof typeof PaymentMethod];

export const PaymentStatus = {
  PENDING: 'pending',
  COMPLETED: 'completed',
  FAILED: 'failed',
  REFUNDED: 'refunded',
} as const;

export type PaymentStatus = (typeof PaymentStatus)[keyof typeof PaymentStatus];

// API Response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}
