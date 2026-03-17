Implement PHASE 5 — API Layer from MASTER_TASKS.md.

Goal:
Expose the trading platform functionality through a backend API so that clients (frontend dashboard and Python SDK) can interact with the system.

The API must integrate with:
- Supabase authentication
- Repository layer
- Trading engine
- Portfolio ownership system


Current System State

The system already includes:

- Market Data module (Massive API)
- Price Cache Service
- Trading Engine (orders, trades, positions)
- Supabase database with RLS
- Repository layer
- User authentication (Supabase Auth)
- Portfolio ownership system


Objectives

1. Build a backend API server.
2. Expose endpoints for trading and portfolio management.
3. Enforce authentication and user access control.
4. Connect API endpoints to services and trading engine.


Technology Choice

Use Python and a modern API framework.

Recommended:
- FastAPI (preferred)
or
- Flask

Use FastAPI unless there is a strong reason not to.


Directory Structure

Create the following structure:

backend/
    api/
        main.py
        routes/
            auth_routes.py
            portfolio_routes.py
            trading_routes.py
        dependencies/
            auth.py
    services/
        trading_service.py
        portfolio_service.py


API Endpoints

Implement the following endpoints:


Authentication (if needed wrapper)

POST /register
POST /login


Portfolio

POST /portfolios
GET /portfolios
DELETE /portfolios/{portfolio_id}


Trading

POST /orders
    body:
    {
        "portfolio_id": "...",
        "symbol": "AAPL",
        "quantity": 10,
        "side": "buy"
    }

GET /positions?portfolio_id=...

GET /trades?portfolio_id=...


Authentication & Security

- Use Supabase JWT tokens for authentication.
- Extract user identity from request headers.
- Validate user using auth.uid() equivalent logic.

All endpoints must enforce:

- user must be authenticated
- user can only access their own portfolios


Dependency Layer

Create an auth dependency that:

- reads JWT token from request
- validates it using Supabase
- extracts user_id
- injects user_id into route handlers


Service Layer

Do NOT call repositories directly from API routes.

Instead:

Routes → Services → Repositories → Database

TradingService should:

- call trading engine
- persist results using repositories

PortfolioService should:

- validate ownership
- manage portfolios


Integration with Trading Engine

When placing an order:

1. Validate portfolio ownership
2. Call trading engine
3. Persist:
   - order
   - trade
   - updated position


Implementation Workflow

Before writing code:

1. Propose the full API structure.
2. Explain authentication flow.
3. Explain request lifecycle (API → Service → Engine → Repository).

Then implement:

- main.py
- auth dependency
- routes
- services


Design Rules

- Keep routes thin (no business logic)
- Put logic in service layer
- Keep trading engine independent
- Use clear request/response models


Success Criteria

- API server runs successfully
- Endpoints are accessible
- Authentication works
- Users can:
  - create portfolios
  - place orders
  - retrieve positions and trades
- Access control is enforced correctly