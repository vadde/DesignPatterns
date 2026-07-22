"""
============================================================
Example: Classic Singleton with __new__ Override
Pattern: Singleton (Creational)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
An application needs a single AppConfig object that loads settings
from environment variables ONCE and is shared across all modules.
Creating multiple AppConfig instances would waste memory and risk
inconsistent state.

PATTERN PARTICIPANTS IN THIS EXAMPLE:
--------------------------------------
- Singleton → AppConfig (overrides __new__)
- _instance → class-level reference to the single object

KEY INSIGHT:
------------
__new__ controls object CREATION (before __init__). By overriding
it, we intercept the construction process and return the existing
instance instead of creating a new one.

============================================================
"""

import os


class AppConfig:
    """
    Application configuration — guaranteed single instance.

    Uses __new__ to intercept object creation. The _initialized
    flag prevents __init__ from re-running on subsequent calls.
    """

    _instance: "AppConfig | None" = None

    def __new__(cls) -> "AppConfig":
        # __new__ is called BEFORE __init__ — this is where we
        # control whether a new object is actually created
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        # __init__ is called EVERY time AppConfig() is invoked,
        # even when __new__ returns the existing instance.
        # The _initialized flag prevents re-initialization.
        if self._initialized:
            return

        # Expensive initialization — runs only ONCE
        self.debug: bool = os.getenv("DEBUG", "false").lower() == "true"
        self.db_host: str = os.getenv("DB_HOST", "localhost")
        self.db_port: int = int(os.getenv("DB_PORT", "5432"))
        self.app_name: str = "MyApplication"
        self._initialized = True
        print(f"  ⚙️  AppConfig initialized (debug={self.debug}, db={self.db_host}:{self.db_port})")

    @classmethod
    def _reset(cls) -> None:
        """For testing only — destroys the singleton to allow re-creation."""
        cls._instance = None

    def __repr__(self) -> str:
        return f"AppConfig(app={self.app_name}, db={self.db_host}:{self.db_port})"


# ─── Usage / Demo ──────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("CLASSIC SINGLETON — __new__ Override")
    print("=" * 60)

    # First call → creates the instance
    config1 = AppConfig()
    print(f"  config1: {config1}")
    print(f"  id(config1): {id(config1)}")
    print()

    # Second call → returns the SAME instance (no re-init message)
    config2 = AppConfig()
    print(f"  config2: {config2}")
    print(f"  id(config2): {id(config2)}")
    print()

    # Proof: they are the SAME object
    print(f"  config1 is config2: {config1 is config2}")
    assert config1 is config2, "Singleton contract violated!"

    # Mutating one affects the other (same object)
    config1.app_name = "ModifiedApp"
    assert config2.app_name == "ModifiedApp", "Shared state broken!"
    print(f"  After mutation: config2.app_name = '{config2.app_name}'")
    print()

    # Reset for testing
    AppConfig._reset()
    config3 = AppConfig()
    print(f"  After reset: config3 is config1? {config3 is config1}")
    assert config3 is not config1, "Reset should create a new instance!"

    print()
    print("✅ Classic Singleton demonstrated successfully!")
