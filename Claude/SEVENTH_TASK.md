Implement PHASE 6 — Python Trading SDK from MASTER_TASKS.md.

Goal:
Build a Python SDK that allows users to interact with the trading platform API programmatically.

The SDK should feel like a real trading client library and provide a clean, easy-to-use interface.


Current System State

The system already includes:

- Market Data module
- Price Cache
- Trading Engine
- Supabase database with RLS
- User authentication system
- Backend API (FastAPI or Flask)


Objectives

1. Provide a Python client for the API.
2. Handle authentication and token management.
3. Expose simple methods for trading and portfolio operations.
4. Keep the SDK clean, modular, and easy to use.


Directory Structure

Create the following module:

python_sdk/
    __init__.py
    client.py
    auth.py
    endpoints/
        portfolio.py
        trading.py
    models/
        order.py
        position.py
        trade.py
    utils/
        http_client.py


Core Design

The SDK should expose a main client class:

TradingClient

Example usage:

from python_sdk.client import TradingClient

client = TradingClient(
    base_url="http://localhost:8000",
    email="user@example.com",
    password="password"
)

client.login()

client.create_portfolio("My Portfolio")

client.place_order(
    portfolio_id="...",
    symbol="AAPL",
    quantity=10,
    side="buy"
)

positions = client.get_positions(portfolio_id="...")


Authentication

- Use API login endpoint to obtain JWT token
- Store token inside the client
- Automatically attach token to all requests


HTTP Layer

Create a reusable HTTP client that:

- handles GET/POST requests
- attaches auth headers
- handles errors and retries
- parses JSON responses


Endpoints to Implement

Portfolio:

create_portfolio(name)
get_portfolios()
delete_portfolio(portfolio_id)

Trading:

place_order(portfolio_id, symbol, quantity, side)
get_positions(portfolio_id)
get_trades(portfolio_id)


Design Requirements

- Keep API calls encapsulated inside endpoint modules
- Keep client.py as the main user interface
- Separate concerns:
  - auth
  - http
  - endpoints

- Provide clear method names and arguments


Error Handling

- Raise meaningful Python exceptions
- Handle HTTP errors gracefully
- Validate inputs before making API calls


Implementation Workflow

Before writing code:

1. Propose SDK architecture.
2. Show file structure.
3. Explain how authentication is handled.

Then implement:

- http_client.py
- auth.py
- endpoint modules
- client.py


Success Criteria

- SDK can connect to the API
- Users can log in successfully
- Users can:
  - create portfolios
  - place orders
  - fetch positions and trades
- Code is modular and easy to extend


Nice to Have (Optional)

- Add type hints
- Add docstrings for all public methods
- Add simple retry logic for HTTP requests