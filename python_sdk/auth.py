"""Authentication module for the SDK."""

from __future__ import annotations

from typing import Any
from python_sdk.utils.http_client import HTTPClient, HTTPError


class AuthError(Exception):
    """Exception raised for authentication errors."""

    pass


class AuthToken:
    """Represents an authentication token."""

    def __init__(
        self,
        access_token: str,
        token_type: str = "bearer",
        expires_in: int | None = None,
        user_id: str | None = None,
        email: str | None = None,
    ):
        """Initialize AuthToken.

        Args:
            access_token: JWT access token.
            token_type: Token type (default: "bearer").
            expires_in: Token expiration time in seconds.
            user_id: User ID associated with token.
            email: User email associated with token.
        """
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in
        self.user_id = user_id
        self.email = email

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> "AuthToken":
        """Create AuthToken from login response.

        Args:
            data: Response data from login endpoint.

        Returns:
            AuthToken instance.
        """
        return cls(
            access_token=data.get("access_token"),
            token_type=data.get("token_type", "bearer"),
            expires_in=data.get("expires_in"),
            user_id=data.get("user_id"),
            email=data.get("email"),
        )


class AuthService:
    """Service for handling authentication operations."""

    def __init__(self, http_client: HTTPClient):
        """Initialize AuthService.

        Args:
            http_client: HTTPClient instance for making requests.
        """
        self.http_client = http_client

    def register(self, email: str, password: str) -> dict[str, Any]:
        """Register a new user.

        Args:
            email: User email.
            password: User password.

        Returns:
            Registration response with user_id and email.

        Raises:
            AuthError: If registration fails.
        """
        try:
            response = self.http_client.post(
                "/auth/register", {"email": email, "password": password}
            )
            return response
        except HTTPError as e:
            raise AuthError(f"Registration failed: {e.message}") from e

    def login(self, email: str, password: str) -> AuthToken:
        """Login user and obtain access token.

        Args:
            email: User email.
            password: User password.

        Returns:
            AuthToken with access_token and user info.

        Raises:
            AuthError: If login fails.
        """
        try:
            response = self.http_client.post(
                "/auth/login", {"email": email, "password": password}
            )
            return AuthToken.from_response(response)
        except HTTPError as e:
            raise AuthError(f"Login failed: {e.message}") from e
