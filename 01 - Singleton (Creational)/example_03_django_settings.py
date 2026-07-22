"""
============================================================
Example: Singleton via Metaclass (Reusable)
Pattern: Singleton (Creational)
Framework: Pure Python (simulating Django-style settings)
============================================================

REAL-WORLD SCENARIO:
--------------------
Django's settings module exposes a single LazySettings object that
wraps the project's settings. Here we simulate the same concept:
a Settings class that loads configuration lazily (on first access)
and is guaranteed to be a singleton via a reusable metaclass.

PATTERN PARTICIPANTS IN THIS EXAMPLE:
--------------------------------------
- SingletonMeta → metaclass that enforces single-instance per class
- Settings → the singleton class (analogous to Django's LazySettings)
- CacheManager → another singleton using the SAME metaclass

KEY INSIGHT:
------------
A metaclass-based Singleton is REUSABLE — any class can become a
singleton by simply declaring `metaclass=SingletonMeta`. No code
duplication. The metaclass stores instances in a per-class dict,
so subclasses get their own instances (fixing the inheritance bug).

============================================================
"""

import threading


class SingletonMeta(type):
    """
    Metaclass that makes any class a thread-safe Singleton.

    Usage:
        class MyService(metaclass=SingletonMeta):
            pass

    How it works:
    - type.__call__ is what runs when you write MyClass()
    - We override __call__ to check if an instance already exists
    - Stores instances in a per-class dict, so subclasses work correctly
    """

    _instances: dict[type, object] = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]

    def _reset(cls) -> None:
        """Remove the stored instance (for testing)."""
        cls._instances.pop(cls, None)


# ─── Django-Style Settings Singleton ───────────────

class Settings(metaclass=SingletonMeta):
    """
    Simulates Django's settings object.

    In Django: django.conf.settings is a LazySettings singleton.
    Here we demonstrate the same concept with a metaclass.
    """

    def __init__(self) -> None:
        # This runs only ONCE (metaclass prevents re-creation)
        self.DEBUG: bool = True
        self.DATABASE: dict = {
            "ENGINE": "django.db.backends.postgresql",
            "HOST": "localhost",
            "PORT": 5432,
            "NAME": "myapp_db",
        }
        self.SECRET_KEY: str = "super-secret-key-do-not-share"
        self.INSTALLED_APPS: list[str] = [
            "django.contrib.auth",
            "django.contrib.admin",
            "myapp.core",
        ]
        print(f"  ⚙️  Settings loaded (DEBUG={self.DEBUG})")

    def __repr__(self) -> str:
        return f"Settings(DEBUG={self.DEBUG}, DB={self.DATABASE['NAME']})"


class CacheManager(metaclass=SingletonMeta):
    """
    Another singleton using the SAME metaclass.
    Demonstrates reusability — no code duplication!
    """

    def __init__(self, backend: str = "redis") -> None:
        self.backend = backend
        self._cache: dict[str, object] = {}
        print(f"  💾 CacheManager initialized (backend={backend})")

    def set(self, key: str, value: object) -> None:
        self._cache[key] = value

    def get(self, key: str) -> object | None:
        return self._cache.get(key)

    def __repr__(self) -> str:
        return f"CacheManager(backend={self.backend}, entries={len(self._cache)})"


# ─── Usage / Demo ──────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("METACLASS SINGLETON — Reusable Across Classes")
    print("=" * 60)

    # Settings singleton
    print("\n--- Settings ---")
    s1 = Settings()
    s2 = Settings()
    print(f"  s1: {s1}")
    print(f"  s2: {s2}")
    print(f"  s1 is s2: {s1 is s2}")
    assert s1 is s2, "Settings singleton violated!"

    # CacheManager singleton (SAME metaclass, DIFFERENT instance)
    print("\n--- CacheManager ---")
    c1 = CacheManager(backend="redis")
    c2 = CacheManager(backend="memcached")  # Ignored — already created
    print(f"  c1: {c1}")
    print(f"  c2: {c2}")
    print(f"  c1 is c2: {c1 is c2}")
    print(f"  c2.backend: '{c2.backend}'  (still 'redis' — init ran only once)")
    assert c1 is c2, "CacheManager singleton violated!"

    # Settings and CacheManager are DIFFERENT singletons
    print("\n--- Cross-Class Independence ---")
    print(f"  Settings is CacheManager? {s1 is c1}")
    assert s1 is not c1, "Different classes should have different instances!"

    # Cache actually works
    c1.set("user:123", {"name": "Alice"})
    result = c2.get("user:123")
    print(f"  Cache set via c1, get via c2: {result}")
    assert result == {"name": "Alice"}, "Shared state broken!"

    print("\n✅ Metaclass Singleton demonstrated successfully!")
