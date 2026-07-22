"""
============================================================
Example: Composition vs Inheritance — Side-by-Side
Pattern: Foundations
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
We're building a notification system for an e-commerce platform.
Notifications can be sent via Email, SMS, or Push. They can also
be urgent, scheduled, or batched. With inheritance, this creates
a combinatorial explosion of subclasses. With composition, it's
clean and extensible.

KEY INSIGHT:
------------
Inheritance creates a rigid hierarchy that explodes with every
new axis of variation. Composition lets you mix and match
behaviors like LEGO bricks — independently and at runtime.

============================================================
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


# ════════════════════════════════════════════════════════════
# ❌ INHERITANCE APPROACH — The Combinatorial Explosion
# ════════════════════════════════════════════════════════════

# Level 1: Base
class NotificationBad(ABC):
    @abstractmethod
    def send(self, message: str) -> None: ...


# Level 2: Channel (3 subclasses)
class EmailNotificationBad(NotificationBad):
    def send(self, message: str) -> None:
        print(f"  📧 Email: {message}")


class SMSNotificationBad(NotificationBad):
    def send(self, message: str) -> None:
        print(f"  📱 SMS: {message}")


class PushNotificationBad(NotificationBad):
    def send(self, message: str) -> None:
        print(f"  🔔 Push: {message}")


# Level 3: Urgency × Channel = 6 MORE subclasses (explosion begins!)
class UrgentEmailNotificationBad(EmailNotificationBad):
    def send(self, message: str) -> None:
        print(f"  🚨📧 URGENT Email: {message}")


class UrgentSMSNotificationBad(SMSNotificationBad):
    def send(self, message: str) -> None:
        print(f"  🚨📱 URGENT SMS: {message}")


class ScheduledEmailNotificationBad(EmailNotificationBad):
    def send(self, message: str) -> None:
        print(f"  ⏰📧 Scheduled Email: {message}")


# ... and it keeps growing:
# BatchedEmailNotificationBad, BatchedSMSNotificationBad,
# ScheduledPushNotificationBad, UrgentBatchedEmailNotificationBad...
#
# With 3 channels × 3 urgency types × 3 delivery modes = 27 classes!
# Add logging? 54 classes. Add encryption? 108 classes. 💀

# ════════════════════════════════════════════════════════════
# ✅ COMPOSITION APPROACH — Mix and Match Like LEGO
# ════════════════════════════════════════════════════════════

# ─── Step 1: Define small, focused behaviors (protocols) ──

@runtime_checkable
class Channel(Protocol):
    """HOW to deliver the notification."""
    def deliver(self, message: str) -> None: ...


@runtime_checkable
class UrgencyFormatter(Protocol):
    """HOW to format the urgency."""
    def format(self, message: str) -> str: ...


class DeliveryMode(Protocol):
    """WHEN to deliver the notification."""
    def schedule(self, message: str) -> str: ...


# ─── Step 2: Implement each axis independently ────────────

# Channels (3 classes)
class EmailChannel:
    def deliver(self, message: str) -> None:
        print(f"  📧 Email: {message}")


class SMSChannel:
    def deliver(self, message: str) -> None:
        print(f"  📱 SMS: {message}")


class PushChannel:
    def deliver(self, message: str) -> None:
        print(f"  🔔 Push: {message}")


# Urgency Formatters (3 classes)
class NormalUrgency:
    def format(self, message: str) -> str:
        return message


class UrgentUrgency:
    def format(self, message: str) -> str:
        return f"🚨 URGENT: {message}"


class LowPriorityUrgency:
    def format(self, message: str) -> str:
        return f"ℹ️ FYI: {message}"


# Delivery Modes (3 classes)
class ImmediateDelivery:
    def schedule(self, message: str) -> str:
        return f"[NOW] {message}"


class ScheduledDelivery:
    def schedule(self, message: str) -> str:
        return f"[SCHEDULED 9AM] {message}"


class BatchedDelivery:
    def schedule(self, message: str) -> str:
        return f"[BATCHED] {message}"


# ─── Step 3: Compose them ─────────────────────────────────

@dataclass
class Notification:
    """
    Composes channel + urgency + delivery mode.

    Instead of 27+ subclasses, we have:
    - 3 channels + 3 urgency types + 3 delivery modes = 9 classes
    - And 3 × 3 × 3 = 27 COMBINATIONS without any new classes!

    Adding a new channel? Just 1 new class (not N × M new subclasses).
    """
    channel: Channel
    urgency: UrgencyFormatter
    delivery: DeliveryMode

    def send(self, message: str) -> None:
        formatted = self.urgency.format(message)
        scheduled = self.delivery.schedule(formatted)
        self.channel.deliver(scheduled)


# ════════════════════════════════════════════════════════════
# COMPARISON TABLE (printed at runtime)
# ════════════════════════════════════════════════════════════

COMPARISON = """
╔══════════════════════════╦══════════════════════════════╗
║     INHERITANCE          ║     COMPOSITION              ║
╠══════════════════════════╬══════════════════════════════╣
║ 27+ classes for 3×3×3    ║ 9 classes + 1 compositor     ║
║ Adding channel = N new   ║ Adding channel = 1 new class ║
║ Fixed at class definition║ Swappable at runtime         ║
║ Deep hierarchy = fragile ║ Flat, independent components ║
║ Hard to test in isolation║ Each component testable alone ║
╚══════════════════════════╩══════════════════════════════╝
"""


# ════════════════════════════════════════════════════════════
# DEMO
# ════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("❌ INHERITANCE APPROACH")
    print("=" * 60)
    print("  (Showing just 3 of the 27+ subclasses needed)")
    EmailNotificationBad().send("Your order shipped!")
    UrgentEmailNotificationBad().send("Payment failed!")
    ScheduledEmailNotificationBad().send("Weekly digest")
    print()

    print("=" * 60)
    print("✅ COMPOSITION APPROACH")
    print("=" * 60)
    print("  (Same 3 combinations — ZERO new subclasses)")

    # Combination 1: Normal email, immediate
    n1 = Notification(
        channel=EmailChannel(),
        urgency=NormalUrgency(),
        delivery=ImmediateDelivery(),
    )
    n1.send("Your order shipped!")

    # Combination 2: Urgent email, immediate
    n2 = Notification(
        channel=EmailChannel(),
        urgency=UrgentUrgency(),
        delivery=ImmediateDelivery(),
    )
    n2.send("Payment failed!")

    # Combination 3: Normal email, scheduled
    n3 = Notification(
        channel=EmailChannel(),
        urgency=NormalUrgency(),
        delivery=ScheduledDelivery(),
    )
    n3.send("Weekly digest")

    print()
    print("  🔄 Runtime swap — same Notification, different channel:")
    # Swap channel at RUNTIME — impossible with inheritance!
    n4 = Notification(
        channel=SMSChannel(),
        urgency=UrgentUrgency(),
        delivery=ImmediateDelivery(),
    )
    n4.send("Server is down!")

    n5 = Notification(
        channel=PushChannel(),
        urgency=LowPriorityUrgency(),
        delivery=BatchedDelivery(),
    )
    n5.send("New blog post available")

    print()
    print(COMPARISON)

    # Verify that our objects satisfy the protocols
    assert isinstance(EmailChannel(), Channel)  # type: ignore[arg-type]
    assert isinstance(UrgentUrgency(), UrgencyFormatter)  # type: ignore[arg-type]

    print("✅ Composition vs Inheritance demonstrated successfully!")
