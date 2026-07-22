"""
============================================================
Example: Manual DI & Mini DI Container
Pattern: Dependency Injection (Architectural)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
You have a `NotificationService` that needs to fetch users from a
database and send them an SMS message.

Instead of hardcoding `PostgresDatabase()` and `TwilioSMSClient()`
inside the service, we use Dependency Injection.

We will show TWO ways to wire this up:
1. Manual wiring (doing it yourself).
2. Using a basic Dependency Injection Container (IoC).

KEY INSIGHT:
------------
The `NotificationService` ONLY relies on Protocols (Interfaces).
It has zero knowledge of Postgres or Twilio.

============================================================
"""

from typing import Protocol, Type, Any, Callable, Dict


# ─── 1. The Abstractions (Protocols) ───────────────────

class DatabaseProtocol(Protocol):
    def get_phone_number(self, user_id: int) -> str: ...

class SMSClientProtocol(Protocol):
    def send_sms(self, phone: str, message: str) -> None: ...


# ─── 2. The Low-Level Modules (Details) ────────────────

class PostgresDatabase:
    """A concrete implementation of DatabaseProtocol."""
    def get_phone_number(self, user_id: int) -> str:
        print("  [DB] Connecting to Postgres...")
        return f"+1-555-010{user_id}"

class TwilioSMSClient:
    """A concrete implementation of SMSClientProtocol."""
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        
    def send_sms(self, phone: str, message: str) -> None:
        print(f"  [Twilio] Sending '{message}' to {phone} using key {self.api_key[:4]}...")


# ─── 3. The High-Level Module (Business Logic) ─────────

class NotificationService:
    """
    Notice the CONSTRUCTOR INJECTION.
    We ask for the Protocols, not the concrete classes!
    """
    def __init__(self, db: DatabaseProtocol, sms: SMSClientProtocol) -> None:
        self.db = db
        self.sms = sms
        
    def notify_user(self, user_id: int, message: str) -> None:
        print(f"\n--- Notifying User {user_id} ---")
        phone = self.db.get_phone_number(user_id)
        self.sms.send_sms(phone, message)


# ==========================================================
# METHOD 1: Manual Wiring
# ==========================================================

print("=" * 60)
print("DEPENDENCY INJECTION - Manual Wiring")
print("=" * 60)

# We act as the "Mechanic". We build the parts, then assemble the car.
db_instance = PostgresDatabase()
sms_instance = TwilioSMSClient("sk_live_987654321")

# We pass the dependencies IN.
service = NotificationService(db=db_instance, sms=sms_instance)
service.notify_user(1, "Your pizza is ready!")


# ==========================================================
# METHOD 2: Mini DI Container (Inversion of Control)
# ==========================================================
# In complex apps, building 50 objects manually is tedious.
# A DI Container automates the wiring.

class DIContainer:
    """A very basic DI Container."""
    def __init__(self) -> None:
        # Maps a Protocol to a factory function that builds the concrete class
        self._providers: Dict[Type, Callable[[], Any]] = {}
        
    def register(self, protocol: Type, factory: Callable[[], Any]) -> None:
        """Register how to build a certain type."""
        self._providers[protocol] = factory
        
    def resolve(self, protocol: Type) -> Any:
        """Ask the container for an object, and it builds it for you."""
        if protocol not in self._providers:
            raise ValueError(f"No provider registered for {protocol}")
        return self._providers[protocol]()


print("\n" + "=" * 60)
print("DEPENDENCY INJECTION - IoC Container")
print("=" * 60)

container = DIContainer()

# 1. Configuration Phase: Tell the container how to build things
container.register(DatabaseProtocol, lambda: PostgresDatabase())
container.register(SMSClientProtocol, lambda: TwilioSMSClient("sk_live_987654321"))

# 2. Wire up the Service
# We ask the container to resolve the dependencies for us!
container.register(
    NotificationService, 
    lambda: NotificationService(
        db=container.resolve(DatabaseProtocol), 
        sms=container.resolve(SMSClientProtocol)
    )
)

# 3. Execution Phase: Just ask for the finished service!
# (Notice we don't manually build the DB or SMS client here!)
app_service: NotificationService = container.resolve(NotificationService)
app_service.notify_user(2, "Your driver is arriving.")

print("\n✅ Dependency Injection demonstrated successfully!")
