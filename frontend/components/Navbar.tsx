"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";

export default function Navbar() {
  const { logout } = useAuth();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.replace("/login");
  };

  return (
    <nav
      className="card"
      style={{
        padding: "14px 16px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
      }}
    >
      <div style={{ display: "flex", gap: 16, alignItems: "center" }}>
        <strong>WealthArena</strong>
        <Link href="/dashboard">Dashboard</Link>
      </div>
      <button type="button" className="btn btn-secondary" onClick={handleLogout}>
        Logout
      </button>
    </nav>
  );
}
