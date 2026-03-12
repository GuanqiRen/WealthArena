"""Portfolio service — portfolio operations with user ownership enforcement.

All mutating operations verify that the portfolio belongs to the requesting
user before proceeding, so one user can never modify another user's data.
"""

from __future__ import annotations

from typing import Any

from backend.repositories.portfolio_repository import PortfolioRepository


class PortfolioServiceError(Exception):
    """Raised when a portfolio service operation fails."""


class PortfolioNotFoundError(PortfolioServiceError):
    """Raised when the requested portfolio does not exist."""


class PortfolioAccessDeniedError(PortfolioServiceError):
    """Raised when a user tries to access a portfolio they do not own."""


class PortfolioService:
    """Manages portfolio lifecycle with user ownership checks."""

    def __init__(self, portfolio_repository: PortfolioRepository | None = None) -> None:
        self._repo = portfolio_repository or PortfolioRepository()

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def create_portfolio(self, user_id: str, name: str) -> dict[str, Any]:
        """Create a new portfolio owned by user_id.

        Returns the created portfolio record (includes the generated id).
        """
        if not user_id:
            raise PortfolioServiceError("user_id is required to create a portfolio.")
        if not name or not name.strip():
            raise PortfolioServiceError("Portfolio name cannot be empty.")

        return self._repo.create_portfolio(user_id=user_id, name=name.strip())

    def delete_portfolio(self, portfolio_id: str, user_id: str) -> None:
        """Delete a portfolio, verifying that it belongs to user_id first.

        Raises PortfolioNotFoundError if the portfolio does not exist.
        Raises PortfolioAccessDeniedError if the portfolio belongs to a different user.
        """
        portfolio = self._repo.get_portfolio(portfolio_id)
        if portfolio is None:
            raise PortfolioNotFoundError(
                f"Portfolio '{portfolio_id}' not found."
            )
        if portfolio.get("user_id") != user_id:
            raise PortfolioAccessDeniedError(
                f"User '{user_id}' does not own portfolio '{portfolio_id}'."
            )
        self._repo.delete_portfolio(portfolio_id)

    def get_user_portfolios(self, user_id: str) -> list[dict[str, Any]]:
        """Return all portfolios belonging to user_id."""
        if not user_id:
            raise PortfolioServiceError("user_id is required.")
        return self._repo.get_user_portfolios(user_id)

    def get_portfolio(self, portfolio_id: str, user_id: str) -> dict[str, Any]:
        """Return a single portfolio, verifying ownership.

        Raises PortfolioNotFoundError or PortfolioAccessDeniedError as needed.
        """
        portfolio = self._repo.get_portfolio(portfolio_id)
        if portfolio is None:
            raise PortfolioNotFoundError(f"Portfolio '{portfolio_id}' not found.")
        if portfolio.get("user_id") != user_id:
            raise PortfolioAccessDeniedError(
                f"User '{user_id}' does not own portfolio '{portfolio_id}'."
            )
        return portfolio
