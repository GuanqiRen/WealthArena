create extension if not exists pgcrypto;

create table if not exists portfolios (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references auth.users(id) on delete cascade,
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

alter table portfolios enable row level security;
alter table positions enable row level security;
alter table orders enable row level security;
alter table trades enable row level security;

drop policy if exists portfolios_select_own on portfolios;
create policy portfolios_select_own
on portfolios
for select
using (auth.uid() = user_id);

drop policy if exists portfolios_insert_own on portfolios;
create policy portfolios_insert_own
on portfolios
for insert
with check (auth.uid() = user_id);

drop policy if exists portfolios_update_own on portfolios;
create policy portfolios_update_own
on portfolios
for update
using (auth.uid() = user_id)
with check (auth.uid() = user_id);

drop policy if exists portfolios_delete_own on portfolios;
create policy portfolios_delete_own
on portfolios
for delete
using (auth.uid() = user_id);

drop policy if exists positions_select_own on positions;
create policy positions_select_own
on positions
for select
using (
    exists (
        select 1
        from portfolios p
        where p.id = positions.portfolio_id
          and p.user_id = auth.uid()
    )
);

drop policy if exists positions_insert_own on positions;
create policy positions_insert_own
on positions
for insert
with check (
    exists (
        select 1
        from portfolios p
        where p.id = positions.portfolio_id
          and p.user_id = auth.uid()
    )
);

drop policy if exists positions_update_own on positions;
create policy positions_update_own
on positions
for update
using (
    exists (
        select 1
        from portfolios p
        where p.id = positions.portfolio_id
          and p.user_id = auth.uid()
    )
)
with check (
    exists (
        select 1
        from portfolios p
        where p.id = positions.portfolio_id
          and p.user_id = auth.uid()
    )
);

drop policy if exists positions_delete_own on positions;
create policy positions_delete_own
on positions
for delete
using (
    exists (
        select 1
        from portfolios p
        where p.id = positions.portfolio_id
          and p.user_id = auth.uid()
    )
);

drop policy if exists orders_select_own on orders;
create policy orders_select_own
on orders
for select
using (
    exists (
        select 1
        from portfolios p
        where p.id = orders.portfolio_id
          and p.user_id = auth.uid()
    )
);

drop policy if exists orders_insert_own on orders;
create policy orders_insert_own
on orders
for insert
with check (
    exists (
        select 1
        from portfolios p
        where p.id = orders.portfolio_id
          and p.user_id = auth.uid()
    )
);

drop policy if exists orders_update_own on orders;
create policy orders_update_own
on orders
for update
using (
    exists (
        select 1
        from portfolios p
        where p.id = orders.portfolio_id
          and p.user_id = auth.uid()
    )
)
with check (
    exists (
        select 1
        from portfolios p
        where p.id = orders.portfolio_id
          and p.user_id = auth.uid()
    )
);

drop policy if exists orders_delete_own on orders;
create policy orders_delete_own
on orders
for delete
using (
    exists (
        select 1
        from portfolios p
        where p.id = orders.portfolio_id
          and p.user_id = auth.uid()
    )
);

drop policy if exists trades_select_own on trades;
create policy trades_select_own
on trades
for select
using (
    exists (
        select 1
        from portfolios p
        where p.id = trades.portfolio_id
          and p.user_id = auth.uid()
    )
);

drop policy if exists trades_insert_own on trades;
create policy trades_insert_own
on trades
for insert
with check (
    exists (
        select 1
        from portfolios p
        where p.id = trades.portfolio_id
          and p.user_id = auth.uid()
    )
);

drop policy if exists trades_update_own on trades;
create policy trades_update_own
on trades
for update
using (
    exists (
        select 1
        from portfolios p
        where p.id = trades.portfolio_id
          and p.user_id = auth.uid()
    )
)
with check (
    exists (
        select 1
        from portfolios p
        where p.id = trades.portfolio_id
          and p.user_id = auth.uid()
    )
);

drop policy if exists trades_delete_own on trades;
create policy trades_delete_own
on trades
for delete
using (
    exists (
        select 1
        from portfolios p
        where p.id = trades.portfolio_id
          and p.user_id = auth.uid()
    )
);
