"""Service for trading operations with persistence."""

from __future__ import annotations

from typing import Any

from trading_engine.engine.trading_engine import TradingEngine
from backend.repositories.order_repository import OrderRepository
from backend.repositories.position_repository import PositionRepository
from backend.repositories.trade_repository import TradeRepository


class TradingServiceError(Exception):
    """Raised when a trading operation fails."""


class TradingService:
    """Orchestrates trading engine with database persistence.

    For each order:
    1. Call trading engine to execute order -> trade
    2. Persist order
    3. Persist trade
    4. Persist/update position
    """

    def __init__(
        self,
        order_repo: OrderRepository | None = None,
        trade_repo: TradeRepository | None = None,
        position_repo: PositionRepository | None = None,
    ) -> None:
        self._order_repo = order_repo or OrderRepository()
        self._trade_repo = trade_repo or TradeRepository()
        self._position_repo = position_repo or PositionRepository()

    def place_order(
        self,
        portfolio_id: str,
        symbol: str,
        quantity: int,
        side: str,
    ) -> dict[str, Any]:
        """Place a market order and persist it with resulting trade and position.

        Args:
            portfolio_id: Portfolio UUID
            symbol: Ticker symbol (e.g. "AAPL")
            quantity: Number of shares
            side: "buy" or "sell"

        Returns:
            dict with keys: order, trade, position

        Raises:
            TradingServiceError: if order placement or persistence fails
        """
        try:
            engine = TradingEngine(portfolio_id=portfolio_id)

            # Place order and get results
            order = engine.place_order(symbol, quantity, side)

            # Order is now either filled or rejected
            if order.status != "filled":
                # Still persist the rejected/pending order
                self._order_repo.save_order(portfolio_id, order)
                return {
                    "order": order,
                    "trade": None,
                    "position": None,
                    "status": order.status,
                }

            # Order was filled — persist trade and position
            trades = engine.get_trade_history()
            positions = engine.get_positions()

            if not trades:
                raise TradingServiceError("Order filled but no trades recorded")

            latest_trade = trades[-1]
            self._trade_repo.save_trade(portfolio_id, latest_trade)
            self._order_repo.save_order(portfolio_id, order)

            # Update position for the symbol
            for pos in positions:
                if pos.symbol == symbol:
                    self._position_repo.update_position(portfolio_id, pos)
                    break

            return {
                "order": order,
                "trade": latest_trade,
                "position": [p for p in positions if p.symbol == symbol][0] if positions else None,
                "status": "filled",
            }

        except Exception as exc:
            raise TradingServiceError(f"Failed to place order: {exc}") from exc

    def get_positions(self, portfolio_id: str) -> list[dict[str, Any]]:
        """Get all positions for a portfolio."""
        return self._position_repo.get_positions(portfolio_id)

    def get_trade_history(self, portfolio_id: str) -> list[dict[str, Any]]:
        """Get all trades for a portfolio."""
        return self._trade_repo.get_trades(portfolio_id)

    def get_orders(self, portfolio_id: str) -> list[dict[str, Any]]:
        """Get all orders for a portfolio."""
        return self._order_repo.get_orders(portfolio_id)
