"""FastAPI application for WealthArena trading platform."""

from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from market_data.cache.price_cache import PriceCache

from backend.api.routes import auth_routes, portfolio_routes, trading_routes
from backend.api.websocket import portfolio_ws

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize shared runtime services."""
    app.state.price_cache = PriceCache()
    yield

# Create FastAPI app
app = FastAPI(
    title="WealthArena API",
    description="REST API for paper trading platform",
    version="0.1.0",
    lifespan=lifespan,
)

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth_routes.router)
app.include_router(portfolio_routes.router)
app.include_router(trading_routes.router)
app.include_router(portfolio_ws.router)


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
