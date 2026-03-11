# WealthArena

## Poject Description

Build a real-time paper trading platform where user can place order with python apis.

## Progress Update (March 11, 2026)

### Completed: Market Data Module (First Task)

Implemented a modular `market_data` package with provider abstraction and Massive API integration.

Created files:

- `market_data/__init__.py`
- `market_data/market_data_client.py`
- `market_data/models/__init__.py`
- `market_data/models/price.py`
- `market_data/providers/__init__.py`
- `market_data/providers/base_provider.py`
- `market_data/providers/massive_provider.py`

### Architecture Implemented

- `MarketDataClient` is the public entry point for other modules.
- `BaseProvider` defines a provider interface:
	- `get_latest_price(symbol)`
	- `get_historical_prices(symbol, start_date, end_date)`
- `MassiveProvider` implements this interface and hides provider-specific API details.

This allows replacing Massive with another provider without changing trading engine integration.

### Data Models Added

- `LatestPrice`: normalized latest quote payload (`symbol`, `price`, `timestamp_ms`, `source`)
- `HistoricalPriceBar`: normalized daily OHLCV payload (`date`, `open`, `high`, `low`, `close`, `volume`, `timestamp_ms`, `source`)

### Error Handling Added

- Missing API key configuration (`MASSIVE_API_KEY`)
- Invalid stock symbol format
- Invalid date ranges / date format validation (`YYYY-MM-DD`)
- Network and HTTP failures
- Malformed or unexpected API responses
- Provider-reported errors (including authorization/entitlement errors)

### Environment Setup

Added local env configuration and git safety:

- `.env` for local secrets and runtime configuration
- `.env.example` as shareable template
- `.gitignore` rules to prevent committing real secrets while keeping `.env.example`

Required variables:

- `MASSIVE_API_KEY` (required)
- `MASSIVE_API_BASE_URL` (optional, defaults to `https://api.polygon.io`)

### Smoke Tests Run

Validation completed:

- Python compile check passed for `market_data` package.
- Live API smoke test passed for latest price retrieval.
- Live API smoke test passed for historical prices in an entitled recent timeframe.

Observed entitlement behavior:

- Some endpoints/timeframes are plan-dependent on Massive/Polygon.
- `get_latest_price` now includes a fallback from `/v2/last/trade/{symbol}` to `/v2/aggs/ticker/{symbol}/prev` when the account is not entitled to last-trade data.
- Historical requests for older windows (example: early 2024) may return authorization errors depending on plan.

### Example Usage

```python
from market_data.market_data_client import MarketDataClient

client = MarketDataClient()

latest = client.get_latest_price("AAPL")
history = client.get_historical_prices("AAPL", "2026-03-04", "2026-03-11")

print(latest)
print(len(history))
```

### Completed: Market Data Cache Service (Second Task)

Implemented an in-memory cache layer that sits between the trading engine and `MarketDataClient` to reduce repeated Massive API calls.

Created files:

- `market_data/cache/price_cache.py`
- `market_data/cache/__init__.py`
- `market_data/config/price_cache_config.yaml`

Updated files:

- `market_data/__init__.py` (exports `PriceCache`)

### Cache Architecture Implemented

System flow:

`Trading Engine -> PriceCache -> MarketDataClient -> MassiveProvider`

Core design:

- In-memory dictionary cache keyed by symbol.
- Internal entry stores latest `price` and `cached_at` timestamp.
- Supports multiple symbols.
- Uses a lock to keep cache access thread-safe.

`get_price(symbol)` behavior:

- Returns cached value if entry is still fresh.
- If expired or missing, calls `MarketDataClient.get_latest_price(symbol)`.
- Refreshes cache and returns updated price.
- Wraps upstream failures in `PriceCacheError` with clear context.

### Cache Configuration

Config file:

- `market_data/config/price_cache_config.yaml`

Default config:

```yaml
price_cache:
	expiry_seconds: 5
```

Configuration precedence:

1. `PRICE_CACHE_EXPIRY_SECONDS` environment variable (if set)
2. YAML value `price_cache.expiry_seconds`
3. Safe default (`5` seconds)

Validation:

- `expiry_seconds` must be a positive integer.
- Invalid values raise `PriceCacheError` with clear messages.

### Verification Results

Cache behavior was validated with a deterministic smoke test using a fake market data client:

- Repeated call within TTL returned cached price.
- Call after TTL expiration refreshed from client.
- API call count confirmed reduced calls:
	- first call fetches from client
	- second call hits cache
	- third call (after TTL) fetches again

Observed sample output:

- `P1 101.0`
- `P2 101.0`
- `P3 102.0`
- `CALLS 2`

### Developer Ergonomics Added

To run example scripts directly from VS Code Run/Debug without import path issues, workspace configs were added:

- `.vscode/settings.json`
- `.vscode/launch.json`

These set interpreter to `.venv` and apply `PYTHONPATH=${workspaceFolder}` for consistent imports.
