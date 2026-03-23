"use client";

import { useEffect } from "react";
import { usePathname, useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";

type AuthGuardProps = {
  children: React.ReactNode;
};

export default function AuthGuard({ children }: AuthGuardProps) {
  const { isAuthenticated, isLoading } = useAuth();
  const pathname = usePathname();
  const router = useRouter();

  const isLoginRoute = pathname === "/login";

  useEffect(() => {
    if (isLoading) {
      return;
    }

    if (!isAuthenticated && !isLoginRoute) {
      router.replace("/login");
    }

    if (isAuthenticated && isLoginRoute) {
      router.replace("/dashboard");
    }
  }, [isAuthenticated, isLoading, isLoginRoute, router]);

  if (isLoading) {
    return <div className="page-shell">Loading session...</div>;
  }

  if (!isAuthenticated && !isLoginRoute) {
    return <div className="page-shell">Redirecting to login...</div>;
  }

  return <>{children}</>;
}
