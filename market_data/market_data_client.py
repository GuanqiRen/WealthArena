"""Public market data client used by the trading engine and other modules."""

from __future__ import annotations

from market_data.models.price import HistoricalPriceBar, LatestPrice
from market_data.providers.base_provider import BaseProvider
from market_data.providers.massive_provider import MassiveProvider


class MarketDataClient:
    """Facade that hides provider-specific API details from the rest of the app."""

    def __init__(self, provider: BaseProvider | None = None) -> None:
        self._provider = provider or MassiveProvider()

    def get_latest_price(self, symbol: str) -> LatestPrice:
        return self._provider.get_latest_price(symbol)

    def get_historical_prices(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
    ) -> list[HistoricalPriceBar]:
        return self._provider.get_historical_prices(symbol, start_date, end_date)
