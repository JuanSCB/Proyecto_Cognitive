import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from 'react';
import type { AuthUser, LoginResponse } from '../services/authService';
import { login as loginApi } from '../services/authService';

type AuthContextType = {
  user: AuthUser | null;
  token: string | null;
  login: (correo: string, contraseña: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const AUTH_STORAGE_KEY = 'iluminacion-auth';

const parseStoredAuth = (): { token: string; user: AuthUser } | null => {
  if (typeof window === 'undefined') return null;
  const stored = localStorage.getItem(AUTH_STORAGE_KEY);
  if (!stored) return null;

  try {
    return JSON.parse(stored) as { token: string; user: AuthUser };
  } catch {
    return null;
  }
};

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [auth, setAuth] = useState<{ token: string | null; user: AuthUser | null }>(() => {
    const stored = parseStoredAuth();
    return stored ? { token: stored.token, user: stored.user } : { token: null, user: null };
  });

  const { token, user } = auth;

  useEffect(() => {
    if (typeof window === 'undefined') return;

    const stored = parseStoredAuth();
    if (!stored || !stored.token || !stored.user) {
      setAuth({ token: null, user: null });
    }
  }, []);

  useEffect(() => {
    if (token && user) {
      localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify({ token, user }));
    } else {
      localStorage.removeItem(AUTH_STORAGE_KEY);
    }
  }, [token, user]);

  const login = async (correo: string, contraseña: string) => {
    const response: LoginResponse = await loginApi({ correo, contraseña });
    setAuth({ token: response.token, user: response.usuario });
  };

  const logout = () => {
    setAuth({ token: null, user: null });
  };

  const value = useMemo(
    () => ({
      user,
      token,
      login,
      logout,
      isAuthenticated: Boolean(token && user)
    }),
    [token, user]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
