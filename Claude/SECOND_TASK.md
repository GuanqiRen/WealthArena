# SECOND TASK

The next component to implement is the Market Data Cache Service.

This service sits between the trading engine and the market_data module implemented in the first task.

The purpose of this service is to cache recent stock prices so the system does not repeatedly call the Massive API.


# Objective

Build a price cache layer that:

- retrieves prices from the market_data module
- caches the latest price for each symbol
- reduces the number of external API calls
- improves response speed for the trading engine


# Architecture

The system should now look like this:

Trading Engine
      |
      v
Market Data Cache Service
      |
      v
Market Data Client
      |
      v
Massive API


# Responsibilities

The cache service must:

- request prices from MarketDataClient when needed
- store the latest price in memory
- return cached prices if they are still fresh
- refresh prices when the cache expires


# Directory Structure

Create the following module if it does not already exist:

market_data/
    config/
        price_cache_config.yaml
    cache/
        price_cache.py


# Cache Design

The cache should store:

symbol
price
timestamp

Example internal structure:

{
    "AAPL": {
        "price": 180.25,
        "timestamp": 1712000000
    }
}


# Cache Rules

1. Cached prices should expire after a short time period.

Recommended expiration:

5 seconds

make this time period configurable

Example Configuration:

price_cache:
    expiry_seconds: 5


2. If a price is requested and the cached value is still valid, return it.

3. If the cache entry has expired:

- call MarketDataClient
- refresh the cache
- return the updated price


# Required Interface

The cache service should expose a simple interface:

get_price(symbol)


Example usage:

from market_data.cache.price_cache import PriceCache

cache = PriceCache()

price = cache.get_price("AAPL")


# Implementation Requirements

The cache should:

- use an in-memory dictionary
- store timestamps for cache entries
- handle multiple symbols
- avoid unnecessary API calls


# Error Handling

The cache service must:

- handle failures from the market_data client
- return clear error messages if price retrieval fails


# Implementation Workflow

Before writing code:

1. Explain the cache design.
2. Explain how the cache interacts with MarketDataClient.

Then implement:

1. price_cache.py


# Success Criteria

The task is complete when:

- requesting the same symbol multiple times within the cache window does NOT trigger new API calls
- prices refresh automatically after expiration
- the module integrates with the MarketDataClient created in the first task