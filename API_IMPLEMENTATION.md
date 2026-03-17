"""
PHASE 5: API Layer — Implementation Summary

The REST API has been fully implemented using FastAPI, providing endpoints for:
- User authentication (register, login)
- Portfolio management (create, list, delete)
- Trading operations (place orders, retrieve positions and trades)

=================================================================
PROJECT STRUCTURE
=================================================================

backend/
  api/
    main.py                      # FastAPI app with middleware and route registration
    __init__.py                  # Package exports
    dependencies/
      auth.py                    # JWT token extraction and validation
      __init__.py
    routes/
      auth_routes.py            # POST /auth/register, POST /auth/login
      portfolio_routes.py       # POST /portfolios, GET /portfolios, DELETE /portfolios/{id}
      trading_routes.py         # POST /trading/orders, GET /trading/positions, GET /trading/trades
      __init__.py
  services/
    trading_service.py          # Orchestrates trading engine + persistence

=================================================================
KEY FEATURES
=================================================================

1. **Authentication & Security**
   - JWT-based auth using Supabase credentials
   - HTTPBearer security scheme extracts token from Authorization header
   - All portfolio and trading endpoints require valid JWT

2. **Portfolio Management**
   - Users can create multiple portfolios
   - Ownership enforced: users can only see/delete their own
   - Portfolios are unique per user/name combination

3. **Trading Operations**
   - Market orders (buy/sell)
   - Order persistence with trade history
   - Position tracking with average cost basis
   - All operations tied to specific portfolios

4. **API Endpoints**

   Authentication:
     POST   /auth/register               Register new user
     POST   /auth/login                  Authenticate and get JWT

   Portfolio:
     POST   /portfolios                  Create portfolio
     GET    /portfolios                  List user's portfolios
     DELETE /portfolios/{portfolio_id}   Delete a portfolio

   Trading:
     POST   /trading/orders              Place a market order
     GET    /trading/positions?portfolio_id=... Retrieve positions
     GET    /trading/trades?portfolio_id=...    Retrieve trades
     GET    /trading/orders?portfolio_id=...    Retrieve orders

   Health:
     GET    /health                      Health check

=================================================================
REQUEST/RESPONSE MODELS (Pydantic)
=================================================================

Auth:
  RegisterRequest: { email, password }
  LoginRequest: { email, password }
  AuthResponse: { user_id, email, access_token, token_type, expires_in }

Portfolio:
  PortfolioRequest: { name }
  PortfolioResponse: { id, user_id, name, created_at }

Trading:
  PlaceOrderRequest: { portfolio_id, symbol, quantity, side }
  OrderResponse: { order_id, symbol, quantity, side, status, timestamp_ms }
  TradeResponse: { trade_id, symbol, quantity, execution_price, timestamp_ms }
  PositionResponse: { symbol, quantity, average_price }
  PlaceOrderResponse: { order, trade, position, status }

=================================================================
AUTHENTICATED REQUEST EXAMPLE
=================================================================

After login, include JWT in all protected requests:

  curl -H "Authorization: Bearer <access_token>" \\
       -X GET http://localhost:8000/portfolios

Or with Python:

  headers = {"Authorization": f"Bearer {access_token}"}
  response = client.get("/portfolios", headers=headers)

=================================================================
RUNNING THE API
=================================================================

1. Start the server:
   PYTHONPATH=. python -m uvicorn backend.api.main:app --reload

2. Access the interactive API docs:
   http://localhost:8000/docs (Swagger UI)
   http://localhost:8000/redoc (ReDoc)

3. Run the demo:
   PYTHONPATH=. python examples/api_demo.py

=================================================================
REQUEST/RESPONSE FLOW
=================================================================

Routes (thin, validation only)
   ↓
Services (business logic, orchestration)
   ↓
Repositories (data persistence)
   ↓
Database (Supabase Postgres with RLS)

This layering keeps concerns separated:
- Routes: HTTP marshaling
- Services: business rules
- Repositories: data access patterns
- Database: persistence + enforced security

=================================================================
SECURITY & ACCESS CONTROL
=================================================================

1. **JWT Authentication**
   - All protected endpoints require valid JWT from Supabase Auth
   - Token extracted from Authorization: Bearer <token> header
   - Invalid/expired tokens return 401 Unauthorized

2. **Portfolio Ownership**
   - Validated in PortfolioService.get_portfolio()
   - Users can only access/delete portfolios they own
   - Violating this returns 403 Forbidden

3. **Database Row-Level Security (RLS)**
   - Tables: portfolios, positions, orders, trades
   - Policies enforce auth.uid() = user_id at the database layer
   - Additional defense-in-depth for trading operations

=================================================================
DEPENDENCIES INSTALLED
=================================================================

- fastapi          # Web framework
- uvicorn          # ASGI server
- pydantic         # Data validation
- email-validator  # Email validation
- httpx            # HTTP client (for TestClient)

All available in the .venv via pip install
"""
