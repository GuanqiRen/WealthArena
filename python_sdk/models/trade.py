"""Trade model for trade history."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Trade:
    """Represents an executed trade."""

    trade_id: str
    symbol: str
    quantity: int
    execution_price: float
    timestamp_ms: int | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Trade":
        """Create Trade from API response dict."""
        return cls(
            trade_id=data.get("trade_id"),
            symbol=data.get("symbol"),
            quantity=data.get("quantity"),
            execution_price=data.get("execution_price"),
            timestamp_ms=data.get("timestamp_ms"),
        )


@dataclass
class TradeResponse:
    """Trade response wrapper."""

    trades: list[Trade]

    @classmethod
    def from_list(cls, data: list) -> "TradeResponse":
        """Create TradeResponse from API response list."""
        trades = [Trade.from_dict(t) for t in data]
        return cls(trades=trades)
