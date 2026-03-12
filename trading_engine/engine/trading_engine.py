"""Trading engine orchestration for immediate market-order simulation."""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import replace

from market_data.cache.price_cache import PriceCache, PriceCacheError
from trading_engine.engine.order_manager import OrderManager, OrderValidationError
from trading_engine.engine.portfolio_manager import PortfolioManager
from trading_engine.models.order import Order
from trading_engine.models.position import Position
from trading_engine.models.trade import Trade


class TradingEngineError(Exception):
    """Raised for trading engine-level failures."""


class TradingEngine:
    """Places and executes immediate market orders using PriceCache prices."""

    def __init__(
        self,
        price_cache: PriceCache | None = None,
        order_manager: OrderManager | None = None,
        portfolio_manager: PortfolioManager | None = None,
    ) -> None:
        self._price_cache = price_cache or PriceCache()
        self._order_manager = order_manager or OrderManager()
        self._portfolio_manager = portfolio_manager or PortfolioManager()

        self._orders: list[Order] = []
        self._trades: list[Trade] = []
        self._lock = threading.Lock()

    def place_order(self, symbol: str, quantity: int, side: str) -> Order:
        try:
            pending_order = self._order_manager.create_order(symbol, quantity, side)
        except OrderValidationError as exc:
            raise TradingEngineError(str(exc)) from exc

        with self._lock:
            current_qty = self._portfolio_manager.get_position_quantity(pending_order.symbol)
            rejection = self._order_manager.validate_execution(pending_order, current_qty)
            if rejection:
                rejected = replace(pending_order, status="rejected", message=rejection)
                self._orders.append(rejected)
                return rejected

        try:
            execution_price = float(self._price_cache.get_price(pending_order.symbol))
        except PriceCacheError as exc:
            rejected = replace(
                pending_order,
                status="rejected",
                message=f"Price retrieval failed for {pending_order.symbol}: {exc}",
            )
            with self._lock:
                self._orders.append(rejected)
            return rejected
        except Exception as exc:
            raise TradingEngineError(f"Unexpected price retrieval failure: {exc}") from exc

        trade = Trade(
            trade_id=uuid.uuid4().hex,
            symbol=pending_order.symbol,
            quantity=pending_order.quantity,
            execution_price=execution_price,
            timestamp_ms=int(time.time() * 1000),
        )
        filled = replace(pending_order, status="filled")

        with self._lock:
            self._portfolio_manager.apply_fill(
                symbol=filled.symbol,
                quantity=filled.quantity,
                side=filled.side,
                execution_price=execution_price,
            )
            self._trades.append(trade)
            self._orders.append(filled)

        return filled

    def get_positions(self) -> list[Position]:
        with self._lock:
            return list(self._portfolio_manager.get_positions())

    def get_trade_history(self) -> list[Trade]:
        with self._lock:
            return list(self._trades)

    def get_order_history(self) -> list[Order]:
        with self._lock:
            return list(self._orders)

    def get_pnl(self) -> float:
        with self._lock:
            snapshot = list(self._portfolio_manager.get_positions())

        pnl = 0.0
        for position in snapshot:
            current_price = float(self._price_cache.get_price(position.symbol))
            pnl += (current_price - position.average_price) * position.quantity
        return pnl
