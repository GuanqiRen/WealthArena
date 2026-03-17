"""Trading routes for orders, positions, and trades."""

from __future__ import annotations

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status, Depends, Query

from backend.api.dependencies import AuthUser, get_current_user
from backend.services.portfolio_service import PortfolioService, PortfolioAccessDeniedError
from backend.services.trading_service import TradingService, TradingServiceError

router = APIRouter(prefix="/trading", tags=["trading"])


class PlaceOrderRequest(BaseModel):
    """Request to place a market order."""

    portfolio_id: str
    symbol: str
    quantity: int
    side: str  # "buy" or "sell"


class OrderResponse(BaseModel):
    """Order response data."""

    order_id: str
    symbol: str
    quantity: int
    side: str
    status: str
    timestamp_ms: int | None = None


class TradeResponse(BaseModel):
    """Trade response data."""

    trade_id: str
    symbol: str
    quantity: int
    execution_price: float
    timestamp_ms: int | None = None


class PositionResponse(BaseModel):
    """Position response data."""

    symbol: str
    quantity: int
    average_price: float


class PlaceOrderResponse(BaseModel):
    """Response after placing an order."""

    order: OrderResponse
    trade: TradeResponse | None = None
    position: PositionResponse | None = None
    status: str


def _validate_portfolio_access(
    portfolio_id: str, user: AuthUser
) -> None:
    """Verify that the portfolio belongs to the user."""
    service = PortfolioService()
    try:
        service.get_portfolio(portfolio_id, user.user_id)
    except PortfolioAccessDeniedError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not own this portfolio",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Portfolio not found: {exc}",
        ) from exc


@router.post("/orders", response_model=PlaceOrderResponse)
async def place_order(
    req: PlaceOrderRequest,
    user: AuthUser = Depends(get_current_user),
) -> PlaceOrderResponse:
    """Place a market order in a portfolio.

    Validates that the portfolio belongs to the user before executing.
    """
    # Verify ownership
    _validate_portfolio_access(req.portfolio_id, user)

    # Place order
    trading_service = TradingService()
    try:
        result = trading_service.place_order(
            portfolio_id=req.portfolio_id,
            symbol=req.symbol,
            quantity=req.quantity,
            side=req.side,
        )

        return PlaceOrderResponse(
            order=OrderResponse(
                order_id=result["order"].order_id,
                symbol=result["order"].symbol,
                quantity=result["order"].quantity,
                side=result["order"].side,
                status=result["order"].status,
                timestamp_ms=result["order"].timestamp_ms,
            ),
            trade=TradeResponse(
                trade_id=result["trade"].trade_id,
                symbol=result["trade"].symbol,
                quantity=result["trade"].quantity,
                execution_price=result["trade"].execution_price,
                timestamp_ms=result["trade"].timestamp_ms,
            ) if result["trade"] else None,
            position=PositionResponse(
                symbol=result["position"].symbol,
                quantity=result["position"].quantity,
                average_price=result["position"].average_price,
            ) if result["position"] else None,
            status=result["status"],
        )
    except TradingServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get("/positions", response_model=list[PositionResponse])
async def get_positions(
    portfolio_id: str = Query(..., description="Portfolio UUID"),
    user: AuthUser = Depends(get_current_user),
) -> list[PositionResponse]:
    """Get all positions in a portfolio."""
    _validate_portfolio_access(portfolio_id, user)

    trading_service = TradingService()
    try:
        positions = trading_service.get_positions(portfolio_id)
        return [
            PositionResponse(
                symbol=p["symbol"],
                quantity=p["quantity"],
                average_price=p["average_price"],
            )
            for p in positions
        ]
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc


@router.get("/trades", response_model=list[TradeResponse])
async def get_trades(
    portfolio_id: str = Query(..., description="Portfolio UUID"),
    user: AuthUser = Depends(get_current_user),
) -> list[TradeResponse]:
    """Get all trades in a portfolio."""
    _validate_portfolio_access(portfolio_id, user)

    trading_service = TradingService()
    try:
        trades = trading_service.get_trade_history(portfolio_id)
        return [
            TradeResponse(
                trade_id=t["id"],
                symbol=t["symbol"],
                quantity=t["quantity"],
                execution_price=t["execution_price"],
                timestamp_ms=t.get("timestamp_ms"),
            )
            for t in trades
        ]
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc


@router.get("/orders", response_model=list[OrderResponse])
async def get_orders(
    portfolio_id: str = Query(..., description="Portfolio UUID"),
    user: AuthUser = Depends(get_current_user),
) -> list[OrderResponse]:
    """Get all orders in a portfolio."""
    _validate_portfolio_access(portfolio_id, user)

    trading_service = TradingService()
    try:
        orders = trading_service.get_orders(portfolio_id)
        return [
            OrderResponse(
                order_id=o["id"],
                symbol=o["symbol"],
                quantity=o["quantity"],
                side=o["side"],
                status=o["status"],
                timestamp_ms=o.get("timestamp_ms"),
            )
            for o in orders
        ]
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
