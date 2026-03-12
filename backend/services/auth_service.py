"""Authentication service using Supabase Auth REST API.

Supabase Auth endpoints used:
    POST /auth/v1/signup          — register a new user
    POST /auth/v1/token           — login, returns access + refresh tokens
    GET  /auth/v1/user            — get the currently authenticated user from their token

Environment:
    SUPABASE_URL             — e.g. https://<ref>.supabase.co
    SUPABASE_PUBLISHABLE_KEY — publishable key (sufficient for signup and login)
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class AuthError(Exception):
    """Raised when authentication operations fail."""


@dataclass
class AuthToken:
    """Holds tokens returned by Supabase Auth after a successful login."""

    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    user: dict[str, Any]


@dataclass
class AuthUser:
    """Represents a Supabase Auth user."""

    id: str
    email: str
    raw: dict[str, Any]


class AuthService:
    """Wraps Supabase Auth REST endpoints for registration and login."""

    def __init__(
        self,
        supabase_url: str | None = None,
        supabase_key: str | None = None,
    ) -> None:
        url = (supabase_url or os.getenv("SUPABASE_URL") or "").rstrip("/")
        key = (
            supabase_key
            or os.getenv("SUPABASE_PUBLISHABLE_KEY")
            or os.getenv("SUPABASE_KEY")  # legacy fallback
            or ""
        )

        if not url:
            raise AuthError("Missing SUPABASE_URL environment variable.")
        if not key:
            raise AuthError("Missing SUPABASE_PUBLISHABLE_KEY environment variable.")

        self._auth_url = f"{url}/auth/v1"
        self._key = key

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def register_user(self, email: str, password: str) -> AuthUser:
        """Register a new user with email and password.

        Returns the created AuthUser on success.
        Raises AuthError if registration fails (e.g. email already in use).
        """
        payload = {"email": email, "password": password}
        data = self._request("POST", "/signup", payload=payload)
        return self._parse_user(data)

    def login_user(self, email: str, password: str) -> AuthToken:
        """Authenticate a user and return tokens.

        Returns an AuthToken containing the access_token (JWT) and user info.
        Raises AuthError on invalid credentials.
        """
        payload = {"email": email, "password": password}
        data = self._request(
            "POST",
            "/token",
            payload=payload,
            query_params={"grant_type": "password"},
        )
        return AuthToken(
            access_token=data["access_token"],
            refresh_token=data.get("refresh_token", ""),
            token_type=data.get("token_type", "bearer"),
            expires_in=data.get("expires_in", 3600),
            user=data.get("user", {}),
        )

    def get_current_user(self, access_token: str) -> AuthUser:
        """Resolve a JWT access token to the authenticated user.

        Raises AuthError if the token is invalid or expired.
        """
        data = self._request(
            "GET",
            "/user",
            extra_headers={"Authorization": f"Bearer {access_token}"},
        )
        return self._parse_user(data)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _parse_user(self, data: dict[str, Any]) -> AuthUser:
        user_id = data.get("id") or ""
        email = data.get("email") or ""
        if not user_id:
            raise AuthError(f"Unexpected Supabase Auth response: {data}")
        return AuthUser(id=user_id, email=email, raw=data)

    def _request(
        self,
        method: str,
        path: str,
        *,
        payload: dict[str, Any] | None = None,
        query_params: dict[str, str] | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        from urllib.parse import urlencode

        url = f"{self._auth_url}{path}"
        if query_params:
            url = f"{url}?{urlencode(query_params)}"

        headers: dict[str, str] = {
            "apikey": self._key,
            "Authorization": f"Bearer {self._key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if extra_headers:
            headers.update(extra_headers)

        request = Request(
            url,
            data=json.dumps(payload).encode() if payload is not None else None,
            headers=headers,
            method=method,
        )

        try:
            with urlopen(request, timeout=15) as response:
                body = response.read().decode("utf-8")
        except HTTPError as exc:
            message = exc.read().decode("utf-8", errors="replace") if hasattr(exc, "read") else ""
            raise AuthError(f"Supabase Auth error {exc.code}: {message}") from exc
        except URLError as exc:
            raise AuthError(f"Supabase Auth network failure: {exc.reason}") from exc
        except TimeoutError as exc:
            raise AuthError("Supabase Auth request timed out.") from exc

        try:
            return json.loads(body)
        except json.JSONDecodeError as exc:
            raise AuthError("Supabase Auth returned non-JSON response.") from exc
