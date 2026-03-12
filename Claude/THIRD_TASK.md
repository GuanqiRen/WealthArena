# THIRD TASK
Take a look at MASTER_TASKS.md which provide a clear roadmap for the entire project. We are implementing PHASE 2 here.

The next component to implement is the Paper Trading Engine.

This module simulates stock trading. It allows users to place simulated buy and sell orders using real-time market prices retrieved from the Market Data Cache Service.

The trading engine must update portfolio positions and record trade history. For the current task, only store the positions and trade histories in in-memory containers. Database for data persistance will be implemented in the following tasks.


# Objective

Build a trading engine capable of:

- placing buy orders
- placing sell orders
- simulating execution using the latest market price
- updating portfolio positions
- recording trade history


# Architecture

The trading engine must retrieve prices through the cache layer.

Trading Engine
      |
      v
Price Cache
      |
      v
Market Data Client
      |
      v
Massive API


# Core Responsibilities

The trading engine must support:

1. Place Buy Orders
2. Place Sell Orders
3. Execute Orders Immediately (market orders)
4. Update Portfolio Positions
5. Record Trade History


# Initial Scope

For the first version of the engine, support only:

Market Orders

Do NOT implement limit orders yet.


# Directory Structure

Create the following module:

trading_engine/
    __init__.py
    engine/
        trading_engine.py
        order_manager.py
        portfolio_manager.py
    models/
        order.py
        position.py
        trade.py
    config/
        trading_engine_config.yaml


# Data Models

Order should contain:

- order_id
- symbol
- quantity
- side (buy or sell)
- timestamp
- status


Position should contain:

- symbol
- quantity
- average_price


Trade should contain:

- trade_id
- symbol
- quantity
- execution_price
- timestamp

# Order Manager Behavior

The order manager should:

- check for short selling before execution
- enable short selling by configuration
- reject short selling and return clear message when short selling is disabled

Example configuration:

order_manager:
    enable_short_selling: True

# Portfolio Behavior

The portfolio manager should:

- maintain positions for each symbol
- update position quantity after trades
- calculate new average price after buys
- reduce position after sells

Example:

Buy 10 AAPL at 180
Buy 10 AAPL at 200

New position:

quantity = 20
average_price = 190


# Execution Logic

Orders should execute using the latest price from the Price Cache.

Example flow:

1. User places order
2. Trading engine requests price from Price Cache
3. Order executes immediately
4. Trade is recorded
5. Portfolio position updates


# Required Interface

The trading engine must expose functions:

place_order(symbol, quantity, side)

Example:

engine.place_order("AAPL", 10, "buy")


get_positions()

Returns current portfolio positions.


get_trade_history()

Returns executed trades.


# Example Usage

from trading_engine.engine.trading_engine import TradingEngine

engine = TradingEngine()

engine.place_order("AAPL", 10, "buy")

positions = engine.get_positions()

print(positions)

pnl = engine.get_pnl()

print(pnl)


# Implementation Requirements

The system must:

- maintain in-memory portfolio state
- maintain trade history
- generate unique IDs for orders and trades
- keep logic modular


# Implementation Workflow

Before writing code:

1. Explain the design of the trading engine.
2. Explain how OrderManager and PortfolioManager interact.
3. Explain how the Price Cache will be used.

Then implement the files step by step.


# Success Criteria

The task is complete when:

- orders can be placed successfully
- trades are recorded
- portfolio positions update correctly
- the trading engine retrieves prices from the Price Cache
- the code is modular and well documented