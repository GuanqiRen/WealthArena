"""Repository for retrieving user information from Supabase Auth.

Uses the Supabase Auth Admin API which requires the secret key.

Environment:
    SUPABASE_URL        — e.g. https://<ref>.supabase.co
    SUPABASE_SECRET_KEY — secret key (Supabase → Settings → API → Secret key).
                          Required; the publishable key is insufficient for admin lookups.
"""

from __future__ import annotations

import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class UserRepositoryError(Exception):
    """Raised when user lookup operations fail."""


class UserRepository:
    """Reads user records from the Supabase Auth Admin API.

    The admin endpoints require the secret key, not the publishable key.
    Store it in the SUPABASE_SECRET_KEY environment variable.
    """

    def __init__(
        self,
        supabase_url: str | None = None,
        service_key: str | None = None,
    ) -> None:
        url = (supabase_url or os.getenv("SUPABASE_URL") or "").rstrip("/")
        key = (
            service_key
            or os.getenv("SUPABASE_SECRET_KEY")
            or os.getenv("SUPABASE_SERVICE_KEY")  # legacy fallback
            or ""
        )

        if not url:
            raise UserRepositoryError("Missing SUPABASE_URL environment variable.")
        if not key:
            raise UserRepositoryError(
                "Missing SUPABASE_SECRET_KEY environment variable."
            )

        self._admin_url = f"{url}/auth/v1/admin"
        self._key = key

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def get_user_by_id(self, user_id: str) -> dict[str, Any] | None:
        """Return the Supabase Auth user record for the given UUID, or None."""
        try:
            return self._request("GET", f"/users/{user_id}")
        except UserRepositoryError as exc:
            if "404" in str(exc):
                return None
            raise

    def get_user_by_email(self, email: str) -> dict[str, Any] | None:
        """Return the Supabase Auth user record matching the given email, or None.

        The Admin API returns a paginated list of all users. We request a large
        page and filter client-side. For most projects (< 1 000 users) this is
        fine; at scale you would manage a separate lookup table.
        """
        from urllib.parse import urlencode

        params = urlencode({"page": "1", "per_page": "1000"})
        data = self._request("GET", f"/users?{params}")

        users: list[dict[str, Any]] = data.get("users", []) if isinstance(data, dict) else []
        for user in users:
            if user.get("email", "").lower() == email.lower():
                return user
        return None

    def create_user(
        self,
        email: str,
        password: str,
        *,
        email_confirm: bool = True,
    ) -> dict[str, Any]:
        """Create a user via the Admin API, bypassing email confirmation.

        Use this for scripts and demos where sending a confirmation email is
        not desired.  ``email_confirm=True`` (the default) marks the address as
        already verified so the user can log in immediately.

        Returns the raw Supabase Auth user record.
        Raises UserRepositoryError if creation fails (e.g. email already taken).
        """
        return self._request(
            "POST",
            "/users",
            payload={"email": email, "password": password, "email_confirm": email_confirm},
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _request(self, method: str, path: str, *, payload: dict[str, Any] | None = None) -> Any:
        url = f"{self._admin_url}{path}"

        headers: dict[str, str] = {
            "apikey": self._key,
            "Authorization": f"Bearer {self._key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

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
            raise UserRepositoryError(
                f"Supabase Auth admin error {exc.code}: {message}"
            ) from exc
        except URLError as exc:
            raise UserRepositoryError(
                f"Supabase Auth admin network failure: {exc.reason}"
            ) from exc
        except TimeoutError as exc:
            raise UserRepositoryError("Supabase Auth admin request timed out.") from exc

        try:
            return json.loads(body)
        except json.JSONDecodeError as exc:
            raise UserRepositoryError(
                "Supabase Auth admin returned non-JSON response."
            ) from exc
