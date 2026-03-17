"""WealthArena Python Trading SDK.

A clean, easy-to-use client library for interacting with the WealthArena
trading platform API.

Example usage:
    from python_sdk import TradingClient

    # Initialize client with credentials
    client = TradingClient(
        base_url="http://localhost:8000",
        email="user@example.com",
        password="password"
    )

    # Authenticate
    client.login()

    # Create a portfolio
    portfolio = client.create_portfolio("My Portfolio")

    # Place an order
    order = client.place_order(
        portfolio_id=portfolio.id,
        symbol="AAPL",
        quantity=10,
        side="buy"
    )

    # Get positions
    positions = client.get_positions(portfolio_id=portfolio.id)

    # List trades
    trades = client.get_trades(portfolio_id=portfolio.id)
"""

from .client import TradingClient, TradingClientError
from .auth import AuthToken, AuthError, AuthService
from .endpoints.portfolio import Portfolio, PortfolioError
from .endpoints.trading import TradingError
from .models import Order, Position, Trade

__version__ = "1.0.0"

__all__ = [
    # Client
    "TradingClient",
    "TradingClientError",
    # Auth
    "AuthToken",
    "AuthError",
    "AuthService",
    # Portfolio
    "Portfolio",
    "PortfolioError",
    # Trading
    "TradingError",
    # Models
    "Order",
    "Position",
    "Trade",
]
