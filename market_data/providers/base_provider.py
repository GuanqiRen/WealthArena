"""Base interface and shared errors for market data providers."""

from __future__ import annotations

from abc import ABC, abstractmethod

from market_data.models.price import HistoricalPriceBar, LatestPrice


class MarketDataError(Exception):
    """Base exception for all market data failures."""


class ConfigurationError(MarketDataError):
    """Raised when provider configuration is missing or invalid."""


class InvalidSymbolError(MarketDataError):
    """Raised when a stock symbol does not pass validation."""


class InvalidDateRangeError(MarketDataError):
    """Raised when a historical date range is invalid."""


class ProviderRequestError(MarketDataError):
    """Raised when HTTP requests to a provider fail."""


class ProviderResponseError(MarketDataError):
    """Raised when provider responses are malformed or incomplete."""


class BaseProvider(ABC):
    """Contract every market data provider implementation must satisfy."""

    @abstractmethod
    def get_latest_price(self, symbol: str) -> LatestPrice:
        """Return latest traded price for a symbol."""

    @abstractmethod
    def get_historical_prices(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
    ) -> list[HistoricalPriceBar]:
        """Return daily OHLCV bars for a symbol within [start_date, end_date]."""
