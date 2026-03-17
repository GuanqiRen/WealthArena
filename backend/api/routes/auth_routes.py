"""Auth routes for user registration and login."""

from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, EmailStr
from fastapi import APIRouter, HTTPException, status

from backend.services.auth_service import AuthService, AuthError

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    """Request body for user registration."""

    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    """Request body for user login."""

    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    """Response after successful registration or login."""

    user_id: str
    email: str
    access_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: Optional[int] = None


@router.post("/register", response_model=AuthResponse)
async def register(req: RegisterRequest) -> AuthResponse:
    """Register a new user.

    On success, returns user_id and email.
    Use login endpoint to get access_token.
    """
    auth = AuthService()

    try:
        user = auth.register_user(req.email, req.password)
        return AuthResponse(user_id=user.id, email=user.email)
    except AuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.post("/login", response_model=AuthResponse)
async def login(req: LoginRequest) -> AuthResponse:
    """Authenticate user and return JWT access token."""
    auth = AuthService()

    try:
        token = auth.login_user(req.email, req.password)
        return AuthResponse(
            user_id=token.user["id"],
            email=token.user.get("email", ""),
            access_token=token.access_token,
            token_type=token.token_type,
            expires_in=token.expires_in,
        )
    except AuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        ) from exc
