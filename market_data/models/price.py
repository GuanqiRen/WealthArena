"""Normalized market data models used by the trading system."""

from dataclasses import dataclass


@dataclass(frozen=True)
class LatestPrice:
    """Latest trade price for a symbol."""

    symbol: str
    price: float
    timestamp_ms: int
    source: str = "massive"


@dataclass(frozen=True)
class HistoricalPriceBar:
    """Single OHLCV bar for a trading day."""

    symbol: str
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    timestamp_ms: int
    source: str = "massive"
