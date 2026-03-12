"""Repository for portfolio persistence."""

from __future__ import annotations

from typing import Any

from backend.db.supabase_client import SupabaseRestClient, get_supabase_client


class PortfolioRepository:
    def __init__(self, client: SupabaseRestClient | None = None) -> None:
        self._client = client or get_supabase_client()

    def create_portfolio(self, user_id: str, name: str, portfolio_id: str | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "user_id": user_id,
            "name": name,
        }
        if portfolio_id is not None:
            payload["id"] = portfolio_id
        return self._client.insert("portfolios", payload)

    def get_portfolio(self, portfolio_id: str) -> dict[str, Any] | None:
        return self._client.select_one("portfolios", filters={"id": f"eq.{portfolio_id}"})

    def get_user_portfolios(self, user_id: str) -> list[dict[str, Any]]:
        return self._client.select("portfolios", filters={"user_id": f"eq.{user_id}"})

    def delete_portfolio(self, portfolio_id: str) -> None:
        self._client.delete("portfolios", filters={"id": f"eq.{portfolio_id}"})
