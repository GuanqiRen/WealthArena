"""Order model for market-order simulation."""

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class Order:
    order_id: str
    symbol: str
    quantity: int
    side: Literal["buy", "sell"]
    timestamp_ms: int
    status: Literal["pending", "filled", "rejected"]
    message: str = ""
