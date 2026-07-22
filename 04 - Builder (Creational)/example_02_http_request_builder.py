"""
============================================================
Example: HTTP Request Builder
Pattern: Builder (Creational)
Framework: Pure Python (requests-inspired)
============================================================

REAL-WORLD SCENARIO:
--------------------
Building HTTP requests with many optional parts: URL, method,
headers, query parameters, body, timeout, authentication.
A builder makes this readable and prevents argument-order confusion.

KEY INSIGHT:
------------
The builder validates constraints at build() time, not during
individual set calls. This allows flexible construction order
while ensuring the final product is always valid.

============================================================
"""

from dataclasses import dataclass, field
from typing import Any, Self
import json


@dataclass(frozen=True)
class HTTPRequest:
    """Immutable HTTP request product."""
    method: str
    url: str
    headers: dict[str, str]
    params: dict[str, str]
    body: str | None
    timeout: int
    auth: tuple[str, str] | None

    def __str__(self) -> str:
        lines = [f"{self.method} {self.url}"]
        if self.params:
            qs = "&".join(f"{k}={v}" for k, v in self.params.items())
            lines[0] += f"?{qs}"
        for k, v in self.headers.items():
            lines.append(f"  {k}: {v}")
        if self.body:
            lines.append(f"  Body: {self.body[:80]}...")
        return "\n".join(lines)


class RequestBuilder:
    """Fluent HTTP request builder."""

    def __init__(self, url: str) -> None:
        self._url = url
        self._method = "GET"
        self._headers: dict[str, str] = {}
        self._params: dict[str, str] = {}
        self._body: str | None = None
        self._timeout = 30
        self._auth: tuple[str, str] | None = None

    def method(self, m: str) -> Self:
        self._method = m.upper()
        return self

    def get(self) -> Self:
        return self.method("GET")

    def post(self) -> Self:
        return self.method("POST")

    def put(self) -> Self:
        return self.method("PUT")

    def delete(self) -> Self:
        return self.method("DELETE")

    def header(self, key: str, value: str) -> Self:
        self._headers[key] = value
        return self

    def content_type(self, ct: str) -> Self:
        return self.header("Content-Type", ct)

    def accept(self, ct: str) -> Self:
        return self.header("Accept", ct)

    def bearer_token(self, token: str) -> Self:
        return self.header("Authorization", f"Bearer {token}")

    def param(self, key: str, value: str) -> Self:
        self._params[key] = value
        return self

    def json_body(self, data: dict[str, Any]) -> Self:
        self._body = json.dumps(data)
        self.content_type("application/json")
        return self

    def timeout(self, seconds: int) -> Self:
        self._timeout = seconds
        return self

    def basic_auth(self, username: str, password: str) -> Self:
        self._auth = (username, password)
        return self

    def build(self) -> HTTPRequest:
        # Validation at build time
        if not self._url:
            raise ValueError("URL is required")
        if self._method in ("POST", "PUT", "PATCH") and not self._body:
            raise ValueError(f"{self._method} requires a body")

        return HTTPRequest(
            method=self._method,
            url=self._url,
            headers=dict(self._headers),
            params=dict(self._params),
            body=self._body,
            timeout=self._timeout,
            auth=self._auth,
        )


# ─── Demo ──────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("BUILDER — HTTP Request Builder")
    print("=" * 60)

    # Simple GET request
    print("\n  --- Simple GET ---")
    req1 = (
        RequestBuilder("https://api.example.com/users")
        .get()
        .accept("application/json")
        .param("page", "1")
        .param("limit", "20")
        .timeout(10)
        .build()
    )
    print(f"  {req1}")

    # Authenticated POST request
    print("\n  --- Authenticated POST ---")
    req2 = (
        RequestBuilder("https://api.example.com/orders")
        .post()
        .bearer_token("eyJ0eXAiOiJKV1QiLCJhbG...")
        .json_body({"item": "Widget", "qty": 3, "price": 29.99})
        .timeout(30)
        .build()
    )
    print(f"  {req2}")

    # Validation: POST without body should fail
    print("\n  --- Validation ---")
    try:
        RequestBuilder("https://api.example.com/bad").post().build()
    except ValueError as e:
        print(f"  ⚠️  Expected error: {e}")

    assert req1.method == "GET"
    assert req2.method == "POST"
    assert "Bearer" in req2.headers.get("Authorization", "")
    assert req1.timeout == 10

    print("\n✅ HTTP Request Builder demonstrated successfully!")
