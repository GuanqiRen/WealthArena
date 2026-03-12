Implement PHASE 4 — User Account System from MASTER_TASKS.md.

Goal:
Add a user account system so multiple users can use the paper trading platform and manage their own portfolios.

Authentication and user management should be implemented using Supabase Auth.


Current System State

The system already includes:

- Market Data module
- Price Cache
- Paper Trading Engine
- Database Persistence layer
- Supabase PostgreSQL database
- Repository layer for orders, trades, positions, and portfolios


Objectives

1. Enable user registration and login.
2. Associate portfolios with specific users.
3. Ensure all trading activity belongs to a user's portfolio.


Authentication System

Use Supabase Auth for:

- user registration
- login
- authentication tokens

The authentication flow should support:

register(email, password)
login(email, password)


Database Integration

Use the Supabase Auth users table as the primary user identity.

Link portfolios to users using:

portfolios.user_id → users.id → auth.users.id


Portfolio Ownership Rules

- Each user can create multiple portfolios.
- Each portfolio belongs to exactly one user.
- Users can only access their own portfolios.
- Trades, orders, and positions must belong to a portfolio.


Directory Structure

Add new services for account and portfolio management.

backend/
    services/
        auth_service.py
        portfolio_service.py
    repositories/
        user_repository.py
        portfolio_repository.py


User Repository

Responsible for retrieving user information from Supabase.

Example functions:

get_user_by_id(user_id)
get_user_by_email(email)


Auth Service

Responsible for authentication operations.

Functions include:

register_user(email, password)
login_user(email, password)
get_current_user(token)


Portfolio Service

Responsible for portfolio operations tied to a user.

Functions include:

create_portfolio(user_id, name)
delete_portfolio(portfolio_id)
get_user_portfolios(user_id)


Access Control Rules

Ensure the system validates:

- users can only modify their own portfolios
- trading engine operations require a portfolio_id that belongs to the user


Integration with Trading Engine

Update the trading engine so that:

- orders require a portfolio_id
- trades are associated with that portfolio
- positions belong to that portfolio


Implementation Workflow

Before writing code:

1. Explain how Supabase Auth works in this architecture.
2. Show the updated database relationships.
3. Propose file structure changes.

Then implement code step by step.


Security Rules

- Do not store plaintext passwords.
- Rely on Supabase Auth for credential management.
- Validate user identity before allowing portfolio operations.


Success Criteria

- Users can register and log in.
- Users can create and delete portfolios.
- Each portfolio belongs to a specific user.
- Trading engine operations require a valid portfolio.
- Data access respects user ownership rules.