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
import {
  getSupabaseAccessToken,
  signInWithGoogle,
  signOutSupabase,
  subscribeToSupabaseAuthChanges,
} from "@/lib/supabase_auth";

type AuthContextValue = {
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  loginWithGoogle: () => Promise<void>;
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
    let isMounted = true;

    const initializeAuth = async () => {
      const existing = getStoredToken();
      if (existing) {
        if (isMounted) {
          setToken(existing);
          setIsLoading(false);
        }
        return;
      }

      const supabaseToken = await getSupabaseAccessToken();
      if (supabaseToken) {
        storeToken(supabaseToken);
      }

      if (isMounted) {
        setToken(supabaseToken);
        setIsLoading(false);
      }
    };

    void initializeAuth();

    const unsubscribe = subscribeToSupabaseAuthChanges((session) => {
      const nextToken = session?.access_token ?? null;

      if (nextToken) {
        storeToken(nextToken);
      } else {
        clearStoredToken();
      }

      setToken(nextToken);
      setIsLoading(false);
    });

    return () => {
      isMounted = false;
      unsubscribe?.();
    };
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const response = await apiLogin(email, password);
    storeToken(response.access_token);
    setToken(response.access_token);
  }, []);

  const loginWithGoogle = useCallback(async () => {
    await signInWithGoogle();
  }, []);

  const logout = useCallback(() => {
    clearStoredToken();
    setToken(null);
    void signOutSupabase();
  }, []);

  const value = useMemo(
    () => ({
      token,
      isAuthenticated: Boolean(token),
      isLoading,
      login,
      loginWithGoogle,
      logout,
    }),
    [token, isLoading, login, loginWithGoogle, logout],
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
