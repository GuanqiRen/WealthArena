# FIRST TASK

The first component to implement for this project is the Market Data module.

This module is responsible for retrieving stock market data from the Massive API and providing a clean internal interface for the rest of the system (such as the trading engine).

The implementation must follow the architecture and coding rules defined in CLAUDE.md.


# Objective

Build a market_data component that retrieves stock prices using the Massive API.

The design must include a provider abstraction layer so that the system can switch to another market data provider in the future with minimal changes.


# Responsibilities of the Market Data Module

The market data module must:

- Retrieve the latest price for a stock symbol
- Retrieve historical price data
- Provide a simple interface for the trading engine
- Hide API implementation details from the rest of the system
- Handle API errors gracefully


# Massive API Integration

Use the Massive stock market data API.

The provider should support:

- retrieving the latest stock price
- retrieving historical OHLC price data

The API key should NOT be hardcoded. It should be loaded from an environment variable:

MASSIVE_API_KEY


# Required Interface

The market data module must expose the following functions through a client class:

get_latest_price(symbol)

Returns the latest price for a stock symbol.

Example:

price = client.get_latest_price("AAPL")


get_historical_prices(symbol, start_date, end_date)

Returns historical price data between two dates.

Example:

data = client.get_historical_prices("AAPL", "2024-01-01", "2024-02-01")


# Directory Structure

Create the following module structure:

market_data/
    __init__.py
    market_data_client.py
    models/
        price.py
    providers/
        base_provider.py
        massive_provider.py


# Design Requirements

1. Implement a provider abstraction layer.

2. Create a BaseProvider interface in:

providers/base_provider.py

This file should define the required functions for all market data providers.

3. Implement MassiveProvider in:

providers/massive_provider.py

This provider will call the Massive API.

4. Create MarketDataClient in:

market_data_client.py

This client should act as the entry point used by the rest of the system.

Other components must interact ONLY with MarketDataClient.


# Example Usage

Example of how the trading engine should use this module:

from market_data.market_data_client import MarketDataClient

client = MarketDataClient()

price = client.get_latest_price("AAPL")

print(price)


# Implementation Workflow

Before writing code:

1. Propose the full file structure for the module.
2. Explain the provider abstraction design.
3. Explain how the Massive API will be integrated.

After that:

4. Implement the files one by one.
5. Add comments explaining key design decisions.


# Error Handling

The module should:

- handle API errors
- handle network failures
- validate stock symbols
- return clear error messages


# Success Criteria

The task is complete when:

- The market_data module compiles and runs
- get_latest_price(symbol) returns a real price from Massive
- get_historical_prices works
- The provider abstraction is clean and extensible
- The code is well structured and documented