"""
============================================================
Example: Event Sourced Bank Account
Pattern: Event Sourcing & CQRS (Architectural)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
We are building a Bank. We cannot use standard CRUD (UPDATE/DELETE).
We must use Event Sourcing to maintain a perfect audit log.

We will build:
1. An Event Store (Append-only log of facts).
2. A Write Side (Processes Commands and creates Events).
3. A Read Side / Projection (Listens to Events and updates the balance).

KEY INSIGHT:
------------
Notice that we NEVER do `balance = new_amount`. We only ever append 
events to a list. The current balance is derived by replaying history.

============================================================
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Protocol


# ─── 1. Events (Immutable Facts) ───────────────────────
# Events are named in the PAST TENSE. They have already happened.

@dataclass(frozen=True)
class Event:
    account_id: str
    timestamp: datetime = datetime.now()

@dataclass(frozen=True)
class AccountOpenedEvent(Event):
    initial_deposit: int = 0

@dataclass(frozen=True)
class MoneyDepositedEvent(Event):
    amount: int = 0

@dataclass(frozen=True)
class MoneyWithdrawnEvent(Event):
    amount: int = 0


class Projection(Protocol):
    """Protocol for Read Models / Projections that consume domain events."""
    def handle_event(self, event: Event) -> None:
        ...


# ─── 2. Event Store (The Single Source of Truth) ───────

class EventStore:
    """An append-only database (like Kafka or EventStoreDB)."""
    def __init__(self) -> None:
        # Dictionary mapping account_id -> List of Events
        self.streams: Dict[str, List[Event]] = {}
        # Simple PubSub for the Read Models
        self.subscribers: List['Projection'] = []
        
    def append(self, event: Event) -> None:
        if event.account_id not in self.streams:
            self.streams[event.account_id] = []
            
        self.streams[event.account_id].append(event)
        print(f"  💾 [EventStore] Appended: {type(event).__name__}")
        
        # Notify the Read Side (CQRS)
        for sub in self.subscribers:
            sub.handle_event(event)
            
    def get_stream(self, account_id: str) -> List[Event]:
        """Fetch all history for an account."""
        return self.streams.get(account_id, [])


# ─── 3. Write Side / Command API ───────────────────────
# Handles business logic, validates rules, and generates events.

class BankAccountService:
    def __init__(self, event_store: EventStore) -> None:
        self.event_store = event_store
        
    def open_account(self, account_id: str, deposit: int) -> None:
        # Validate Command
        if deposit < 0: raise ValueError("Cannot open with negative balance")
        
        # Generate and Save Event
        event = AccountOpenedEvent(account_id=account_id, initial_deposit=deposit)
        self.event_store.append(event)
        
    def deposit(self, account_id: str, amount: int) -> None:
        if amount <= 0: raise ValueError("Deposit must be positive")
        event = MoneyDepositedEvent(account_id=account_id, amount=amount)
        self.event_store.append(event)
        
    def withdraw(self, account_id: str, amount: int) -> None:
        # WARNING: In a real Event Sourced system, we have to rebuild the 
        # state here to ensure they have enough funds before withdrawing!
        # For this simple example, we skip the balance check.
        if amount <= 0: raise ValueError("Withdrawal must be positive")
        event = MoneyWithdrawnEvent(account_id=account_id, amount=amount)
        self.event_store.append(event)


# ─── 4. Read Side / Projection (CQRS) ──────────────────
# A background worker that listens to events and updates a fast DB for queries.

class BalanceProjection:
    """The Read Model. Highly optimized for fast queries."""
    def __init__(self) -> None:
        # This acts like a Redis cache or a highly indexed SQL table
        self.read_database: Dict[str, int] = {}
        
    def handle_event(self, event: Event) -> None:
        """Called automatically when the EventStore receives a new event."""
        account_id = event.account_id
        
        # Initialize if not exists
        if account_id not in self.read_database:
            self.read_database[account_id] = 0
            
        # Apply the changes to the Read DB
        if isinstance(event, AccountOpenedEvent):
            self.read_database[account_id] += event.initial_deposit
        elif isinstance(event, MoneyDepositedEvent):
            self.read_database[account_id] += event.amount
        elif isinstance(event, MoneyWithdrawnEvent):
            self.read_database[account_id] -= event.amount
            
        print(f"  📊 [Projection] Updated Read DB. {account_id} Balance is now ${self.read_database[account_id]}")

    def query_balance(self, account_id: str) -> int:
        """Lightning fast query. No calculations needed!"""
        return self.read_database.get(account_id, 0)


# ─── 5. Time Travel (Replaying History) ────────────────
# If the Read DB crashes, we can rebuild it from scratch!

def rebuild_state_from_events(events: List[Event]) -> int:
    balance = 0
    for event in events:
        if isinstance(event, AccountOpenedEvent): balance += event.initial_deposit
        elif isinstance(event, MoneyDepositedEvent): balance += event.amount
        elif isinstance(event, MoneyWithdrawnEvent): balance -= event.amount
    return balance


# ─── Demo ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("EVENT SOURCING & CQRS - Bank Account")
    print("=" * 60)
    
    # Setup Infrastructure
    store = EventStore()
    projection = BalanceProjection()
    store.subscribers.append(projection) # Connect the Read Side to the EventStore
    
    # Setup Write API
    service = BankAccountService(store)
    
    print("\n--- Processing Commands (Write Side) ---")
    service.open_account("ACC_123", 500)
    service.deposit("ACC_123", 200)
    service.withdraw("ACC_123", 100)
    service.deposit("ACC_123", 50)
    
    print("\n--- Processing Queries (Read Side) ---")
    # Client asks for balance. It queries the lightning fast Read DB.
    final_balance = projection.query_balance("ACC_123")
    print(f"  🔎 Fast Query Result: ${final_balance}")
    
    print("\n--- Auditing / Time Travel ---")
    # The bank auditors want to know HOW we got that number.
    history = store.get_stream("ACC_123")
    print("  📜 Audit Log:")
    for i, e in enumerate(history):
        print(f"     Step {i+1}: {type(e).__name__} {e}")
        
    print("\n  [Disaster Recovery] Read DB crashed! Rebuilding from Event Store...")
    rebuilt_balance = rebuild_state_from_events(history)
    print(f"  🛠️  Rebuilt Balance: ${rebuilt_balance}")
    
    print("\n✅ Event Sourcing & CQRS demonstrated successfully!")
