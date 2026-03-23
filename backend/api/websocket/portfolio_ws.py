"""WebSocket endpoint for realtime portfolio position updates."""

from __future__ import annotations

import asyncio
import time
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from backend.services.auth_service import AuthService, AuthError
from backend.services.portfolio_service import (
    PortfolioService,
    PortfolioAccessDeniedError,
    PortfolioNotFoundError,
)
from backend.services.trading_service import TradingService
from market_data.cache.price_cache import PriceCacheError

router = APIRouter(tags=["websocket"])

_STREAM_INTERVAL_SECONDS = 2


def _extract_token(websocket: WebSocket) -> str | None:
    token = websocket.query_params.get("token")
    if token:
        return token

    auth_header = websocket.headers.get("authorization")
    if not auth_header:
        return None

    if auth_header.lower().startswith("bearer "):
        return auth_header.split(" ", 1)[1]
    return None


@router.websocket("/ws/portfolio/{portfolio_id}")
async def portfolio_updates(websocket: WebSocket, portfolio_id: str) -> None:
    token = _extract_token(websocket)
    if not token:
        await websocket.close(code=1008, reason="Missing auth token")
        return

    auth_service = AuthService()
    portfolio_service = PortfolioService()
    trading_service = TradingService()
    price_cache = getattr(websocket.app.state, "price_cache", None)

    if price_cache is None:
        await websocket.close(code=1011, reason="Price cache not initialized")
        return

    try:
        auth_user = auth_service.get_current_user(token)
    except AuthError:
        await websocket.close(code=1008, reason="Invalid or expired token")
        return

    try:
        portfolio_service.get_portfolio(portfolio_id, auth_user.id)
    except (PortfolioNotFoundError, PortfolioAccessDeniedError):
        await websocket.close(code=1008, reason="Portfolio access denied")
        return
    except Exception:
        await websocket.close(code=1011, reason="Portfolio lookup failure")
        return

    await websocket.accept()

    try:
        while True:
            positions = trading_service.get_positions(portfolio_id)
            payload_positions: list[dict[str, float | int | str]] = []
            total_pnl = 0.0

            for position in positions:
                symbol = str(position.get("symbol", "")).upper()
                quantity = int(position.get("quantity", 0))
                average_price = float(position.get("average_price", 0.0))

                if not symbol:
                    continue

                try:
                    current_price = float(price_cache.get_price(symbol))
                except PriceCacheError:
                    # Skip symbols that cannot be priced; keep stream alive.
                    continue

                pnl = (current_price - average_price) * quantity
                total_pnl += pnl
                payload_positions.append(
                    {
                        "symbol": symbol,
                        "price": current_price,
                        "quantity": quantity,
                        "average_price": average_price,
                        "pnl": pnl,
                    }
                )

            await websocket.send_json(
                {
                    "portfolio_id": portfolio_id,
                    "positions": payload_positions,
                    "total_pnl": total_pnl,
                    "timestamp_ms": int(time.time() * 1000),
                }
            )
            await asyncio.sleep(_STREAM_INTERVAL_SECONDS)
    except WebSocketDisconnect:
        return
    except Exception:
        await websocket.close(code=1011, reason="Streaming failure")
