"use client";

import Link from "next/link";
import { useParams, useSearchParams } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import Navbar from "@/components/Navbar";
import PositionsTable from "@/components/PositionsTable";
import TradesTable from "@/components/TradesTable";
import { ApiError, getPositions, getTrades, type Position, type Trade } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import { useWebSocket } from "@/hooks/useWebSocket";

export default function PortfolioDetailPage() {
  const params = useParams<{ id: string }>();
  const searchParams = useSearchParams();
  const portfolioId = params?.id;
  const portfolioName = searchParams.get("name");
  const { token } = useAuth();

  const [positions, setPositions] = useState<Position[]>([]);
  const [trades, setTrades] = useState<Trade[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { livePositions, totalPnl, isConnected, error: wsError } = useWebSocket(portfolioId, token);

  useEffect(() => {
    async function load(): Promise<void> {
      if (!token || !portfolioId) {
        return;
      }

      setLoading(true);
      setError(null);

      try {
        const [positionsData, tradesData] = await Promise.all([
          getPositions(token, portfolioId),
          getTrades(token, portfolioId),
        ]);
        setPositions(positionsData);
        setTrades(tradesData);
      } catch (err) {
        if (err instanceof ApiError) {
          setError(err.message);
        } else {
          setError("Failed to load portfolio details.");
        }
      } finally {
        setLoading(false);
      }
    }

    load();
  }, [token, portfolioId]);

  const totalPositions = positions.length;
  const grossExposure = useMemo(
    () => positions.reduce((sum, p) => sum + p.quantity * p.average_price, 0),
    [positions],
  );
  const liveBySymbol = useMemo(
    () => Object.fromEntries(livePositions.map((p) => [p.symbol, p])),
    [livePositions],
  );

  return (
    <main className="page-shell stack">
      <Navbar />

      <section className="card" style={{ padding: 18 }}>
        <div style={{ display: "flex", justifyContent: "space-between", gap: 12, alignItems: "center" }}>
          <div>
            <h1 style={{ margin: "0 0 8px 0" }}>Portfolio Details</h1>
            {portfolioName ? <p style={{ margin: "0 0 4px 0", color: "var(--text)" }}>Portfolio Name: {portfolioName}</p> : null}
            <p style={{ margin: 0, color: "var(--muted)" }}>Portfolio ID: {portfolioId}</p>
          </div>
          <Link href="/dashboard" className="btn btn-secondary">Back to Dashboard</Link>
        </div>
      </section>

      <section className="card" style={{ padding: 16 }}>
        <h2 style={{ marginTop: 0 }}>Portfolio Summary</h2>
        <p style={{ marginTop: 0, color: isConnected ? "#1f7a1f" : "var(--muted)" }}>
          Realtime: {isConnected ? "Connected" : "Reconnecting..."}
        </p>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 10 }}>
          <div className="card" style={{ padding: 12 }}>
            <div style={{ color: "var(--muted)", fontSize: "0.9rem" }}>Total Positions</div>
            <div style={{ fontSize: "1.5rem", fontWeight: 700 }}>{totalPositions}</div>
          </div>
          <div className="card" style={{ padding: 12 }}>
            <div style={{ color: "var(--muted)", fontSize: "0.9rem" }}>Gross Exposure</div>
            <div style={{ fontSize: "1.5rem", fontWeight: 700 }}>${grossExposure.toFixed(2)}</div>
          </div>
          <div className="card" style={{ padding: 12 }}>
            <div style={{ color: "var(--muted)", fontSize: "0.9rem" }}>Live Total PnL</div>
            <div style={{ fontSize: "1.5rem", fontWeight: 700, color: totalPnl >= 0 ? "#1f7a1f" : "#b42318" }}>
              {totalPnl >= 0 ? "+" : ""}${totalPnl.toFixed(2)}
            </div>
          </div>
        </div>
      </section>

      {loading ? <div className="card" style={{ padding: 16 }}>Loading portfolio data...</div> : null}
      {error ? <div className="card error" style={{ padding: 16 }}>{error}</div> : null}
      {wsError ? <div className="card error" style={{ padding: 16 }}>{wsError}</div> : null}

      {!loading && !error ? (
        <>
          <PositionsTable positions={positions} liveBySymbol={liveBySymbol} />
          <TradesTable trades={trades} />
        </>
      ) : null}
    </main>
  );
}
