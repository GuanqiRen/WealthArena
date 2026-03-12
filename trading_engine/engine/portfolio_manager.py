"""In-memory portfolio state and position update logic."""

from __future__ import annotations

from trading_engine.models.position import Position


class PortfolioManager:
    """Maintains in-memory positions and average price calculations."""

    def __init__(self) -> None:
        self._positions: dict[str, Position] = {}

    def load_positions(self, positions: list[Position]) -> None:
        self._positions = {position.symbol: position for position in positions}

    def get_position_quantity(self, symbol: str) -> int:
        normalized = symbol.strip().upper()
        position = self._positions.get(normalized)
        return position.quantity if position else 0

    def apply_fill(self, symbol: str, quantity: int, side: str, execution_price: float) -> Position | None:
        normalized = symbol.strip().upper()
        delta = quantity if side == "buy" else -quantity

        existing = self._positions.get(normalized, Position(symbol=normalized, quantity=0, average_price=0.0))
        updated = self._apply_delta(existing, delta, execution_price)

        if updated.quantity == 0:
            self._positions.pop(normalized, None)
            return None

        self._positions[normalized] = updated
        return updated

    def get_positions(self) -> list[Position]:
        return [self._positions[symbol] for symbol in sorted(self._positions)]

    def _apply_delta(self, current: Position, delta: int, price: float) -> Position:
        current_qty = current.quantity
        current_avg = current.average_price

        if current_qty == 0:
            return Position(symbol=current.symbol, quantity=delta, average_price=float(price))

        same_direction = (current_qty > 0 and delta > 0) or (current_qty < 0 and delta < 0)
        if same_direction:
            new_qty = current_qty + delta
            weighted_total = (abs(current_qty) * current_avg) + (abs(delta) * float(price))
            new_avg = weighted_total / abs(new_qty)
            return Position(symbol=current.symbol, quantity=new_qty, average_price=new_avg)

        new_qty = current_qty + delta
        if new_qty == 0:
            return Position(symbol=current.symbol, quantity=0, average_price=0.0)

        # Reduced but still same side; average entry remains unchanged.
        if abs(current_qty) > abs(delta):
            return Position(symbol=current.symbol, quantity=new_qty, average_price=current_avg)

        # Position flipped to opposite side; remaining quantity opens at latest execution price.
        return Position(symbol=current.symbol, quantity=new_qty, average_price=float(price))
