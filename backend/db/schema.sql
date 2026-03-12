create extension if not exists pgcrypto;

create table if not exists users (
    id uuid primary key default gen_random_uuid(),
    email text not null unique,
    created_at timestamptz not null default timezone('utc', now())
);

create table if not exists portfolios (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references users(id) on delete cascade,
    name text not null,
    created_at timestamptz not null default timezone('utc', now()),
    unique (user_id, name)
);

create table if not exists positions (
    id uuid primary key default gen_random_uuid(),
    portfolio_id uuid not null references portfolios(id) on delete cascade,
    symbol text not null,
    quantity integer not null,
    average_price double precision not null,
    updated_at timestamptz not null default timezone('utc', now()),
    unique (portfolio_id, symbol)
);

create table if not exists orders (
    id uuid primary key,
    portfolio_id uuid not null references portfolios(id) on delete cascade,
    symbol text not null,
    quantity integer not null check (quantity > 0),
    side text not null check (side in ('buy', 'sell')),
    status text not null check (status in ('pending', 'filled', 'rejected')),
    created_at timestamptz not null default timezone('utc', now())
);

create table if not exists trades (
    id uuid primary key,
    portfolio_id uuid not null references portfolios(id) on delete cascade,
    symbol text not null,
    quantity integer not null check (quantity > 0),
    execution_price double precision not null,
    timestamp timestamptz not null default timezone('utc', now())
);

create index if not exists idx_portfolios_user_id on portfolios(user_id);
create index if not exists idx_positions_portfolio_id on positions(portfolio_id);
create index if not exists idx_orders_portfolio_id on orders(portfolio_id);
create index if not exists idx_trades_portfolio_id on trades(portfolio_id);
