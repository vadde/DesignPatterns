"""
============================================================
Example: Testable User Service with Repository
Pattern: Repository (Architectural)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
You have a service that upgrades a user to a "Premium" account.
To do this, it needs to check their balance, deduct funds, and
update their status.

If you hardcode database queries (SQL/ORM) into this service, 
you cannot unit test it without a real database. 

Instead, we use a `UserRepository` interface. For production, we
use a `SqlUserRepository`. For testing, we use a `FakeUserRepository`.

KEY INSIGHT:
------------
The `UserService` (Business Logic) knows absolutely NOTHING about SQL,
sessions, connections, or database tables. It only knows about the
pure `User` entity and the `UserRepository` protocol.

============================================================
"""

from typing import Protocol, Optional
from dataclasses import dataclass


# ─── 1. Domain Entity (Pure Python, No DB logic) ────────

@dataclass
class User:
    """A pure domain entity. Contains business logic and data."""
    id: int
    name: str
    balance: float
    is_premium: bool = False
    
    def can_afford(self, amount: float) -> bool:
        return self.balance >= amount
        
    def upgrade_to_premium(self) -> None:
        if self.is_premium:
            raise ValueError("User is already premium!")
        self.is_premium = True
        self.balance -= 100.0


# ─── 2. Repository Interface ───────────────────────────

class UserRepository(Protocol):
    """The contract for data access. Completely independent of the DB."""
    
    def get(self, user_id: int) -> Optional[User]: ...
    def save(self, user: User) -> None: ...


# ─── 3. Business Service (The Use Case) ────────────────

class UserService:
    """
    Business Logic Layer. 
    Notice how it takes the repository via Dependency Injection.
    """
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo
        
    def upgrade_user(self, user_id: int) -> None:
        print(f"  [Service] Attempting to upgrade user {user_id}...")
        
        user = self.repo.get(user_id)
        if not user:
            print("  ❌ Upgrade failed: User not found.")
            return
            
        if not user.can_afford(100.0):
            print(f"  ❌ Upgrade failed: {user.name} has insufficient funds (${user.balance:.2f}).")
            return
            
        # Execute business logic on the pure entity
        user.upgrade_to_premium()
        
        # Persist the changes
        self.repo.save(user)
        print(f"  ✅ Upgrade successful! {user.name} is now Premium. Balance: ${user.balance:.2f}")


# ─── 4. Concrete Repositories ──────────────────────────

class SqlUserRepository:
    """
    Production Repository.
    Pretend this connects to Postgres using SQLAlchemy.
    """
    def __init__(self, db_connection_string: str) -> None:
        print(f"  [DB] Connecting to Production Database at {db_connection_string}...")
        
    def get(self, user_id: int) -> Optional[User]:
        print(f"  [DB] Executing: SELECT * FROM users WHERE id = {user_id}")
        # Simulated DB fetch...
        return User(id=user_id, name="Production Proderson", balance=500.0)
        
    def save(self, user: User) -> None:
        print(f"  [DB] Executing: UPDATE users SET balance={user.balance}, is_premium={user.is_premium} WHERE id={user.id}")


class FakeUserRepository:
    """
    Testing Repository.
    Stores data in memory (a dictionary). Lightning fast. No DB required.
    """
    def __init__(self, initial_data: list[User]) -> None:
        self._store = {user.id: user for user in initial_data}
        
    def get(self, user_id: int) -> Optional[User]:
        print(f"  [TestRepo] Fetching user {user_id} from memory...")
        return self._store.get(user_id)
        
    def save(self, user: User) -> None:
        print(f"  [TestRepo] Saving user {user.id} to memory...")
        self._store[user.id] = user


# ─── Demo ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("REPOSITORY PATTERN")
    print("=" * 60)
    
    print("\n--- 1. Running in Production Mode ---")
    prod_repo = SqlUserRepository("postgresql://user:pass@localhost/db")
    prod_service = UserService(prod_repo)
    prod_service.upgrade_user(99)
    
    print("\n--- 2. Running in Unit Test Mode ---")
    # We can easily setup edge cases without touching a database!
    test_repo = FakeUserRepository([
        User(id=1, name="Alice (Rich)", balance=500.0),
        User(id=2, name="Bob (Poor)", balance=20.0)
    ])
    test_service = UserService(test_repo)
    
    print("\n  [Testing Bob (Should Fail)]")
    test_service.upgrade_user(2)
    
    print("\n  [Testing Alice (Should Succeed)]")
    test_service.upgrade_user(1)
    
    print("\n✅ Repository pattern demonstrated successfully!")
