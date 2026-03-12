"""Repository for order persistence."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from backend.db.supabase_client import SupabaseRestClient, get_supabase_client
from trading_engine.models.order import Order


class OrderRepository:
    def __init__(self, client: SupabaseRestClient | None = None) -> None:
        self._client = client or get_supabase_client()

    def save_order(self, portfolio_id: str, order: Order) -> dict[str, Any]:
        payload = {
            "id": order.order_id,
            "portfolio_id": portfolio_id,
            "symbol": order.symbol,
            "quantity": order.quantity,
            "side": order.side,
            "status": order.status,
            "created_at": datetime.fromtimestamp(order.timestamp_ms / 1000, tz=timezone.utc).isoformat(),
        }
        return self._client.insert("orders", payload)

    def get_orders(self, portfolio_id: str) -> list[dict[str, Any]]:
        return self._client.select(
            "orders",
            filters={"portfolio_id": f"eq.{portfolio_id}", "order": "created_at.asc"},
        )
