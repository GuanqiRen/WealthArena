"""Trading endpoint service."""

from __future__ import annotations

from typing import Any, Dict
from python_sdk.utils.http_client import HTTPClient, HTTPError
from python_sdk.models import Order, Position, Trade


class TradingError(Exception):
    """Exception raised for trading operations."""

    pass


class TradingService:
    """Service for trading operations."""

    def __init__(self, http_client: HTTPClient):
        """Initialize TradingService.

        Args:
            http_client: HTTPClient instance for making requests.
        """
        self.http_client = http_client

    def place_order(
        self,
        portfolio_id: str,
        symbol: str,
        quantity: int,
        side: str,
    ) -> Dict[str, Any]:
        """Place a market order.

        Args:
            portfolio_id: Portfolio ID.
            symbol: Stock symbol (e.g., "AAPL").
            quantity: Number of shares.
            side: "buy" or "sell".

        Returns:
            Order execution response with order, trade, and position data.

        Raises:
            TradingError: If order placement fails.
        """
        if side not in ("buy", "sell"):
            raise TradingError(f"Invalid side: {side}. Must be 'buy' or 'sell'.")
        if quantity <= 0:
            raise TradingError(f"Invalid quantity: {quantity}. Must be positive.")

        try:
            request_data = {
                "portfolio_id": portfolio_id,
                "symbol": symbol,
                "quantity": quantity,
                "side": side,
            }
            response = self.http_client.post("/trading/orders", request_data)
            return response
        except HTTPError as e:
            raise TradingError(f"Failed to place order: {e.message}") from e

    def get_positions(self, portfolio_id: str) -> list[Position]:
        """Get all positions in a portfolio.

        Args:
            portfolio_id: Portfolio ID.

        Returns:
            List of positions.

        Raises:
            TradingError: If request fails.
        """
        try:
            response = self.http_client.get(
                f"/trading/positions?portfolio_id={portfolio_id}"
            )
            # Handle both direct list and wrapped response
            positions_data = (
                response if isinstance(response, list) else response.get("positions", [])
            )
            return [Position.from_dict(p) for p in positions_data]
        except HTTPError as e:
            raise TradingError(f"Failed to get positions: {e.message}") from e

    def get_trades(self, portfolio_id: str) -> list[Trade]:
        """Get all trades in a portfolio.

        Args:
            portfolio_id: Portfolio ID.

        Returns:
            List of trades.

        Raises:
            TradingError: If request fails.
        """
        try:
            response = self.http_client.get(
                f"/trading/trades?portfolio_id={portfolio_id}"
            )
            # Handle both direct list and wrapped response
            trades_data = (
                response if isinstance(response, list) else response.get("trades", [])
            )
            return [Trade.from_dict(t) for t in trades_data]
        except HTTPError as e:
            raise TradingError(f"Failed to get trades: {e.message}") from e

    def get_orders(self, portfolio_id: str) -> list[Order]:
        """Get all orders in a portfolio.

        Args:
            portfolio_id: Portfolio ID.

        Returns:
            List of orders.

        Raises:
            TradingError: If request fails.
        """
        try:
            response = self.http_client.get(
                f"/trading/orders?portfolio_id={portfolio_id}"
            )
            # Handle both direct list and wrapped response
            orders_data = (
                response if isinstance(response, list) else response.get("orders", [])
            )
            return [Order.from_dict(o) for o in orders_data]
        except HTTPError as e:
            raise TradingError(f"Failed to get orders: {e.message}") from e
