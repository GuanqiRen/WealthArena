import type { Position } from "@/lib/api";

type PositionsTableProps = {
  positions: Position[];
};

export default function PositionsTable({ positions }: PositionsTableProps) {
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
            </tr>
          </thead>
          <tbody>
            {positions.map((position) => (
              <tr key={position.symbol}>
                <td>{position.symbol}</td>
                <td>{position.quantity}</td>
                <td>${position.average_price.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}
