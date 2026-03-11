"""In-memory latest price cache sitting between the trading engine and market data client."""

from __future__ import annotations

import os
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from market_data.market_data_client import MarketDataClient


class PriceCacheError(Exception):
    """Raised when cache refresh cannot retrieve data from market data client."""


@dataclass
class _CacheEntry:
    price: float
    cached_at: float


class PriceCache:
    """Caches latest prices in memory to reduce provider API calls."""

    _DEFAULT_EXPIRY_SECONDS = 5

    def __init__(
        self,
        market_data_client: MarketDataClient | None = None,
        config_path: str | None = None,
    ) -> None:
        self._market_data_client = market_data_client or MarketDataClient()
        self._config_path = (
            Path(config_path)
            if config_path
            else Path(__file__).resolve().parents[1] / "config" / "price_cache_config.yaml"
        )
        self._expiry_seconds = self._load_expiry_seconds()
        self._cache: dict[str, _CacheEntry] = {}
        self._lock = threading.Lock()

    def get_price(self, symbol: str) -> float:
        """Return a latest price using cache if fresh, otherwise refresh from provider."""
        normalized_symbol = symbol.strip().upper()
        now = time.time()

        with self._lock:
            existing = self._cache.get(normalized_symbol)
            if existing and (now - existing.cached_at) < self._expiry_seconds:
                return existing.price

        try:
            latest = self._market_data_client.get_latest_price(normalized_symbol)
        except Exception as exc:
            raise PriceCacheError(
                f"Failed to retrieve latest price for symbol '{normalized_symbol}': {exc}"
            ) from exc

        with self._lock:
            self._cache[normalized_symbol] = _CacheEntry(price=float(latest.price), cached_at=now)
            return self._cache[normalized_symbol].price

    def _load_expiry_seconds(self) -> int:
        """Load TTL from env/config with safe defaults and validation."""
        env_ttl = os.getenv("PRICE_CACHE_EXPIRY_SECONDS")
        if env_ttl is not None:
            return self._parse_expiry(env_ttl, source="PRICE_CACHE_EXPIRY_SECONDS")

        if not self._config_path.exists():
            return self._DEFAULT_EXPIRY_SECONDS

        parsed_from_yaml = self._load_expiry_from_yaml(self._config_path)
        if parsed_from_yaml is None:
            return self._DEFAULT_EXPIRY_SECONDS
        return self._parse_expiry(str(parsed_from_yaml), source=str(self._config_path))

    def _load_expiry_from_yaml(self, path: Path) -> Any | None:
        """Read `price_cache.expiry_seconds` from YAML; supports a minimal fallback parser."""
        text = path.read_text(encoding="utf-8")

        try:
            import yaml  # type: ignore

            data = yaml.safe_load(text) or {}
            if not isinstance(data, dict):
                return None
            cache_config = data.get("price_cache", {})
            if not isinstance(cache_config, dict):
                return None
            return cache_config.get("expiry_seconds")
        except ImportError:
            # Fallback for environments without PyYAML: parse only the needed key.
            for line in text.splitlines():
                stripped = line.split("#", 1)[0].strip()
                if stripped.startswith("expiry_seconds:"):
                    return stripped.split(":", 1)[1].strip()
            return None

    def _parse_expiry(self, value: str, source: str) -> int:
        try:
            expiry = int(value)
        except (TypeError, ValueError) as exc:
            raise PriceCacheError(
                f"Invalid expiry_seconds value '{value}' from {source}; expected a positive integer."
            ) from exc

        if expiry <= 0:
            raise PriceCacheError(
                f"Invalid expiry_seconds value '{value}' from {source}; must be > 0."
            )

        return expiry
