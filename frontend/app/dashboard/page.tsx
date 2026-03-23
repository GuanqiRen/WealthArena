"use client";

import { useEffect, useState } from "react";
import Navbar from "@/components/Navbar";
import PortfolioList from "@/components/PortfolioList";
import { ApiError, getPortfolios, type Portfolio } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";

export default function DashboardPage() {
  const { token } = useAuth();

  const [portfolios, setPortfolios] = useState<Portfolio[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load(): Promise<void> {
      if (!token) {
        return;
      }

      setLoading(true);
      setError(null);

      try {
        const data = await getPortfolios(token);
        setPortfolios(data);
      } catch (err) {
        if (err instanceof ApiError) {
          setError(err.message);
        } else {
          setError("Failed to load portfolios.");
        }
      } finally {
        setLoading(false);
      }
    }

    load();
  }, [token]);

  return (
    <main className="page-shell stack">
      <Navbar />

      <section className="card" style={{ padding: 18 }}>
        <h1 style={{ marginTop: 0, marginBottom: 8 }}>Dashboard</h1>
        <p style={{ margin: 0, color: "var(--muted)" }}>Read-only view of your portfolios.</p>
      </section>

      {loading ? <div className="card" style={{ padding: 16 }}>Loading portfolios...</div> : null}
      {error ? <div className="card error" style={{ padding: 16 }}>{error}</div> : null}
      {!loading && !error ? <PortfolioList portfolios={portfolios} /> : null}
    </main>
  );
}
