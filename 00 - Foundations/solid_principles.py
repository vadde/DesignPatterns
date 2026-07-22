"""
============================================================
Example: SOLID Principles — Violation → Fix
Pattern: Foundations
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
We model a simple e-commerce system with users, orders, emails,
and reports. Each SOLID principle is demonstrated by first showing
the VIOLATION (bad code), then the FIX (good code).

KEY INSIGHT:
------------
SOLID isn't abstract theory — it's the difference between code
that's a joy to extend and code that makes you dread Monday mornings.

============================================================
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable


# ════════════════════════════════════════════════════════════
# S — SINGLE RESPONSIBILITY PRINCIPLE (SRP)
# ════════════════════════════════════════════════════════════

# ❌ BAD: One class does EVERYTHING
class UserManagerBad:
    """Handles user CRUD, emails, reports, AND logging. Too many jobs!"""

    def create_user(self, name: str, email: str) -> dict:
        user = {"name": name, "email": email}
        # ... save to database ...
        self._send_welcome_email(email)  # SRP violation: why is email logic here?
        self._log(f"Created user {name}")  # SRP violation: why is logging here?
        return user

    def _send_welcome_email(self, email: str) -> None:
        print(f"Sending welcome email to {email}")

    def _log(self, message: str) -> None:
        print(f"LOG: {message}")

    def generate_user_report(self) -> str:
        # SRP violation: report generation has nothing to do with user management
        return "User Report: ..."


# ✅ GOOD: Each class has ONE reason to change
class UserService:
    """Responsible ONLY for user business logic."""

    def __init__(self, email_service: "EmailService", logger: "AppLogger") -> None:
        self._email_service = email_service
        self._logger = logger

    def create_user(self, name: str, email: str) -> dict:
        user = {"name": name, "email": email}
        # Delegates email and logging to dedicated services
        self._email_service.send_welcome(email)
        self._logger.log(f"Created user {name}")
        return user


class EmailService:
    """Responsible ONLY for sending emails."""

    def send_welcome(self, email: str) -> None:
        print(f"  📧 Sending welcome email to {email}")


class AppLogger:
    """Responsible ONLY for logging."""

    def log(self, message: str) -> None:
        print(f"  📝 LOG: {message}")


class ReportService:
    """Responsible ONLY for generating reports."""

    def generate_user_report(self) -> str:
        return "  📊 User Report: ..."


# ════════════════════════════════════════════════════════════
# O — OPEN/CLOSED PRINCIPLE (OCP)
# ════════════════════════════════════════════════════════════

# ❌ BAD: Adding a new discount type requires modifying existing code
def calculate_discount_bad(customer_type: str, amount: float) -> float:
    """Every new customer type = another elif branch = modification."""
    if customer_type == "gold":
        return amount * 0.10
    elif customer_type == "silver":
        return amount * 0.05
    elif customer_type == "platinum":  # ← had to MODIFY this function
        return amount * 0.15
    else:
        return 0.0


# ✅ GOOD: New discount types = new classes, zero modification to existing code
class DiscountStrategy(ABC):
    """Abstract interface — closed for modification."""

    @abstractmethod
    def calculate(self, amount: float) -> float: ...


class GoldDiscount(DiscountStrategy):
    def calculate(self, amount: float) -> float:
        return amount * 0.10


class SilverDiscount(DiscountStrategy):
    def calculate(self, amount: float) -> float:
        return amount * 0.05


class PlatinumDiscount(DiscountStrategy):
    """New type — added WITHOUT touching any existing class."""

    def calculate(self, amount: float) -> float:
        return amount * 0.15


def calculate_discount_good(strategy: DiscountStrategy, amount: float) -> float:
    """Open for extension (new strategies), closed for modification."""
    return strategy.calculate(amount)


# ════════════════════════════════════════════════════════════
# L — LISKOV SUBSTITUTION PRINCIPLE (LSP)
# ════════════════════════════════════════════════════════════

# ❌ BAD: Square breaks Rectangle's contract
class RectangleBad:
    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        self._width = value

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        self._height = value

    def area(self) -> int:
        return self._width * self._height


class SquareBad(RectangleBad):
    """❌ Violates LSP: setting width also sets height (surprise!)."""

    @RectangleBad.width.setter
    def width(self, value: int) -> None:
        self._width = value
        self._height = value  # ← SURPRISE! Breaks Rectangle's expected behavior

    @RectangleBad.height.setter
    def height(self, value: int) -> None:
        self._width = value  # ← SURPRISE!
        self._height = value


# ✅ GOOD: Separate abstractions that don't violate each other's contracts
@runtime_checkable
class Shape(Protocol):
    """Both Rectangle and Square implement Shape without pretending to be each other."""

    def area(self) -> int: ...


@dataclass
class Rectangle:
    width: int
    height: int

    def area(self) -> int:
        return self.width * self.height


@dataclass
class Square:
    side: int

    def area(self) -> int:
        return self.side * self.side


def print_area(shape: Shape) -> None:
    """Works with ANY Shape — no surprises, no broken contracts."""
    print(f"  📐 Area = {shape.area()}")


# ════════════════════════════════════════════════════════════
# I — INTERFACE SEGREGATION PRINCIPLE (ISP)
# ════════════════════════════════════════════════════════════

# ❌ BAD: Fat interface forces irrelevant method implementations
class IWorkerBad(ABC):
    @abstractmethod
    def work(self) -> str: ...

    @abstractmethod
    def eat(self) -> str: ...

    @abstractmethod
    def sleep(self) -> str: ...


class RobotBad(IWorkerBad):
    def work(self) -> str:
        return "Working..."

    def eat(self) -> str:
        raise NotImplementedError("Robots don't eat!")  # ← Forced to implement nonsense

    def sleep(self) -> str:
        raise NotImplementedError("Robots don't sleep!")  # ← Forced to implement nonsense


# ✅ GOOD: Lean interfaces — each client depends only on what it needs
class Workable(Protocol):
    def work(self) -> str: ...


class Feedable(Protocol):
    def eat(self) -> str: ...


class Sleepable(Protocol):
    def sleep(self) -> str: ...


class HumanWorker:
    """Implements all three — because humans work, eat, AND sleep."""

    def work(self) -> str:
        return "Human working"

    def eat(self) -> str:
        return "Human eating"

    def sleep(self) -> str:
        return "Human sleeping"


class RobotWorker:
    """Implements ONLY Workable — no nonsensical eat()/sleep()."""

    def work(self) -> str:
        return "Robot working"


def assign_task(worker: Workable) -> str:
    """Only cares about work() — doesn't force eat() or sleep()."""
    return worker.work()


