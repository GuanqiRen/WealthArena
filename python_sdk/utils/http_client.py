"""HTTP client for making API requests with authentication."""

from __future__ import annotations

import json
import time
from typing import Any
from urllib.request import Request, urlopen
from urllib.error import HTTPError as URLHTTPError


class HTTPError(Exception):
    """Custom exception for HTTP errors."""

    def __init__(self, status_code: int, message: str):
        """Initialize HTTPError.

        Args:
            status_code: HTTP status code.
            message: Error message.
        """
        self.status_code = status_code
        self.message = message
        super().__init__(f"HTTP {status_code}: {message}")


class HTTPClient:
    """HTTP client for making API requests with auth token."""

    def __init__(self, base_url: str, max_retries: int = 3, timeout: int = 10):
        """Initialize HTTP client.

        Args:
            base_url: Base URL for API (e.g., "http://localhost:8000").
            max_retries: Maximum number of retries for failed requests.
            timeout: Request timeout in seconds.
        """
        self.base_url = base_url.rstrip("/")
        self.max_retries = max_retries
        self.timeout = timeout
        self.token: str | None = None
        self.token_type: str = "Bearer"

    def set_token(self, token: str, token_type: str = "Bearer") -> None:
        """Set authorization token.

        Args:
            token: JWT token.
            token_type: Token type (default: "Bearer").
        """
        self.token: str | None = token
        self.token_type = token_type

    def _make_request(
        self,
        method: str,
        url: str,
        data: dict[str, Any] | None = None,
        retry_count: int = 0,
    ) -> dict[str, Any]:
        """Make an HTTP request with retry logic.

        Args:
            method: HTTP method (GET, POST, etc.).
            url: Full URL for the request.
            data: Request body data (for POST requests).
            retry_count: Current retry attempt.

        Returns:
            Parsed JSON response.

        Raises:
            HTTPError: If request fails after retries.
        """
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        if self.token:
            headers["Authorization"] = f"{self.token_type} {self.token}"

        body = None
        if data is not None:
            body = json.dumps(data).encode("utf-8")

        try:
            req = Request(url, data=body, headers=headers, method=method)
            with urlopen(req, timeout=self.timeout) as response:
                response_data = response.read().decode("utf-8")
                return json.loads(response_data) if response_data else {}
        except URLHTTPError as e:
            error_body = e.read().decode("utf-8")
            try:
                error_data = json.loads(error_body)
                error_msg = error_data.get("detail", error_body)
            except json.JSONDecodeError:
                error_msg = error_body

            # Retry on server errors (5xx)
            if 500 <= e.code < 600 and retry_count < self.max_retries:
                time.sleep(2**retry_count)  # Exponential backoff
                return self._make_request(method, url, data, retry_count + 1)

            raise HTTPError(e.code, error_msg) from e
        except Exception as e:
            if retry_count < self.max_retries:
                time.sleep(2**retry_count)
                return self._make_request(method, url, data, retry_count + 1)
            raise HTTPError(500, f"Request failed: {str(e)}") from e

    def get(self, endpoint: str) -> dict[str, Any]:
        """Make a GET request.

        Args:
            endpoint: API endpoint (e.g., "/portfolios").

        Returns:
            Parsed JSON response.
        """
        url = f"{self.base_url}{endpoint}"
        return self._make_request("GET", url)

    def post(
        self, endpoint: str, data: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Make a POST request.

        Args:
            endpoint: API endpoint (e.g., "/auth/login").
            data: Request body data.

        Returns:
            Parsed JSON response.
        """
        url = f"{self.base_url}{endpoint}"
        return self._make_request("POST", url, data)

    def delete(self, endpoint: str) -> dict[str, Any]:
        """Make a DELETE request.

        Args:
            endpoint: API endpoint (e.g., "/portfolios/{id}").

        Returns:
            Parsed JSON response.
        """
        url = f"{self.base_url}{endpoint}"
        return self._make_request("DELETE", url)
