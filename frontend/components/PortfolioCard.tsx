import Link from "next/link";
import type { Portfolio } from "@/lib/api";

type PortfolioCardProps = {
  portfolio: Portfolio;
};

export default function PortfolioCard({ portfolio }: PortfolioCardProps) {
  return (
    <Link href={`/portfolio/${portfolio.id}`} className="card" style={{ padding: 16, display: "block" }}>
      <div style={{ display: "flex", justifyContent: "space-between", gap: 16 }}>
        <div>
          <h3 style={{ margin: "0 0 8px 0" }}>{portfolio.name}</h3>
          <div style={{ color: "var(--muted)", fontSize: "0.92rem" }}>ID: {portfolio.id}</div>
        </div>
        <div style={{ color: "var(--accent)", fontWeight: 600, alignSelf: "center" }}>
          View Details
        </div>
      </div>
    </Link>
  );
}