# ════════════════════════════════════════════════════════════
# D — DEPENDENCY INVERSION PRINCIPLE (DIP)
# ════════════════════════════════════════════════════════════

# ❌ BAD: High-level module directly depends on low-level module
class MySQLDatabase:
    def save(self, data: dict) -> None:
        print(f"  💾 Saving to MySQL: {data}")


class OrderServiceBad:
    def __init__(self) -> None:
        self._db = MySQLDatabase()  # ← Hardcoded dependency on MySQL

    def place_order(self, order: dict) -> None:
        self._db.save(order)


# ✅ GOOD: Both depend on an abstraction (Protocol)
class Database(Protocol):
    """The abstraction both high-level and low-level modules depend on."""

    def save(self, data: dict) -> None: ...


class MySQLDB:
    def save(self, data: dict) -> None:
        print(f"  💾 Saving to MySQL: {data}")


class PostgresDB:
    def save(self, data: dict) -> None:
        print(f"  💾 Saving to PostgreSQL: {data}")


class InMemoryDB:
    """Perfect for testing — swap in without changing OrderService."""

    def __init__(self) -> None:
        self.store: list[dict] = []

    def save(self, data: dict) -> None:
        self.store.append(data)
        print(f"  💾 Saving to InMemory: {data}")


class OrderService:
    """Depends on Database PROTOCOL, not a specific implementation."""

    def __init__(self, db: Database) -> None:
        self._db = db  # ← Injected abstraction

    def place_order(self, order: dict) -> None:
        self._db.save(order)


# ════════════════════════════════════════════════════════════
# DEMO
# ════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("S — SINGLE RESPONSIBILITY PRINCIPLE")
    print("=" * 60)
    email_svc = EmailService()
    logger = AppLogger()
    user_svc = UserService(email_svc, logger)
    user = user_svc.create_user("Alice", "alice@example.com")
    print(f"  Created: {user}")
    print()

    print("=" * 60)
    print("O — OPEN/CLOSED PRINCIPLE")
    print("=" * 60)
    amount = 100.0
    for strategy in [GoldDiscount(), SilverDiscount(), PlatinumDiscount()]:
        discount = calculate_discount_good(strategy, amount)
        print(f"  {strategy.__class__.__name__}: ${amount} → discount ${discount:.2f}")
    print()

    print("=" * 60)
    print("L — LISKOV SUBSTITUTION PRINCIPLE")
    print("=" * 60)
    shapes: list[Shape] = [Rectangle(5, 10), Square(7)]
    for s in shapes:
        print(f"  {s.__class__.__name__}:", end="")
        print_area(s)
    print()

    print("=" * 60)
    print("I — INTERFACE SEGREGATION PRINCIPLE")
    print("=" * 60)
    human = HumanWorker()
    robot = RobotWorker()
    print(f"  {assign_task(human)}")
    print(f"  {assign_task(robot)}")
    print()

    print("=" * 60)
    print("D — DEPENDENCY INVERSION PRINCIPLE")
    print("=" * 60)
    # Swap database implementation without changing OrderService
    for db in [MySQLDB(), PostgresDB(), InMemoryDB()]:
        order_svc = OrderService(db)
        order_svc.place_order({"item": "Widget", "qty": 3})
    print()

    print("✅ All SOLID principles demonstrated successfully!")
