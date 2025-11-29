import type { Car, ApiResponse, PaginatedResponse } from '../types';
import apiClient from './api';

export const carService = {
  // Get all cars
  getAllCars: async (params?: {
    page?: number;
    pageSize?: number;
    category?: string;
    status?: string;
  }): Promise<PaginatedResponse<Car>> => {
    const response = await apiClient.get<PaginatedResponse<Car>>('/cars', { params });
    return response.data;
  },

  // Get car by ID
  getCarById: async (id: string): Promise<ApiResponse<Car>> => {
    const response = await apiClient.get<ApiResponse<Car>>(`/cars/${id}`);
    return response.data;
  },

  // Create new car (admin only)
  createCar: async (carData: Omit<Car, 'id'>): Promise<ApiResponse<Car>> => {
    const response = await apiClient.post<ApiResponse<Car>>('/cars', carData);
    return response.data;
  },

  // Update car (admin only)
  updateCar: async (id: string, carData: Partial<Car>): Promise<ApiResponse<Car>> => {
    const response = await apiClient.put<ApiResponse<Car>>(`/cars/${id}`, carData);
    return response.data;
  },

  // Delete car (admin only)
  deleteCar: async (id: string): Promise<ApiResponse<void>> => {
    const response = await apiClient.delete<ApiResponse<void>>(`/cars/${id}`);
    return response.data;
  },
};
