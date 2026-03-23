Implement Real-Time Updates (WebSocket + Live Portfolio Data).

Goal:
Add real-time updates to the dashboard so that positions, prices, and portfolio performance update automatically without refreshing the page.

The dashboard remains READ-ONLY.


Current System State

- Backend API (FastAPI or Flask)
- Supabase authentication + database
- Market Data module (Massive API)
- Price Cache Service
- Trading Engine
- Next.js read-only dashboard


Objectives

1. Stream live price updates from backend to frontend
2. Update positions in real time using latest prices
3. Compute and display live PnL
4. Avoid excessive polling (use WebSocket instead)


Architecture

Frontend (Next.js)
        ↓ WebSocket
Backend API (FastAPI)
        ↓
Price Cache + Market Data (Massive API)


Backend Requirements

1. WebSocket Endpoint

Create a WebSocket endpoint:

/ws/portfolio/{portfolio_id}

Responsibilities:

- accept client connection
- authenticate user via token
- verify portfolio ownership
- push updates at regular intervals (e.g., every 1–3 seconds)


2. Data to Stream

Each update should include:

- symbol
- latest price
- position quantity
- average price
- unrealized PnL

Example payload:

{
  "positions": [
    {
      "symbol": "AAPL",
      "price": 185.20,
      "quantity": 10,
      "average_price": 180,
      "pnl": 52
    }
  ]
}


3. Price Updates

- Use Price Cache to get latest prices
- Do NOT call external API directly on every tick
- Ensure efficient updates


4. PnL Calculation

For each position:

pnl = (current_price - average_price) * quantity


Frontend Requirements

1. WebSocket Client

Create a WebSocket connection when user opens:

/portfolio/[id]

Connect to:

ws://<backend>/ws/portfolio/{portfolio_id}

2. State Updates

- Store incoming data in React state
- Update UI automatically on message


3. UI Integration

Update:

- PositionsTable → show live price + PnL
- Portfolio summary → show total PnL

Highlight changes if possible (optional).


4. Cleanup

- Close WebSocket on page unmount
- Reconnect on failure (basic retry logic)


Directory Changes

Backend:

backend/
    api/
        websocket/
            portfolio_ws.py

Frontend:

frontend/
    hooks/
        useWebSocket.ts


Implementation Workflow

Before writing code:

1. Explain WebSocket architecture.
2. Explain how authentication works over WebSocket.
3. Explain how PnL is calculated and updated.

Then implement step by step:

Backend:
- WebSocket endpoint
- price streaming logic

Frontend:
- WebSocket hook
- integrate into portfolio page
- update UI components


Design Rules

- Do NOT break existing REST API
- Keep WebSocket logic separate from REST routes
- Avoid unnecessary API calls
- Keep updates efficient and lightweight


Success Criteria

- Portfolio page updates automatically without refresh
- Prices update in near real-time
- PnL updates correctly
- No excessive API calls
- WebSocket connection is stable


Nice to Have (Optional)

- Reconnect logic on disconnect
- Visual indicators for price changes (green/red)
- Throttling updates for performance