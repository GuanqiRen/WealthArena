import type { Portfolio } from "@/lib/api";
import PortfolioCard from "@/components/PortfolioCard";

type PortfolioListProps = {
  portfolios: Portfolio[];
};

export default function PortfolioList({ portfolios }: PortfolioListProps) {
  if (portfolios.length === 0) {
    return (
      <div className="card" style={{ padding: 16 }}>
        No portfolios found for this user.
      </div>
    );
  }

  return (
    <section className="stack">
      {portfolios.map((portfolio) => (
        <PortfolioCard key={portfolio.id} portfolio={portfolio} />
      ))}
    </section>
  );
}
