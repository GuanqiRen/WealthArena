"""Position model tracked in in-memory portfolio state."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    symbol: str
    quantity: int
    average_price: float
