"use client";

import { create } from "zustand";

interface AuthState {
  user: any | null;
  tenants: any[];
  currentTenant: any | null;

  setAuth: (user: any, tenants: any[]) => void;
  setCurrentTenant: (tenant: any) => void;
}

export const useAuthStore = create<AuthState>()((set) => ({
  user: null,
  tenants: [],
  currentTenant: null,

  setAuth: (user, tenants) => set({ user, tenants }),

  setCurrentTenant: (tenant) => set({ currentTenant: tenant }),
}));
