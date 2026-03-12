"""Trade model for executed fills."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Trade:
    trade_id: str
    symbol: str
    quantity: int
    execution_price: float
    timestamp_ms: int
