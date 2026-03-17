"""Order model for trading operations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Order:
    """Represents a trading order."""

    order_id: str
    symbol: str
    quantity: int
    side: str  # "buy" or "sell"
    status: str
    timestamp_ms: int | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Order":
        """Create Order from API response dict."""
        return cls(
            order_id=data.get("order_id"),
            symbol=data.get("symbol"),
            quantity=data.get("quantity"),
            side=data.get("side"),
            status=data.get("status"),
            timestamp_ms=data.get("timestamp_ms"),
        )


@dataclass
class OrderResponse:
    """Order response including related data."""

    order: Order
    status: str
    trade: dict | None = None
    position: dict | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "OrderResponse":
        """Create OrderResponse from API response dict."""
        order_data = data.get("order", {})
        return cls(
            order=Order.from_dict(order_data),
            status=data.get("status"),
            trade=data.get("trade"),
            position=data.get("position"),
        )
