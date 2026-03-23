import type { Position } from "@/lib/api";
import type { LivePosition } from "@/hooks/useWebSocket";

type PositionsTableProps = {
  positions: Position[];
  liveBySymbol?: Record<string, LivePosition>;
};

function formatPnl(pnl: number) {
  const color = pnl >= 0 ? "#1f7a1f" : "#b42318";
  const sign = pnl >= 0 ? "+" : "";
  return <span style={{ color }}>{sign}${pnl.toFixed(2)}</span>;
}

export default function PositionsTable({ positions, liveBySymbol = {} }: PositionsTableProps) {
  return (
    <section className="card" style={{ padding: 16 }}>
      <h2 style={{ marginTop: 0 }}>Positions</h2>
      {positions.length === 0 ? (
        <p style={{ color: "var(--muted)" }}>No positions yet.</p>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Quantity</th>
              <th>Average Price</th>
              <th>Live Price</th>
              <th>Unrealized PnL</th>
            </tr>
          </thead>
          <tbody>
            {positions.map((position) => {
              const live = liveBySymbol[position.symbol];

              return (
                <tr key={position.symbol}>
                  <td>{position.symbol}</td>
                  <td>{position.quantity}</td>
                  <td>${position.average_price.toFixed(2)}</td>
                  <td>{live ? `$${live.price.toFixed(2)}` : "-"}</td>
                  <td>{live ? formatPnl(live.pnl) : "-"}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      )}
    </section>
  );
}
