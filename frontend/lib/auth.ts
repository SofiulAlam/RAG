import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
  token: string | null;
  refreshToken: string | null;
  user: User | null;
  setAuth: (token: string, refreshToken: string, user: User) => void;
  clearAuth: () => void;
}

interface User {
  id: string;
  email: string;
  name?: string;
  system_prompt?: string;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      refreshToken: null,
      user: null,
      setAuth: (token, refreshToken, user) => set({ token, refreshToken, user }),
      clearAuth: () => set({ token: null, refreshToken: null, user: null }),
    }),
    {
      name: 'auth-storage',
    }
  )
);

export async function login(email: string, password: string) {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Login failed');
  }

  const data = await response.json();

  // Fetch user info
  const userResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/me`, {
    headers: { Authorization: `Bearer ${data.access_token}` },
  });

  if (!userResponse.ok) {
    throw new Error('Failed to fetch user info');
  }

  const user = await userResponse.json();

  return { ...data, user };
}

export async function signup(email: string, password: string, name?: string) {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, name }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Signup failed');
  }

  const data = await response.json();

  // Fetch user info
  const userResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/me`, {
    headers: { Authorization: `Bearer ${data.access_token}` },
  });

  if (!userResponse.ok) {
    throw new Error('Failed to fetch user info');
  }

  const user = await userResponse.json();

  return { ...data, user };
}

export async function refreshAccessToken(refreshToken: string) {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/refresh`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token: refreshToken }),
  });

  if (!response.ok) {
    throw new Error('Token refresh failed');
  }

  return response.json();
}

export function getAuthHeader() {
  const { token } = useAuthStore.getState();
  return token ? { Authorization: `Bearer ${token}` } : {};
}
