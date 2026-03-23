import type { Trade } from "@/lib/api";

type TradesTableProps = {
  trades: Trade[];
};

function formatTimestamp(timestampMs?: number): string {
  if (!timestampMs) {
    return "N/A";
  }
  return new Date(timestampMs).toLocaleString();
}

export default function TradesTable({ trades }: TradesTableProps) {
  return (
    <section className="card" style={{ padding: 16 }}>
      <h2 style={{ marginTop: 0 }}>Trade History</h2>
      {trades.length === 0 ? (
        <p style={{ color: "var(--muted)" }}>No trades yet.</p>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Quantity</th>
              <th>Execution Price</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {trades.map((trade) => (
              <tr key={trade.trade_id}>
                <td>{trade.symbol}</td>
                <td>{trade.quantity}</td>
                <td>${trade.execution_price.toFixed(2)}</td>
                <td>{formatTimestamp(trade.timestamp_ms)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}
