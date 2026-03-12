Implement PHASE 3 — Database Persistence from MASTER_TASKS.md.

Goal:
Add persistent storage for users, portfolios, orders, trades, and positions using Supabase (PostgreSQL).

The current system already contains:
- Market Data module
- Price Cache
- Paper Trading Engine (orders, trades, positions in memory)

This phase should persist trading data in a Supabase database.


Requirements

1. Database Schema

Design a PostgreSQL schema with the following tables:

users
portfolios
positions
orders
trades

Relationships:

users
  └── portfolios

portfolios
  ├── positions
  ├── orders
  └── trades


Suggested fields:

users
- id (uuid)
- email
- created_at

portfolios
- id (uuid)
- user_id
- name
- created_at

positions
- id (uuid)
- portfolio_id
- symbol
- quantity
- average_price
- updated_at

orders
- id (uuid)
- portfolio_id
- symbol
- quantity
- side
- status
- created_at

trades
- id (uuid)
- portfolio_id
- symbol
- quantity
- execution_price
- timestamp


2. Directory Structure

Create a persistence layer separate from the trading engine.

backend/
    db/
        supabase_client.py
        schema.sql
    repositories/
        portfolio_repository.py
        order_repository.py
        trade_repository.py
        position_repository.py


3. Supabase Client

Create a Supabase client wrapper that:

- loads SUPABASE_URL from environment variables
- loads SUPABASE_KEY from environment variables
- provides a reusable client instance
- update .env.example to store related variables


4. Repository Layer

Implement repository classes responsible for database interaction.

PortfolioRepository
OrderRepository
TradeRepository
PositionRepository

Each repository should provide simple functions such as:

create_portfolio()
get_portfolio()
save_order()
save_trade()
update_position()
get_positions()


5. Integration with Trading Engine

Modify the trading engine so that:

- executed trades are saved to the database
- orders are saved
- portfolio positions are updated in the database


6. Implementation Workflow

Before writing code:

1. Explain the database design.
2. Show the full schema.sql.
3. Show the new directory structure.

Then implement code step by step.


7. Design Rules

- Keep the trading engine logic separate from database logic.
- All database operations should go through repositories.
- Do not tightly couple the trading engine to Supabase.


Success Criteria

- Database schema is created.
- Orders, trades, and positions persist to Supabase.
- Trading engine continues to function.
- Repository layer cleanly abstracts database operations.