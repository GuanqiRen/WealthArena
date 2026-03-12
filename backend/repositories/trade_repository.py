"""Repository for trade persistence."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from backend.db.supabase_client import SupabaseRestClient, get_supabase_client
from trading_engine.models.trade import Trade


class TradeRepository:
    def __init__(self, client: SupabaseRestClient | None = None) -> None:
        self._client = client or get_supabase_client()

    def save_trade(self, portfolio_id: str, trade: Trade) -> dict[str, Any]:
        payload = {
            "id": trade.trade_id,
            "portfolio_id": portfolio_id,
            "symbol": trade.symbol,
            "quantity": trade.quantity,
            "execution_price": trade.execution_price,
            "timestamp": datetime.fromtimestamp(trade.timestamp_ms / 1000, tz=timezone.utc).isoformat(),
        }
        return self._client.insert("trades", payload)

    def get_trades(self, portfolio_id: str) -> list[dict[str, Any]]:
        return self._client.select(
            "trades",
            filters={"portfolio_id": f"eq.{portfolio_id}", "order": "timestamp.asc"},
        )
