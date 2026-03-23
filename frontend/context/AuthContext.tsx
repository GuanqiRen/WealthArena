"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { clearStoredToken, getStoredToken, storeToken } from "@/lib/auth";
import { login as apiLogin } from "@/lib/api";

type AuthContextValue = {
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextValue | null>(null);

type AuthProviderProps = {
  children: ReactNode;
};

export function AuthProvider({ children }: AuthProviderProps) {
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const existing = getStoredToken();
    setToken(existing);
    setIsLoading(false);
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const response = await apiLogin(email, password);
    storeToken(response.access_token);
    setToken(response.access_token);
  }, []);

  const logout = useCallback(() => {
    clearStoredToken();
    setToken(null);
  }, []);

  const value = useMemo(
    () => ({
      token,
      isAuthenticated: Boolean(token),
      isLoading,
      login,
      logout,
    }),
    [token, isLoading, login, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}
