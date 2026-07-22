"""
============================================================
Example: Bank Transfer with Unit of Work
Pattern: Unit of Work (Architectural)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
You need to transfer $500 from Alice's account to Bob's account.
1. Deduct $500 from Alice.
2. Add $500 to Bob.

If step 1 succeeds but step 2 crashes (e.g. database disconnects), 
the money is destroyed! It vanished into the void.

To fix this, we use a Unit of Work (UoW). The UoW ensures that BOTH
operations happen together (Atomicity). If anything fails, it rolls
back all changes.

KEY INSIGHT:
------------
We use Python Context Managers (`__enter__` and `__exit__`).
If an exception occurs inside the `with` block, `__exit__` catches
it and calls `rollback()`.

============================================================
"""

from abc import ABC, abstractmethod
from types import TracebackType


# ─── Simulated Database ────────────────────────────────

class FakeDatabaseSession:
    """Simulates an ORM session (like SQLAlchemy's Session)."""
    def __init__(self) -> None:
        self.accounts = {"Alice": 1000, "Bob": 100}
        self.uncommitted_changes: dict[str, int] = {}
        self.is_active = False
        
    def begin(self) -> None:
        self.is_active = True
        self.uncommitted_changes.clear()
        print("  [DB] BEGIN TRANSACTION")
        
    def commit(self) -> None:
        if not self.is_active: return
        self.accounts.update(self.uncommitted_changes)
        self.is_active = False
        self.uncommitted_changes.clear()
        print("  [DB] COMMIT")
        
    def rollback(self) -> None:
        if not self.is_active: return
        self.is_active = False
        self.uncommitted_changes.clear()
        print("  [DB] ROLLBACK (Discarding pending changes)")
        
    def update_balance(self, user: str, new_balance: int) -> None:
        self.uncommitted_changes[user] = new_balance


# ─── Repositories ──────────────────────────────────────

class AccountRepository:
    """Takes a session and uses it to execute queries."""
    def __init__(self, session: FakeDatabaseSession) -> None:
        self.session = session
        
    def get_balance(self, user: str) -> int:
        # Check uncommitted changes first, then committed state
        return self.session.uncommitted_changes.get(user, self.session.accounts[user])
        
    def set_balance(self, user: str, balance: int) -> None:
        print(f"  [Repo] Setting {user}'s balance to ${balance}")
        self.session.update_balance(user, balance)


# ─── Unit Of Work ──────────────────────────────────────

class AbstractUnitOfWork(ABC):
    accounts: AccountRepository
    
    def __enter__(self) -> 'AbstractUnitOfWork':
        return self
        
    def __exit__(
        self, 
        exc_type: type[BaseException] | None, 
        exc_val: BaseException | None, 
        exc_tb: TracebackType | None
    ) -> None:
        """Called automatically when the 'with' block ends."""
        if exc_type:
            self.rollback() # An error happened! Rollback!
        
    @abstractmethod
    def commit(self) -> None: ...
    @abstractmethod
    def rollback(self) -> None: ...


class DatabaseUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session: FakeDatabaseSession) -> None:
        self.session = session
        
    def __enter__(self) -> 'DatabaseUnitOfWork':
        # 1. Start the transaction
        self.session.begin()
        
        # 2. Instantiate repositories injecting the active session
        self.accounts = AccountRepository(self.session)
        return super().__enter__()
        
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        super().__exit__(exc_type, exc_val, exc_tb)
        # We always rollback at the end. If commit() was called successfully
        # inside the block, this rollback does nothing.
        self.rollback()
        
    def commit(self) -> None:
        self.session.commit()
        
    def rollback(self) -> None:
        self.session.rollback()


# ─── Business Logic (The Service) ──────────────────────

def transfer_money(uow: AbstractUnitOfWork, sender: str, receiver: str, amount: int, crash: bool = False) -> None:
    print(f"\n--- Initiating Transfer: ${amount} from {sender} to {receiver} ---")
    
    try:
        # THE MAGIC HAPPENS HERE
        with uow:
            # 1. Read balances
            sender_bal = uow.accounts.get_balance(sender)
            receiver_bal = uow.accounts.get_balance(receiver)
            
            # 2. Modify balances
            uow.accounts.set_balance(sender, sender_bal - amount)
            
            # Simulate a system crash right in the middle!
            if crash:
                print("  💥 SYSTEM CRASH (Power out, Exception thrown)!")
                raise Exception("System crash!")
                
            uow.accounts.set_balance(receiver, receiver_bal + amount)
            
            # 3. Commit only if we reach the end
            uow.commit()
            print("  ✅ Transfer successful.")
            
    except Exception as e:
        print(f"  ❌ Transfer failed: {e}")


# ─── Demo ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("UNIT OF WORK PATTERN - Bank Transfer")
    print("=" * 60)
    
    # Setup global database connection
    db_session = FakeDatabaseSession()
    
    print("\nInitial State:")
    print(f"  Alice: ${db_session.accounts['Alice']}")
    print(f"  Bob: ${db_session.accounts['Bob']}")
    
    # Scenario 1: Successful Transfer
    transfer_money(DatabaseUnitOfWork(db_session), "Alice", "Bob", 200)
    print("\nState after Scenario 1:")
    print(f"  Alice: ${db_session.accounts['Alice']} (Expected: 800)")
    print(f"  Bob: ${db_session.accounts['Bob']} (Expected: 300)")
    
    # Scenario 2: Crashed Transfer (Money should NOT be lost!)
    transfer_money(DatabaseUnitOfWork(db_session), "Alice", "Bob", 500, crash=True)
    print("\nState after Scenario 2 (Crash):")
    print(f"  Alice: ${db_session.accounts['Alice']} (Expected: 800 - No change!)")
    print(f"  Bob: ${db_session.accounts['Bob']} (Expected: 300 - No change!)")
    
    print("\n✅ Unit of Work pattern demonstrated successfully!")
