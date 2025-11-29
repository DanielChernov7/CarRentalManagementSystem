import { create } from 'zustand';
import type { User } from '../types';
import { STORAGE_KEYS } from '../constants';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (user: User, token: string) => void;
  logout: () => void;
  updateUser: (user: User) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: JSON.parse(localStorage.getItem(STORAGE_KEYS.USER) || 'null'),
  token: localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN),
  isAuthenticated: !!localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN),

  login: (user, token) => {
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user));
    localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, token);
    set({ user, token, isAuthenticated: true });
  },

  logout: () => {
    localStorage.removeItem(STORAGE_KEYS.USER);
    localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN);
    set({ user: null, token: null, isAuthenticated: false });
  },

  updateUser: (user) => {
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user));
    set({ user });
  },
}));
