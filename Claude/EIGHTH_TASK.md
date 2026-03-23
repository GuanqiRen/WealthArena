Implement PHASE 7 — Read-Only Web Dashboard using Next.js (App Router).

Goal:
Build a browser-based dashboard that allows users to view their trading data.

This dashboard is strictly READ-ONLY.

Users should be able to:

- log in
- view their portfolios
- view positions
- view trade history
- monitor basic portfolio performance

Do NOT implement:
- order placement
- portfolio creation
- portfolio deletion


Current System State

The backend is complete and includes:

- API layer (FastAPI or Flask)
- Supabase authentication
- Trading engine
- Portfolio system
- Database persistence


Technology Requirements

Use:

- Next.js (latest version, App Router)
- React (built into Next.js)
- TypeScript (preferred)


Project Structure

frontend/
    app/
        login/
            page.tsx
        dashboard/
            page.tsx
        portfolio/
            [id]/
                page.tsx
        layout.tsx
        page.tsx

    components/
        PortfolioList.tsx
        PortfolioCard.tsx
        PositionsTable.tsx
        TradesTable.tsx
        Navbar.tsx

    lib/
        api.ts
        auth.ts

    context/
        AuthContext.tsx


Core Features

1. Authentication

- Login page (/login)
- Call backend login endpoint
- Store JWT token
- Attach token to API requests
- Protect all routes except /login
- Redirect unauthenticated users to /login


2. Dashboard (Portfolio List)

- Display all user portfolios
- Each portfolio is clickable
- Navigate to /portfolio/{id}


3. Portfolio Detail Page

On /portfolio/{id} display:

- Positions table
- Trade history table


4. Positions Table

Display:

- symbol
- quantity
- average price


5. Trades Table

Display:

- symbol
- quantity
- execution price
- timestamp


6. Portfolio Summary (Basic)

Display:

- total number of positions
- optional simple PnL (if API provides it)


API Integration

Create a centralized API module:

lib/api.ts

Only include read-only endpoints:

login()
get_portfolios()
get_positions(portfolio_id)
get_trades(portfolio_id)

The API layer should:

- attach JWT token to requests
- handle errors cleanly


Auth Handling

Use AuthContext to manage:

- authentication state
- token
- login/logout

Provide a hook:

useAuth()


Routing (Next.js App Router)

- /login → login page
- /dashboard → portfolio list
- /portfolio/[id] → portfolio detail


Navigation

- Add a simple Navbar
- Include:
  - Dashboard link
  - Logout button


Design Requirements

- Keep components modular
- Separate UI from API logic
- Keep code clean and readable
- Use simple styling (Tailwind optional)


Implementation Workflow

Before writing code:

1. Propose frontend architecture.
2. Show file structure.
3. Explain authentication flow.
4. Explain API integration.

Then implement step by step:

1. Next.js setup
2. API module
3. Auth context
4. Login page
5. Dashboard page
6. Portfolio detail page
7. Components


Success Criteria

- Frontend runs successfully
- User can log in
- User can:
  - view portfolios
  - view positions
  - view trades

- Routes are protected
- API integration works correctly
- UI is clean and responsive


Nice to Have (Optional)

- Loading states
- Error handling UI
- Basic styling improvements