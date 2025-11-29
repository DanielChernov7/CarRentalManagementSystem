export const APP_NAME = 'Car Rental Management System';
export const APP_VERSION = '1.0.0';

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api';

export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  DASHBOARD: '/dashboard',
  CARS: '/cars',
  CAR_DETAIL: '/cars/:id',
  RENTALS: '/rentals',
  RENTAL_DETAIL: '/rentals/:id',
  PROFILE: '/profile',
  ADMIN: '/admin',
  ADMIN_CARS: '/admin/cars',
  ADMIN_RENTALS: '/admin/rentals',
  ADMIN_USERS: '/admin/users',
} as const;

export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'access_token',
  REFRESH_TOKEN: 'refresh_token',
  USER: 'user',
} as const;

export const QUERY_KEYS = {
  CARS: 'cars',
  CAR: 'car',
  RENTALS: 'rentals',
  RENTAL: 'rental',
  USER: 'user',
  USERS: 'users',
} as const;
