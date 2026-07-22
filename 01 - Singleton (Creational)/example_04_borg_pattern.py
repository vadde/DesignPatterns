"""
============================================================
Example: Borg / Monostate Pattern (Singleton Alternative)
Pattern: Singleton (Creational) — Variant
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
A logging configuration where multiple Logger instances are fine
(different identity / id()), but they MUST share the same state
(same log level, same handlers, same formatter). Borg achieves
this by sharing __dict__ across all instances.

PATTERN PARTICIPANTS IN THIS EXAMPLE:
--------------------------------------
- Borg base class → shares __dict__ across all instances
- LoggerConfig → concrete Borg that shares logging state

KEY INSIGHT:
------------
Singleton: same IDENTITY (same object, same id())
Borg:      same STATE   (different objects, shared __dict__)

Borg is more Pythonic and subclass-friendly. It also plays nicer
with pickling and copying since instances are "real" objects.

============================================================
"""

from typing import Any


class Borg:
    """
    The Borg pattern (a.k.a. Monostate).

    All instances share the SAME __dict__, so they have the same
    state even though they are different objects (different id()).

    Named after the Star Trek Borg: "We are one. Resistance is futile."
    """

    _shared_state: dict[str, Any] = {}

    def __init__(self) -> None:
        # Point this instance's __dict__ to the shared state
        # This is the magic — all instances now share attributes
        self.__dict__ = self._shared_state


class LoggerConfig(Borg):
    """
    Shared logging configuration using Borg pattern.

    Every LoggerConfig instance sees the same log_level, handlers,
    and formatter — because they all share __dict__.
    """

    def __init__(
        self,
        log_level: str = "INFO",
        formatter: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    ) -> None:
        super().__init__()

        # Only initialize if not already set (first instance)
        if not hasattr(self, "_initialized"):
            self.log_level = log_level
            self.formatter = formatter
            self.handlers: list[str] = ["console"]
            self._initialized = True
            print(f"  📋 LoggerConfig initialized (level={log_level})")

    def add_handler(self, handler: str) -> None:
        if handler not in self.handlers:
            self.handlers.append(handler)
            print(f"  ➕ Added handler: {handler}")

    def set_level(self, level: str) -> None:
        self.log_level = level
        print(f"  🔧 Log level changed to: {level}")

    def __repr__(self) -> str:
        return f"LoggerConfig(level={self.log_level}, handlers={self.handlers})"


# ─── Usage / Demo ──────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("BORG / MONOSTATE PATTERN")
    print("=" * 60)

    # Create first instance
    logger1 = LoggerConfig(log_level="DEBUG")
    print(f"  logger1: {logger1}")
    print(f"  id(logger1): {id(logger1)}")
    print()

    # Create second instance — shares state with first
    logger2 = LoggerConfig()
    print(f"  logger2: {logger2}")
    print(f"  id(logger2): {id(logger2)}")
    print()

    # Key difference from Singleton: DIFFERENT objects, SAME state
    print(f"  logger1 is logger2: {logger1 is logger2}")  # False!
    print(f"  logger1.__dict__ is logger2.__dict__: {logger1.__dict__ is logger2.__dict__}")  # True!
    assert logger1 is not logger2, "Borg creates different objects"
    assert logger1.__dict__ is logger2.__dict__, "Borg shares __dict__"
    print()

    # Mutating one affects the other (shared state)
    logger1.add_handler("file")
    logger1.set_level("WARNING")
    print(f"\n  After logger1 mutations:")
    print(f"  logger2.log_level: {logger2.log_level}")
    print(f"  logger2.handlers: {logger2.handlers}")
    assert logger2.log_level == "WARNING", "Shared state broken!"
    assert "file" in logger2.handlers, "Shared state broken!"

    # Comparison table
    print()
    print("  ╔════════════════════╦═══════════════════════════╗")
    print("  ║                    ║  Singleton vs Borg        ║")
    print("  ╠════════════════════╬═══════════════════════════╣")
    print("  ║ Identity (is)      ║  Same obj  vs  Diff objs  ║")
    print("  ║ State (__dict__)   ║  Same      vs  Same       ║")
    print(f"  ║ id(a) == id(b)     ║  True      vs  {id(logger1) == id(logger2):<14}║")
    print("  ║ Subclass-friendly  ║  Tricky    vs  Easy       ║")
    print("  ║ Pickle/Copy        ║  Tricky    vs  Works      ║")
    print("  ╚════════════════════╩═══════════════════════════╝")

    print("\n✅ Borg / Monostate pattern demonstrated successfully!")
