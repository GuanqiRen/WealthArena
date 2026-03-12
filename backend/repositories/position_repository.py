"""Repository for position persistence."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from backend.db.supabase_client import SupabaseRestClient, get_supabase_client
from trading_engine.models.position import Position


class PositionRepository:
    def __init__(self, client: SupabaseRestClient | None = None) -> None:
        self._client = client or get_supabase_client()

    def update_position(self, portfolio_id: str, position: Position) -> dict[str, Any]:
        payload = {
            "portfolio_id": portfolio_id,
            "symbol": position.symbol,
            "quantity": position.quantity,
            "average_price": position.average_price,
            "updated_at": datetime.now(tz=timezone.utc).isoformat(),
        }
        return self._client.upsert("positions", payload, on_conflict="portfolio_id,symbol")

    def delete_position(self, portfolio_id: str, symbol: str) -> None:
        self._client.delete(
            "positions",
            filters={"portfolio_id": f"eq.{portfolio_id}", "symbol": f"eq.{symbol}"},
        )

    def get_positions(self, portfolio_id: str) -> list[dict[str, Any]]:
        return self._client.select(
            "positions",
            filters={"portfolio_id": f"eq.{portfolio_id}", "order": "symbol.asc"},
        )
