"""
============================================================
Example: Web Middleware Chain (Modern)
Pattern: Chain of Responsibility (Behavioral)
Framework: Pure Python (FastAPI/Django style)
============================================================

REAL-WORLD SCENARIO:
--------------------
A modern web server receives an HTTP request. Before it reaches
the actual application logic (the view), it needs to pass through:
1. Logging Middleware
2. Authentication Middleware
3. Payload Validation Middleware

Unlike the classic GoF pattern (where the chain stops at the FIRST
handler that can process it), this "Middleware" chain passes the 
request through EVERY handler sequentially. Each handler can:
- Modify the request/response
- Stop the chain early (e.g., if Auth fails)
- Do work *after* the next handler returns (onion routing)

KEY INSIGHT:
------------
This is the architecture used by almost every modern web framework
(Django, Express, FastAPI, Starlette). It is a variation of the
Chain of Responsibility pattern.

============================================================
"""

from typing import Any, Callable, Dict

# The "Request" and "Response" objects
Request = Dict[str, Any]
Response = Dict[str, Any]

# A handler is a function that takes a Request and returns a Response
HandlerFunc = Callable[[Request], Response]


# ─── Middleware Base Class ─────────────────────────────

class Middleware:
    """
    The base class for our chain. 
    It holds a reference to the `next` middleware (or the final app).
    """
    def __init__(self) -> None:
        self._next_app: HandlerFunc | None = None
        
    def set_next(self, next_app: HandlerFunc) -> None:
        self._next_app = next_app
        
    def __call__(self, request: Request) -> Response:
        """
        By implementing __call__, our middleware acts like a function.
        Subclasses MUST implement this and call `self._next_app(request)`
        when they are ready to pass the request down the chain.
        """
        raise NotImplementedError()


# ─── Concrete Middleware (The Handlers) ────────────────

class LoggingMiddleware(Middleware):
    def __call__(self, request: Request) -> Response:
        print(f"  📝 [Logging] Received request to {request.get('path')}")
        
        # Pass to the next handler...
        if self._next_app:
            response = self._next_app(request)
        else:
            response = {"status": 500, "body": "No app attached"}
            
        # We can also do work ON THE WAY BACK UP! (Onion routing)
        print(f"  📝 [Logging] Sending response with status {response.get('status')}")
        return response


class AuthMiddleware(Middleware):
    def __call__(self, request: Request) -> Response:
        print("  🔒 [Auth] Checking headers...")
        token = request.get("headers", {}).get("Authorization")
        
        if token != "Bearer valid_token":
            print("  🔒 [Auth] ❌ Invalid token! Halting the chain.")
            # SHORT-CIRCUIT: We DO NOT call the next app!
            return {"status": 401, "body": "Unauthorized"}
            
        print("  🔒 [Auth] ✅ Token valid. Passing down chain.")
        if self._next_app:
            return self._next_app(request)
        return {"status": 500, "body": "No app attached"}


class ValidationMiddleware(Middleware):
    def __call__(self, request: Request) -> Response:
        print("  ✅ [Validation] Checking payload...")
        if "body" not in request:
            print("  ✅ [Validation] ❌ Missing body! Halting the chain.")
            return {"status": 400, "body": "Bad Request"}
            
        print("  ✅ [Validation] Payload valid. Passing down chain.")
        if self._next_app:
            return self._next_app(request)
        return {"status": 500, "body": "No app attached"}


# ─── The Final Application (End of the Chain) ──────────

def core_application(request: Request) -> Response:
    """
    The actual view function. It assumes all middleware checks passed.
    """
    print(f"  ⚙️  [App] Processing valid, authenticated request: {request['body']}")
    return {"status": 200, "body": "Success!"}


# ─── Chain Builder Utility ─────────────────────────────

def build_middleware_chain(middlewares: list[Middleware], app: HandlerFunc) -> HandlerFunc:
    """
    Helper function to wire the chain together backwards.
    M1 -> M2 -> M3 -> App
    """
    current_app = app
    for middleware in reversed(middlewares):
        middleware.set_next(current_app)
        current_app = middleware
    return current_app


# ─── Demo ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("CHAIN OF RESPONSIBILITY - Web Middleware")
    print("=" * 60)
    
    # 1. Build the chain
    chain = build_middleware_chain(
        middlewares=[
            LoggingMiddleware(),
            AuthMiddleware(),
            ValidationMiddleware()
        ],
        app=core_application
    )
    
    # 2. Test Case 1: Bad Auth (Should halt at AuthMiddleware)
    print("\n--- Test 1: Bad Token ---")
    bad_req = {
        "path": "/api/data",
        "headers": {"Authorization": "Bearer BAD_TOKEN"},
        "body": {"data": 123}
    }
    resp1 = chain(bad_req)
    print(f"Result: {resp1}")
    
    # 3. Test Case 2: Bad Payload (Should halt at ValidationMiddleware)
    print("\n--- Test 2: Bad Payload ---")
    bad_payload_req = {
        "path": "/api/data",
        "headers": {"Authorization": "Bearer valid_token"}
        # missing "body"
    }
    resp2 = chain(bad_payload_req)
    print(f"Result: {resp2}")
    
    # 4. Test Case 3: Perfect Request (Should reach the App)
    print("\n--- Test 3: Perfect Request ---")
    good_req = {
        "path": "/api/data",
        "headers": {"Authorization": "Bearer valid_token"},
        "body": {"data": 123}
    }
    resp3 = chain(good_req)
    print(f"Result: {resp3}")
    
    print("\n✅ Middleware Chain demonstrated successfully!")
