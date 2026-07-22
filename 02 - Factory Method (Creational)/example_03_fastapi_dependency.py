"""
============================================================
Example: FastAPI-Style Dependency Injection as Factory
Pattern: Factory Method (Creational)
Framework: FastAPI-inspired (pure Python simulation)
============================================================

REAL-WORLD SCENARIO:
--------------------
In FastAPI, `Depends()` is essentially a factory method — you
declare WHAT dependency you need, and the framework creates it
for you. This example simulates how FastAPI's DI works under
the hood, showing that Depends() IS the Factory Method pattern.

PATTERN PARTICIPANTS IN THIS EXAMPLE:
--------------------------------------
- Product → Database session, AuthService, etc.
- Factory → Dependency functions (get_db, get_auth_service)
- Creator → The DI framework that calls the factories

KEY INSIGHT:
------------
FastAPI's Depends() is Factory Method in disguise. The dependency
function IS the factory — it creates and yields the right resource.
The endpoint never knows HOW the resource was created.

============================================================
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Generator
from contextlib import contextmanager


# ─── Simulated Database ────────────────────────────

@dataclass
class DatabaseSession:
    """Simulates a database session (like SQLAlchemy Session)."""
    db_url: str
    _queries: list[str] = field(default_factory=list)
    _committed: bool = False

    def execute(self, query: str) -> str:
        self._queries.append(query)
        return f"Result of: {query}"

    def commit(self) -> None:
        self._committed = True

    def close(self) -> None:
        pass  # Cleanup

    def __repr__(self) -> str:
        return f"DBSession(url={self.db_url}, queries={len(self._queries)})"


# ─── Dependency Factories (the "factory methods") ──

def get_db() -> Generator[DatabaseSession, None, None]:
    """
    Factory that creates a database session.

    This IS the Factory Method — FastAPI calls this function,
    gets a session, injects it into the endpoint, and cleans
    up after the request.
    """
    db = DatabaseSession(db_url="postgresql://localhost/myapp")
    try:
        yield db
        db.commit()
    finally:
        db.close()


@dataclass
class AuthService:
    """Simulates an authentication service."""
    secret_key: str = "my-jwt-secret"

    def verify_token(self, token: str) -> dict[str, Any]:
        # Simplified — in reality, decode JWT
        if token == "valid-token":
            return {"user_id": 42, "role": "admin"}
        raise PermissionError("Invalid token")


def get_auth_service() -> AuthService:
    """Factory for AuthService — no cleanup needed, so no generator."""
    return AuthService(secret_key="production-secret-key")


@dataclass
class CurrentUser:
    user_id: int
    role: str


def get_current_user(
    token: str = "valid-token",
    auth: AuthService | None = None,
) -> CurrentUser:
    """
    Factory that DEPENDS ON another factory (chained DI).

    In FastAPI: Depends(get_current_user) which itself uses
    Depends(get_auth_service). Factories composing factories!
    """
    if auth is None:
        auth = get_auth_service()
    payload = auth.verify_token(token)
    return CurrentUser(user_id=payload["user_id"], role=payload["role"])


# ─── Simulated DI Container ────────────────────────

class DependencyInjector:
    """
    Simplified version of how FastAPI's Depends() works internally.

    This IS the Factory Method pattern: the injector calls factory
    functions and provides their results to the endpoint.
    """

    def __init__(self) -> None:
        self._overrides: dict[Callable, Callable] = {}

    def override(self, original: Callable, replacement: Callable) -> None:
        """Override a dependency (for testing)."""
        self._overrides[original] = replacement

    def resolve(self, factory: Callable) -> Any:
        """
        Resolve a dependency by calling its factory.

        If overridden (for testing), call the override instead.
        """
        actual_factory = self._overrides.get(factory, factory)
        result = actual_factory()

        # Handle generators (like get_db which yields)
        if hasattr(result, "__next__"):
            return next(result)
        return result


# ─── Simulated FastAPI Endpoints ───────────────────

def list_users_endpoint(db: DatabaseSession, user: CurrentUser) -> dict:
    """
    Simulated endpoint.

    In FastAPI this would be:
        @app.get("/users")
        def list_users(db: Session = Depends(get_db),
                       user: CurrentUser = Depends(get_current_user)):

    The endpoint doesn't know HOW db or user were created.
    It just USES them. That's Factory Method + DI.
    """
    if user.role != "admin":
        return {"error": "Forbidden"}

    result = db.execute("SELECT * FROM users")
    return {"data": result, "requested_by": user.user_id}


# ─── Usage / Demo ──────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("FACTORY METHOD — FastAPI-Style Dependency Injection")
    print("=" * 60)

    injector = DependencyInjector()

    # Resolve dependencies using factories
    print("\n  --- Production Dependencies ---")
    db = injector.resolve(get_db)
    print(f"  DB: {db}")

    auth = injector.resolve(get_auth_service)
    print(f"  Auth: {auth}")

    user = injector.resolve(get_current_user)
    print(f"  User: {user}")

    # Call endpoint with injected dependencies
    response = list_users_endpoint(db=db, user=user)
    print(f"  Response: {response}")

    # ── Testing: Override factories ──────────────────
    print("\n  --- Test Dependencies (Overridden) ---")

    # Create test doubles
    def get_test_db() -> DatabaseSession:
        return DatabaseSession(db_url="sqlite:///:memory:")

    def get_test_user() -> CurrentUser:
        return CurrentUser(user_id=999, role="tester")

    injector.override(get_db, get_test_db)
    injector.override(get_current_user, get_test_user)

    test_db = injector.resolve(get_db)
    test_user = injector.resolve(get_current_user)
    print(f"  Test DB: {test_db}")
    print(f"  Test User: {test_user}")

    assert test_db.db_url == "sqlite:///:memory:", "Override should use test DB"
    assert test_user.role == "tester", "Override should use test user"

    print("\n  Key insight: Depends() IS Factory Method!")
    print("  The dependency function = the factory")
    print("  The framework = the client that calls the factory")
    print("  Override for testing = swap the factory, not the product")

    print("\n✅ FastAPI-Style Dependency Factory demonstrated successfully!")
