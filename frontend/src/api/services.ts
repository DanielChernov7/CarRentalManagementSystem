import api from './axios';
import type {
  User,
  Location,
  Vehicle,
  RatePlan,
  Reservation,
  Payment,
  PriceCalculation,
  CreateReservationData,
  LoginCredentials,
  RegisterData,
  AuthResponse,
} from '@/types';

// Auth API
export const authAPI = {
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    const response = await api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    return response.data;
  },

  register: async (data: RegisterData): Promise<User> => {
    const response = await api.post('/auth/register/customer', data);
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

// Locations API
export const locationsAPI = {
  getAll: async (): Promise<Location[]> => {
    const response = await api.get('/locations/');
    return response.data;
  },

  getById: async (id: number): Promise<Location> => {
    const response = await api.get(`/locations/${id}`);
    return response.data;
  },

  create: async (data: Partial<Location>): Promise<Location> => {
    const response = await api.post('/locations/', data);
    return response.data;
  },

  update: async (id: number, data: Partial<Location>): Promise<Location> => {
    const response = await api.put(`/locations/${id}`, data);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/locations/${id}`);
  },
};

// Vehicles API
export const vehiclesAPI = {
  getAll: async (params?: {
    status?: string;
    vehicle_type?: string;
    location_id?: number;
  }): Promise<Vehicle[]> => {
    const response = await api.get('/vehicles/', { params });
    return response.data;
  },

  getAvailable: async (params: {
    start_date: string;
    end_date: string;
    location_id?: number;
    vehicle_type?: string;
  }): Promise<Vehicle[]> => {
    const response = await api.get('/vehicles/available', { params });
    return response.data;
  },

  getById: async (id: number): Promise<Vehicle> => {
    const response = await api.get(`/vehicles/${id}`);
    return response.data;
  },

  create: async (data: Partial<Vehicle>): Promise<Vehicle> => {
    const response = await api.post('/vehicles/', data);
    return response.data;
  },

  update: async (id: number, data: Partial<Vehicle>): Promise<Vehicle> => {
    const response = await api.put(`/vehicles/${id}`, data);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/vehicles/${id}`);
  },
};

// Rate Plans API
export const ratePlansAPI = {
  getAll: async (): Promise<RatePlan[]> => {
    const response = await api.get('/rate-plans/');
    return response.data;
  },

  getById: async (id: number): Promise<RatePlan> => {
    const response = await api.get(`/rate-plans/${id}`);
    return response.data;
  },

  create: async (data: Partial<RatePlan>): Promise<RatePlan> => {
    const response = await api.post('/rate-plans/', data);
    return response.data;
  },

  update: async (id: number, data: Partial<RatePlan>): Promise<RatePlan> => {
    const response = await api.put(`/rate-plans/${id}`, data);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/rate-plans/${id}`);
  },
};

// Reservations API
export const reservationsAPI = {
  getAll: async (): Promise<Reservation[]> => {
    const response = await api.get('/reservations/');
    return response.data;
  },

  getMy: async (): Promise<Reservation[]> => {
    const response = await api.get('/reservations/my-reservations');
    return response.data;
  },

  getById: async (id: number): Promise<Reservation> => {
    const response = await api.get(`/reservations/${id}`);
    return response.data;
  },

  calculatePrice: async (data: {
    vehicle_id: number;
    rate_plan_id: number;
    pickup_location_id: number;
    dropoff_location_id: number;
    start_date: string;
    end_date: string;
    include_insurance: boolean;
  }): Promise<PriceCalculation> => {
    const response = await api.post('/reservations/calculate-price', data);
    return response.data;
  },

  create: async (data: CreateReservationData): Promise<Reservation> => {
    const response = await api.post('/reservations/', data);
    return response.data;
  },

  update: async (id: number, data: Partial<Reservation>): Promise<Reservation> => {
    const response = await api.put(`/reservations/${id}`, data);
    return response.data;
  },

  activate: async (id: number): Promise<void> => {
    await api.post(`/reservations/${id}/activate`);
  },

  complete: async (id: number): Promise<void> => {
    await api.post(`/reservations/${id}/complete`);
  },

  cancel: async (id: number): Promise<void> => {
    await api.post(`/reservations/${id}/cancel`);
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/reservations/${id}`);
  },
};

// Payments API
export const paymentsAPI = {
  getAll: async (): Promise<Payment[]> => {
    const response = await api.get('/payments/');
    return response.data;
  },

  getById: async (id: number): Promise<Payment> => {
    const response = await api.get(`/payments/${id}`);
    return response.data;
  },

  getByReservation: async (reservationId: number): Promise<Payment[]> => {
    const response = await api.get(`/payments/reservation/${reservationId}`);
    return response.data;
  },

  create: async (data: {
    reservation_id: number;
    amount: number;
    payment_method: string;
    payment_details?: string;
  }): Promise<Payment> => {
    const response = await api.post('/payments/', data);
    return response.data;
  },

  refund: async (id: number): Promise<void> => {
    await api.post(`/payments/${id}/refund`);
  },
};
