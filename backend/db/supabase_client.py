"""Minimal Supabase REST client wrapper used by repository classes."""

from __future__ import annotations

import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class SupabaseError(Exception):
    """Raised when Supabase configuration or REST requests fail."""


class SupabaseRestClient:
    """Small REST wrapper around Supabase PostgREST endpoints."""

    def __init__(self, url: str | None = None, key: str | None = None) -> None:
        self._url = (url or os.getenv("SUPABASE_URL") or "").rstrip("/")
        self._key = key or os.getenv("SUPABASE_KEY") or ""

        if not self._url:
            raise SupabaseError("Missing SUPABASE_URL environment variable.")
        if not self._key:
            raise SupabaseError("Missing SUPABASE_KEY environment variable.")

        self._rest_url = f"{self._url}/rest/v1"

    def select(
        self,
        table: str,
        *,
        filters: dict[str, str] | None = None,
        columns: str = "*",
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        params = {"select": columns}
        if filters:
            params.update(filters)
        if limit is not None:
            params["limit"] = str(limit)
        response = self._request("GET", f"/{table}", query_params=params)
        if isinstance(response, list):
            return response
        raise SupabaseError(f"Expected list response when selecting from {table}.")

    def select_one(
        self,
        table: str,
        *,
        filters: dict[str, str],
        columns: str = "*",
    ) -> dict[str, Any] | None:
        rows = self.select(table, filters=filters, columns=columns, limit=1)
        return rows[0] if rows else None

    def insert(self, table: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = self._request(
            "POST",
            f"/{table}",
            payload=payload,
            extra_headers={"Prefer": "return=representation"},
        )
        if isinstance(response, list) and response:
            return response[0]
        raise SupabaseError(f"Expected inserted row response for table {table}.")

    def upsert(
        self,
        table: str,
        payload: dict[str, Any],
        *,
        on_conflict: str,
    ) -> dict[str, Any]:
        response = self._request(
            "POST",
            f"/{table}",
            payload=payload,
            query_params={"on_conflict": on_conflict},
            extra_headers={
                "Prefer": "resolution=merge-duplicates,return=representation",
            },
        )
        if isinstance(response, list) and response:
            return response[0]
        raise SupabaseError(f"Expected upserted row response for table {table}.")

    def delete(self, table: str, *, filters: dict[str, str]) -> None:
        self._request(
            "DELETE",
            f"/{table}",
            query_params=filters,
            extra_headers={"Prefer": "return=minimal"},
        )

    def _request(
        self,
        method: str,
        path: str,
        *,
        payload: dict[str, Any] | None = None,
        query_params: dict[str, str] | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> Any:
        query = urlencode(query_params or {})
        url = f"{self._rest_url}{path}"
        if query:
            url = f"{url}?{query}"

        headers = {
            "apikey": self._key,
            "Authorization": f"Bearer {self._key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if extra_headers:
            headers.update(extra_headers)

        request = Request(
            url,
            data=json.dumps(payload).encode("utf-8") if payload is not None else None,
            headers=headers,
            method=method,
        )

        try:
            with urlopen(request, timeout=15) as response:
                body = response.read().decode("utf-8")
        except HTTPError as exc:
            message = exc.read().decode("utf-8", errors="replace") if hasattr(exc, "read") else ""
            raise SupabaseError(f"Supabase request failed with HTTP {exc.code}: {message}") from exc
        except URLError as exc:
            raise SupabaseError(f"Supabase network failure: {exc.reason}") from exc
        except TimeoutError as exc:
            raise SupabaseError("Supabase request timed out.") from exc

        if not body:
            return None

        try:
            return json.loads(body)
        except json.JSONDecodeError as exc:
            raise SupabaseError("Supabase returned non-JSON response.") from exc


_shared_client: SupabaseRestClient | None = None


def get_supabase_client() -> SupabaseRestClient:
    global _shared_client
    if _shared_client is None:
        _shared_client = SupabaseRestClient()
    return _shared_client
