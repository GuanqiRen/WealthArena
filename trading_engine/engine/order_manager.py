"""Order validation and configuration-driven execution policy checks."""

from __future__ import annotations

import os
import re
import time
import uuid
from pathlib import Path
from typing import Any

from trading_engine.models.order import Order


class OrderValidationError(Exception):
    """Raised when order data or execution policy validation fails."""


class OrderManager:
    _SYMBOL_PATTERN = re.compile(r"^[A-Z][A-Z0-9.\-]{0,9}$")

    def __init__(self, config_path: str | None = None) -> None:
        self._config_path = (
            Path(config_path)
            if config_path
            else Path(__file__).resolve().parents[1] / "config" / "trading_engine_config.yaml"
        )
        self._enable_short_selling = self._load_short_selling_flag()

    @property
    def enable_short_selling(self) -> bool:
        return self._enable_short_selling

    def create_order(self, symbol: str, quantity: int, side: str) -> Order:
        normalized_symbol = self._normalize_symbol(symbol)
        normalized_side = self._normalize_side(side)
        normalized_qty = self._normalize_quantity(quantity)

        return Order(
            order_id=str(uuid.uuid4()),
            symbol=normalized_symbol,
            quantity=normalized_qty,
            side=normalized_side,
            timestamp_ms=int(time.time() * 1000),
            status="pending",
        )

    def validate_execution(self, order: Order, current_quantity: int) -> str | None:
        if order.side == "sell" and not self._enable_short_selling and order.quantity > current_quantity:
            return (
                f"Short selling is disabled. Cannot sell {order.quantity} {order.symbol} "
                f"with current position {current_quantity}."
            )
        return None

    def _normalize_symbol(self, symbol: str) -> str:
        normalized = symbol.strip().upper()
        if not normalized or not self._SYMBOL_PATTERN.fullmatch(normalized):
            raise OrderValidationError(
                f"Invalid symbol '{symbol}'. Use 1-10 chars: A-Z, 0-9, '.', '-'."
            )
        return normalized

    def _normalize_side(self, side: str) -> str:
        normalized = side.strip().lower()
        if normalized not in {"buy", "sell"}:
            raise OrderValidationError("side must be 'buy' or 'sell'.")
        return normalized

    def _normalize_quantity(self, quantity: int) -> int:
        if not isinstance(quantity, int) or quantity <= 0:
            raise OrderValidationError("quantity must be a positive integer.")
        return quantity

    def _load_short_selling_flag(self) -> bool:
        env_value = os.getenv("ORDER_MANAGER_ENABLE_SHORT_SELLING")
        if env_value is not None:
            return self._parse_bool(env_value, source="ORDER_MANAGER_ENABLE_SHORT_SELLING")

        if not self._config_path.exists():
            return False

        value = self._load_flag_from_yaml(self._config_path)
        if value is None:
            return False
        return self._parse_bool(str(value), source=str(self._config_path))

    def _load_flag_from_yaml(self, path: Path) -> Any | None:
        text = path.read_text(encoding="utf-8")
        try:
            import yaml  # type: ignore

            data = yaml.safe_load(text) or {}
            if not isinstance(data, dict):
                return None
            section = data.get("order_manager", {})
            if not isinstance(section, dict):
                return None
            return section.get("enable_short_selling")
        except ImportError:
            in_order_manager = False
            for raw in text.splitlines():
                line = raw.split("#", 1)[0].rstrip()
                if not line.strip():
                    continue
                if line.strip() == "order_manager:":
                    in_order_manager = True
                    continue
                if in_order_manager and line.startswith("  enable_short_selling:"):
                    return line.split(":", 1)[1].strip()
            return None

    def _parse_bool(self, value: str, source: str) -> bool:
        normalized = value.strip().lower()
        if normalized in {"true", "1", "yes", "on"}:
            return True
        if normalized in {"false", "0", "no", "off"}:
            return False
        raise OrderValidationError(
            f"Invalid boolean value '{value}' from {source} for enable_short_selling."
        )
