"""Portfolio endpoint service."""

from __future__ import annotations

from typing import Any
from python_sdk.utils.http_client import HTTPClient, HTTPError


class PortfolioError(Exception):
    """Exception raised for portfolio operations."""

    pass


class Portfolio:
    """Represents a portfolio."""

    def __init__(
        self, id: str, user_id: str, name: str, created_at: str | None = None
    ):
        """Initialize Portfolio.

        Args:
            id: Portfolio ID.
            user_id: Owner user ID.
            name: Portfolio name.
            created_at: Creation timestamp.
        """
        self.id = id
        self.user_id = user_id
        self.name = name
        self.created_at = created_at

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Portfolio":
        """Create Portfolio from API response dict.

        Args:
            data: Portfolio data from API.

        Returns:
            Portfolio instance.
        """
        return cls(
            id=data.get("id"),
            user_id=data.get("user_id"),
            name=data.get("name"),
            created_at=data.get("created_at"),
        )


class PortfolioService:
    """Service for portfolio operations."""

    def __init__(self, http_client: HTTPClient):
        """Initialize PortfolioService.

        Args:
            http_client: HTTPClient instance for making requests.
        """
        self.http_client = http_client

    def create_portfolio(self, name: str) -> Portfolio:
        """Create a new portfolio.

        Args:
            name: Portfolio name.

        Returns:
            Created portfolio.

        Raises:
            PortfolioError: If creation fails.
        """
        try:
            response = self.http_client.post("/portfolios", {"name": name})
            return Portfolio.from_dict(response)
        except HTTPError as e:
            raise PortfolioError(f"Failed to create portfolio: {e.message}") from e

    def list_portfolios(self) -> list[Portfolio]:
        """List all portfolios for the current user.

        Returns:
            List of portfolios.

        Raises:
            PortfolioError: If listing fails.
        """
        try:
            response = self.http_client.get("/portfolios")
            # Handle both direct list and wrapped response
            portfolios_data = (
                response if isinstance(response, list) else response.get("portfolios", [])
            )
            return [Portfolio.from_dict(p) for p in portfolios_data]
        except HTTPError as e:
            raise PortfolioError(f"Failed to list portfolios: {e.message}") from e

    def get_portfolio(self, portfolio_id: str) -> Portfolio:
        """Get a specific portfolio by ID.

        Args:
            portfolio_id: Portfolio ID.

        Returns:
            Portfolio details.

        Raises:
            PortfolioError: If portfolio not found or request fails.
        """
        try:
            response = self.http_client.get(f"/portfolios/{portfolio_id}")
            return Portfolio.from_dict(response)
        except HTTPError as e:
            raise PortfolioError(f"Failed to get portfolio: {e.message}") from e

    def delete_portfolio(self, portfolio_id: str) -> bool:
        """Delete a portfolio.

        Args:
            portfolio_id: Portfolio ID to delete.

        Returns:
            True if deletion was successful.

        Raises:
            PortfolioError: If deletion fails.
        """
        try:
            self.http_client.delete(f"/portfolios/{portfolio_id}")
            return True
        except HTTPError as e:
            raise PortfolioError(f"Failed to delete portfolio: {e.message}") from e
