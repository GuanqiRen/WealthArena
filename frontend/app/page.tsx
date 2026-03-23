"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";

export default function HomePage() {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (isLoading) {
      return;
    }
    router.replace(isAuthenticated ? "/dashboard" : "/login");
  }, [isAuthenticated, isLoading, router]);

  return <main className="page-shell">Loading...</main>;
}
