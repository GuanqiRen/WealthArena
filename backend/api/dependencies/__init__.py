"""API dependencies."""

from backend.api.dependencies.auth import AuthUser, get_current_user

__all__ = ["AuthUser", "get_current_user"]
