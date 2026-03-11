# Project Goal

Build a browser-based paper trading platform that allows users to simulate stock trading using real-time market data without executing real trades.

The system should support user accounts, portfolio management, simulated order execution, and a dashboard for tracking performance.


# Core Features

## 1. User Accounts

- Users can register and log in.
- Authentication must be handled securely.
- Each user can manage multiple portfolios.


## 2. Portfolio Management

Users can:

- Create portfolios
- Delete portfolios
- View portfolio positions
- Track portfolio performance

Portfolio data must be persisted in the backend database.


## 3. Market Data

The platform should load real-time stock price data from an external API.

The system should support retrieving:
- latest price
- historical prices (optional future feature)

The market data provider should be modular so it can be replaced easily.


## 4. Paper Trading Engine

Users should be able to:

- Place buy orders
- Place sell orders
- Cancel orders
- View order history

Orders should simulate realistic behavior including:

- order status
- filled quantity
- execution price
- timestamps


## 5. Python Trading API

Provide a Python API / SDK that allows users to programmatically:

- place orders
- cancel orders
- query portfolio positions
- query account status

Example usage:

client.place_order("AAPL", qty=10, side="buy")

This allows users to build automated trading strategies.


## 6. Web Dashboard

Provide a browser-based frontend dashboard that allows users to:

- View portfolios
- View positions
- View trade history
- Monitor portfolio performance
- Visualize PnL and asset allocation


# Technology Stack

Backend:
- Use Supabase for authentication, database, and backend services.
- Use PostgreSQL via Supabase to store:
  - users
  - portfolios
  - positions
  - orders
  - trade history

Trading Engine:
- Implement trading logic in Python.
- Responsibilities include:
  - order management
  - portfolio updates
  - trade simulation
  - providing an API for programmatic trading

Frontend:
- Build a browser-based dashboard.
- Recommended technologies:
  - React or a similar web framework
  - a charting library for portfolio visualization


# Architecture Guidelines

The system should follow a modular architecture:

Frontend Dashboard
    |
    v
Backend API (Supabase)
    |
    v
Trading Engine (Python)
    |
    v
Market Data Provider

Key design principles:

- modular architecture
- clear separation of frontend, backend, and trading logic
- easily replaceable market data source
- scalable backend


# Coding Rules

When generating code:

1. Use a clear modular project structure.
2. Write clean and readable code.
3. Add comments explaining:
   - architecture decisions
   - important logic
4. Prefer simple and maintainable implementations.
5. Avoid unnecessary complexity.


# Development Expectations for Claude

When implementing features:

- Explain major architectural decisions.
- Propose file structure before generating large amounts of code.
- Build the system incrementally.
- Ensure all components integrate correctly.

# Project File Structure

The repository should follow this structure unless there is a strong reason to change it.

project-root/
    frontend/
        src/
        components/
        pages/
        services/
    backend/
        api/
        services/
        models/
    trading_engine/
        engine/
        order_manager.py
        portfolio_manager.py
        execution_simulator.py
    market_data/
        providers/
        market_data_client.py
    python_sdk/
        client.py
        orders.py
        portfolio.py
    database/
        schema.sql
        migrations/
    docs/
    tests/

Guidelines:
- Keep modules small and focused.
- Each directory should represent a clear responsibility.
- Avoid mixing frontend and backend logic.

# Implementation Workflow

When implementing new functionality, follow this workflow:

1. Understand the feature requirements.
2. Propose the architecture and file changes first.
3. Wait for confirmation if the change is large.
4. Implement the feature in small steps.
5. Ensure new code integrates with existing modules.
6. Add comments explaining important design choices.

Avoid generating large amounts of code without first explaining the structure.

# Market Data Abstraction

Market data providers must be abstracted behind a common interface.

Example interface:

get_latest_price(symbol)
get_historical_prices(symbol, start_date, end_date)

The implementation should allow switching providers without changing trading logic.

# Trading Engine Rules

The trading engine should simulate realistic behavior:

- Market orders execute at the latest available price.
- Orders must update portfolio positions immediately after execution.
- All trades must be recorded in trade history.
- Portfolio PnL should be recalculated after each trade.