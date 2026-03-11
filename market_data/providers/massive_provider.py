"""Massive API provider implementation.

Massive was formerly Polygon.io. This adapter targets the public REST shape
used by Massive/Polygon endpoints and keeps those details behind BaseProvider.
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from market_data.models.price import HistoricalPriceBar, LatestPrice
from market_data.providers.base_provider import (
    BaseProvider,
    ConfigurationError,
    InvalidDateRangeError,
    InvalidSymbolError,
    ProviderRequestError,
    ProviderResponseError,
)


class MassiveProvider(BaseProvider):
    """Provider that fetches prices from Massive/Polygon style endpoints."""

    _DEFAULT_BASE_URL = "https://api.polygon.io"
    _SYMBOL_PATTERN = re.compile(r"^[A-Z][A-Z0-9.\-]{0,9}$")

    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:
        self._api_key = api_key or os.getenv("MASSIVE_API_KEY")
        self._base_url = (base_url or os.getenv("MASSIVE_API_BASE_URL") or self._DEFAULT_BASE_URL).rstrip("/")
        if not self._api_key:
            raise ConfigurationError(
                "Missing MASSIVE_API_KEY environment variable for MassiveProvider."
            )

    def get_latest_price(self, symbol: str) -> LatestPrice:
        normalized_symbol = self._validate_symbol(symbol)
        try:
            payload = self._request_json(
                path=f"/v2/last/trade/{normalized_symbol}",
                params={"apiKey": self._api_key},
            )

            results = payload.get("results")
            if not isinstance(results, dict):
                raise ProviderResponseError(
                    f"Massive latest price response missing 'results' for symbol {normalized_symbol}."
                )

            price = results.get("p")
            timestamp = results.get("t")
            if price is None or timestamp is None:
                raise ProviderResponseError(
                    f"Massive latest price response missing price/timestamp for symbol {normalized_symbol}."
                )

            return LatestPrice(
                symbol=normalized_symbol,
                price=float(price),
                timestamp_ms=int(timestamp),
                source="massive",
            )
        except ProviderRequestError as exc:
            # Some plans are not entitled to /v2/last/trade. Fall back to previous close.
            if "NOT_AUTHORIZED" not in str(exc) and "not entitled" not in str(exc).lower():
                raise

        fallback = self._request_json(
            path=f"/v2/aggs/ticker/{normalized_symbol}/prev",
            params={
                "adjusted": "true",
                "apiKey": self._api_key,
            },
        )
        fallback_results = fallback.get("results")
        if not isinstance(fallback_results, list) or not fallback_results:
            raise ProviderResponseError(
                f"Massive fallback latest price response missing 'results' for symbol {normalized_symbol}."
            )

        first = fallback_results[0]
        if not isinstance(first, dict):
            raise ProviderResponseError(
                f"Massive fallback latest price response has invalid bar format for symbol {normalized_symbol}."
            )

        close = first.get("c")
        timestamp = first.get("t")
        if close is None or timestamp is None:
            raise ProviderResponseError(
                f"Massive fallback latest price response missing close/timestamp for symbol {normalized_symbol}."
            )

        return LatestPrice(
            symbol=normalized_symbol,
            price=float(close),
            timestamp_ms=int(timestamp),
            source="massive",
        )

    def get_historical_prices(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
    ) -> list[HistoricalPriceBar]:
        normalized_symbol = self._validate_symbol(symbol)
        self._validate_date_range(start_date, end_date)

        payload = self._request_json(
            path=f"/v2/aggs/ticker/{normalized_symbol}/range/1/day/{start_date}/{end_date}",
            params={
                "adjusted": "true",
                "sort": "asc",
                "limit": "50000",
                "apiKey": self._api_key,
            },
        )

        results = payload.get("results", [])
        if not isinstance(results, list):
            raise ProviderResponseError(
                f"Massive historical response has invalid 'results' for symbol {normalized_symbol}."
            )

        bars: list[HistoricalPriceBar] = []
        for result in results:
            if not isinstance(result, dict):
                continue

            timestamp = result.get("t")
            if timestamp is None:
                continue

            bar_date = datetime.utcfromtimestamp(int(timestamp) / 1000).strftime("%Y-%m-%d")
            bars.append(
                HistoricalPriceBar(
                    symbol=normalized_symbol,
                    date=bar_date,
                    open=float(result.get("o", 0.0)),
                    high=float(result.get("h", 0.0)),
                    low=float(result.get("l", 0.0)),
                    close=float(result.get("c", 0.0)),
                    volume=float(result.get("v", 0.0)),
                    timestamp_ms=int(timestamp),
                    source="massive",
                )
            )

        return bars

    def _request_json(self, path: str, params: dict[str, str]) -> dict[str, Any]:
        query = urlencode(params)
        url = f"{self._base_url}{path}?{query}"
        request = Request(url, headers={"Accept": "application/json"}, method="GET")

        try:
            with urlopen(request, timeout=10) as response:
                raw_payload = response.read().decode("utf-8")
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace") if hasattr(exc, "read") else ""
            raise ProviderRequestError(
                f"Massive API request failed with HTTP {exc.code}: {body}"
            ) from exc
        except URLError as exc:
            raise ProviderRequestError(f"Network failure calling Massive API: {exc.reason}") from exc
        except TimeoutError as exc:
            raise ProviderRequestError("Massive API request timed out.") from exc

        try:
            payload = json.loads(raw_payload)
        except json.JSONDecodeError as exc:
            raise ProviderResponseError("Massive API returned non-JSON response.") from exc

        if not isinstance(payload, dict):
            raise ProviderResponseError("Massive API returned unexpected JSON structure.")

        if payload.get("status") in {"ERROR", "NOT_AUTHORIZED"}:
            message = payload.get("error") or payload.get("message") or "Unknown provider error"
            raise ProviderRequestError(f"Massive API error: {message}")

        return payload

    def _validate_symbol(self, symbol: str) -> str:
        normalized = symbol.strip().upper()
        if not normalized or not self._SYMBOL_PATTERN.fullmatch(normalized):
            raise InvalidSymbolError(
                f"Invalid stock symbol '{symbol}'. Use 1-10 characters: A-Z, 0-9, '.', '-'."
            )
        return normalized

    def _validate_date_range(self, start_date: str, end_date: str) -> None:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError as exc:
            raise InvalidDateRangeError(
                "Dates must be in ISO format YYYY-MM-DD."
            ) from exc

        if start > end:
            raise InvalidDateRangeError("start_date cannot be after end_date.")
