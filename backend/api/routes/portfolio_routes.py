"""Portfolio routes for managing user portfolios."""

from __future__ import annotations

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status, Depends

from backend.api.dependencies import AuthUser, get_current_user
from backend.services.portfolio_service import (
    PortfolioService,
    PortfolioNotFoundError,
    PortfolioAccessDeniedError,
)

router = APIRouter(prefix="/portfolios", tags=["portfolios"])


class PortfolioRequest(BaseModel):
    """Request to create a portfolio."""

    name: str


class PortfolioResponse(BaseModel):
    """Portfolio data in responses."""

    id: str
    user_id: str
    name: str
    created_at: str | None = None


@router.post("", response_model=PortfolioResponse)
async def create_portfolio(
    req: PortfolioRequest,
    user: AuthUser = Depends(get_current_user),
) -> PortfolioResponse:
    """Create a new portfolio for the authenticated user."""
    service = PortfolioService()

    try:
        portfolio = service.create_portfolio(user_id=user.user_id, name=req.name)
        return PortfolioResponse(
            id=portfolio["id"],
            user_id=portfolio["user_id"],
            name=portfolio["name"],
            created_at=portfolio.get("created_at"),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get("", response_model=list[PortfolioResponse])
async def list_portfolios(
    user: AuthUser = Depends(get_current_user),
) -> list[PortfolioResponse]:
    """List all portfolios for the authenticated user."""
    service = PortfolioService()

    try:
        portfolios = service.get_user_portfolios(user.user_id)
        return [
            PortfolioResponse(
                id=p["id"],
                user_id=p["user_id"],
                name=p["name"],
                created_at=p.get("created_at"),
            )
            for p in portfolios
        ]
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc


@router.delete("/{portfolio_id}")
async def delete_portfolio(
    portfolio_id: str,
    user: AuthUser = Depends(get_current_user),
) -> dict:
    """Delete a portfolio if it belongs to the current user."""
    service = PortfolioService()

    try:
        service.delete_portfolio(portfolio_id, user.user_id)
        return {"message": "Portfolio deleted successfully"}
    except PortfolioNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Portfolio {portfolio_id} not found",
        )
    except PortfolioAccessDeniedError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not own this portfolio",
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
