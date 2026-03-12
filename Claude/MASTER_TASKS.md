# MASTER TASK ROADMAP

This document defines the development roadmap for the browser-based paper trading platform.

Claude should follow these tasks sequentially and complete them one stage at a time.

Before implementing each stage:

1. Explain the design.
2. Propose file structure changes.
3. Then implement the code incrementally.

Do NOT skip steps or implement future components early.


--------------------------------------------------
PHASE 1 — MARKET DATA LAYER
--------------------------------------------------

Goal:
Provide reliable stock price data for the rest of the system.

Tasks:

1. Market Data Module
   - Implement market_data module
   - Integrate with Massive API
   - Create provider abstraction layer

   Files include:
   - market_data_client.py
   - providers/base_provider.py
   - providers/massive_provider.py

2. Price Cache Service
   - Implement in-memory price cache
   - Cache recent prices to avoid excessive API calls
   - Integrate with MarketDataClient

   Files include:
   - market_data/cache/price_cache.py


--------------------------------------------------
PHASE 2 — PAPER TRADING ENGINE
--------------------------------------------------

Goal:
Simulate realistic trading behavior.

Tasks:

3. Trading Engine Core
   - Implement order placement
   - Execute market orders
   - Record trades
   - Update portfolio positions

   Modules include:
   - trading_engine.py
   - order_manager.py
   - portfolio_manager.py

4. Trading Models
   - Order
   - Trade
   - Position

5. Portfolio Calculations
   - Average price calculation
   - Position updates


--------------------------------------------------
PHASE 3 — DATABASE PERSISTENCE
--------------------------------------------------

Goal:
Persist trading data and user portfolios.

Backend service:
Supabase

Tasks:

6. Database Schema

Create tables for:

users
portfolios
positions
orders
trades

Define relationships between tables.

7. Persistence Layer

Create services that save and load:

- orders
- trades
- positions
- portfolios


--------------------------------------------------
PHASE 4 — USER ACCOUNT SYSTEM
--------------------------------------------------

Goal:
Allow multiple users to use the platform.

Tasks:

8. Authentication
   - Integrate Supabase authentication
   - Support user registration
   - Support login

9. Portfolio Ownership
   - Each user can create portfolios
   - Each portfolio stores positions and trades


--------------------------------------------------
PHASE 5 — API LAYER
--------------------------------------------------

Goal:
Expose system functionality through an API.

Tasks:

10. Backend API

Create endpoints for:

- place order
- cancel order
- get positions
- get trade history
- get portfolio summary

Use a Python web framework if needed.

Examples:
FastAPI or Flask.


--------------------------------------------------
PHASE 6 — PYTHON TRADING SDK
--------------------------------------------------

Goal:
Allow users to write trading scripts.

Tasks:

11. Python Client SDK

Provide a Python package that wraps the API.

Example usage:

client.place_order("AAPL", qty=10, side="buy")

Functions include:

- place_order
- cancel_order
- get_positions
- get_account


--------------------------------------------------
PHASE 7 — WEB DASHBOARD
--------------------------------------------------

Goal:
Provide a browser interface for users.

Tasks:

12. Frontend Dashboard

Features:

- portfolio overview
- position table
- trade history
- performance charts

Suggested stack:

React
or other modern web framework.


--------------------------------------------------
PHASE 8 — ADVANCED FEATURES
--------------------------------------------------

Future improvements:

13. Limit Orders
14. Stop Orders
15. Portfolio analytics
16. Strategy backtesting
17. WebSocket live price updates
18. Real-time PnL tracking


--------------------------------------------------
DEVELOPMENT PRINCIPLES

Always follow these principles:

- Keep modules small and modular
- Separate frontend, backend, and trading logic
- Avoid tight coupling between components
- Write clear comments explaining architecture
- Prefer simple implementations first