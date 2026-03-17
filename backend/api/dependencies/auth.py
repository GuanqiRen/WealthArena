"""API dependency for extracting and validating JWT from requests."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from backend.services.auth_service import AuthService, AuthError

security = HTTPBearer()


class AuthUser:
    """Represents an authenticated user extracted from JWT."""

    def __init__(self, user_id: str, email: str) -> None:
        self.user_id = user_id
        self.email = email


async def get_current_user(credential: HTTPAuthorizationCredentials = Depends(security)) -> AuthUser:
    """Extract and validate JWT token from Authorization header.

    Raises HTTPException 401 if token is invalid or missing.
    """
    token = credential.credentials
    auth_service = AuthService()

    try:
        user = auth_service.get_current_user(token)
        return AuthUser(user_id=user.id, email=user.email)
    except AuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {exc}",
        ) from exc
