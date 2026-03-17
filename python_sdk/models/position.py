"""Position model for portfolio positions."""

from dataclasses import dataclass


@dataclass
class Position:
    """Represents a position in a portfolio."""

    symbol: str
    quantity: int
    average_price: float

    @classmethod
    def from_dict(cls, data: dict) -> "Position":
        """Create Position from API response dict."""
        return cls(
            symbol=data.get("symbol"),
            quantity=data.get("quantity"),
            average_price=data.get("average_price"),
        )


@dataclass
class PositionResponse:
    """Position response wrapper."""

    positions: list[Position]

    @classmethod
    def from_list(cls, data: list) -> "PositionResponse":
        """Create PositionResponse from API response list."""
        positions = [Position.from_dict(p) for p in data]
        return cls(positions=positions)
