"""Main TradingClient class for SDK users."""

from __future__ import annotations

from typing import Any
from python_sdk.utils.http_client import HTTPClient
from python_sdk.auth import AuthService, AuthError, AuthToken
from python_sdk.endpoints.portfolio import PortfolioService, Portfolio, PortfolioError
from python_sdk.endpoints.trading import TradingService, TradingError
from python_sdk.models import Order, Position, Trade


class TradingClientError(Exception):
    """Exception raised for TradingClient errors."""

    pass


class TradingClient:
    """Main client for interacting with the WealthArena trading platform.

    Example usage:
        client = TradingClient(
            base_url="http://localhost:8000",
            email="user@example.com",
            password="password"
        )
        client.login()

        portfolio = client.create_portfolio("My Portfolio")
        client.place_order(
            portfolio_id=portfolio.id,
            symbol="AAPL",
            quantity=10,
            side="buy"
        )
        positions = client.get_positions(portfolio_id=portfolio.id)
    """

    def __init__(
        self,
        base_url: str,
        email: str | None = None,
        password: str | None = None,
        token: str | None = None,
    ):
        """Initialize TradingClient.

        Args:
            base_url: Base URL of the API (e.g., "http://localhost:8000").
            email: User email (required if not using token).
            password: User password (required if not using token).
            token: Existing JWT token (alternative to email/password).

        Raises:
            TradingClientError: If initialization fails.
        """
        self.base_url = base_url
        self.email = email
        self.password = password
        self.token: AuthToken | None = None

        # Initialize HTTP client
        self.http_client = HTTPClient(base_url)

        # If token is provided, use it directly
        if token:
            self.http_client.set_token(token)
            self.token = AuthToken(access_token=token)

        # Initialize services
        self.auth_service = AuthService(self.http_client)
        self.portfolio_service = PortfolioService(self.http_client)
        self.trading_service = TradingService(self.http_client)

    def register(self, email: str, password: str) -> dict[str, Any]:
        """Register a new user.

        Args:
            email: Email address.
            password: Password.

        Returns:
            Registration response with user_id and email.

        Raises:
            TradingClientError: If registration fails.
        """
        try:
            return self.auth_service.register(email, password)
        except AuthError as e:
            raise TradingClientError(f"Registration failed: {str(e)}") from e

    def login(self) -> AuthToken:
        """Authenticate user and obtain access token.

        Uses email and password provided in __init__.

        Returns:
            AuthToken with access token and user info.

        Raises:
            TradingClientError: If login fails or credentials not provided.
        """
        if not self.email or not self.password:
            raise TradingClientError(
                "Email and password required for login. "
                "Provide them in __init__ or use token parameter."
            )

        try:
            self.token = self.auth_service.login(self.email, self.password)
            self.http_client.set_token(self.token.access_token, self.token.token_type)
            return self.token
        except AuthError as e:
            raise TradingClientError(f"Login failed: {str(e)}") from e

    def is_authenticated(self) -> bool:
        """Check if client is authenticated.

        Returns:
            True if token is available, False otherwise.
        """
        return self.token is not None and self.http_client.token is not None

    def create_portfolio(self, name: str) -> Portfolio:
        """Create a new portfolio.

        Args:
            name: Name of the portfolio.

        Returns:
            Created Portfolio object.

        Raises:
            TradingClientError: If not authenticated or creation fails.
        """
        if not self.is_authenticated():
            raise TradingClientError("Not authenticated. Call login() first.")

        try:
            return self.portfolio_service.create_portfolio(name)
        except PortfolioError as e:
            raise TradingClientError(f"Portfolio creation failed: {str(e)}") from e

    def list_portfolios(self) -> list[Portfolio]:
        """List all portfolios for the current user.

        Returns:
            List of Portfolio objects.

        Raises:
            TradingClientError: If not authenticated or request fails.
        """
        if not self.is_authenticated():
            raise TradingClientError("Not authenticated. Call login() first.")

        try:
            return self.portfolio_service.list_portfolios()
        except PortfolioError as e:
            raise TradingClientError(f"Failed to list portfolios: {str(e)}") from e

    def get_portfolio(self, portfolio_id: str) -> Portfolio:
        """Get a specific portfolio by ID.

        Args:
            portfolio_id: Portfolio ID.

        Returns:
            Portfolio object.

        Raises:
            TradingClientError: If not authenticated or portfolio not found.
        """
        if not self.is_authenticated():
            raise TradingClientError("Not authenticated. Call login() first.")

        try:
            return self.portfolio_service.get_portfolio(portfolio_id)
        except PortfolioError as e:
            raise TradingClientError(f"Failed to get portfolio: {str(e)}") from e

    def delete_portfolio(self, portfolio_id: str) -> bool:
        """Delete a portfolio.

        Args:
            portfolio_id: Portfolio ID to delete.

        Returns:
            True if deletion was successful.

        Raises:
            TradingClientError: If not authenticated or deletion fails.
        """
        if not self.is_authenticated():
            raise TradingClientError("Not authenticated. Call login() first.")

        try:
            return self.portfolio_service.delete_portfolio(portfolio_id)
        except PortfolioError as e:
            raise TradingClientError(f"Failed to delete portfolio: {str(e)}") from e

    def place_order(
        self,
        portfolio_id: str,
        symbol: str,
        quantity: int,
        side: str,
    ) -> dict[str, Any]:
        """Place a market order in a portfolio.

        Args:
            portfolio_id: Portfolio ID.
            symbol: Stock symbol (e.g., "AAPL").
            quantity: Number of shares.
            side: "buy" or "sell".

        Returns:
            Order response with order, trade, and position data.

        Raises:
            TradingClientError: If not authenticated or order fails.
        """
        if not self.is_authenticated():
            raise TradingClientError("Not authenticated. Call login() first.")

        try:
            return self.trading_service.place_order(portfolio_id, symbol, quantity, side)
        except TradingError as e:
            raise TradingClientError(f"Order placement failed: {str(e)}") from e

    def get_positions(self, portfolio_id: str) -> list[Position]:
        """Get all positions in a portfolio.

        Args:
            portfolio_id: Portfolio ID.

        Returns:
            List of Position objects.

        Raises:
            TradingClientError: If not authenticated or request fails.
        """
        if not self.is_authenticated():
            raise TradingClientError("Not authenticated. Call login() first.")

        try:
            return self.trading_service.get_positions(portfolio_id)
        except TradingError as e:
            raise TradingClientError(f"Failed to get positions: {str(e)}") from e

    def get_trades(self, portfolio_id: str) -> list[Trade]:
        """Get all trades in a portfolio.

        Args:
            portfolio_id: Portfolio ID.

        Returns:
            List of Trade objects.

        Raises:
            TradingClientError: If not authenticated or request fails.
        """
        if not self.is_authenticated():
            raise TradingClientError("Not authenticated. Call login() first.")

        try:
            return self.trading_service.get_trades(portfolio_id)
        except TradingError as e:
            raise TradingClientError(f"Failed to get trades: {str(e)}") from e

    def get_orders(self, portfolio_id: str) -> list[Order]:
        """Get all orders in a portfolio.

        Args:
            portfolio_id: Portfolio ID.

        Returns:
            List of Order objects.

        Raises:
            TradingClientError: If not authenticated or request fails.
        """
        if not self.is_authenticated():
            raise TradingClientError("Not authenticated. Call login() first.")

        try:
            return self.trading_service.get_orders(portfolio_id)
        except TradingError as e:
            raise TradingClientError(f"Failed to get orders: {str(e)}") from e
