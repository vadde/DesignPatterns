"""
============================================================
Example: Class Adapter (Multiple Inheritance)
Pattern: Adapter (Structural)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
You have a notification system that expects objects to have a
`send_alert(msg)` method. You have a third-party `TwilioSMS`
class that has a `dispatch_text_message(text)` method.

Instead of wrapping the Twilio object (Object Adapter), you create
a new class that inherits from BOTH the target interface and the
third-party class.

KEY INSIGHT:
------------
This is the "Class Adapter" pattern. It relies on Multiple Inheritance,
which is natively supported in Python. It does not require wrapping an
instance, but it tightly couples the adapter to the specific Adaptee class.
Because it uses inheritance, it cannot adapt subclasses of the Adaptee.

============================================================
"""

from typing import Protocol

# ─── Target (The interface the client expects) ─────────

class AlertSystem(Protocol):
    """The interface our system uses to send alerts."""
    def send_alert(self, message: str) -> None: ...


# ─── Client ────────────────────────────────────────────

def notify_admin(alerter: AlertSystem, message: str) -> None:
    """Client function that relies on the AlertSystem interface."""
    print("  🚨 System issue detected! Triggering alert...")
    alerter.send_alert(message)


# ─── Adaptee (The 3rd party class) ─────────────────────

class TwilioSMS:
    """Third-party SMS service with an incompatible API."""
    
    def dispatch_text_message(self, text: str) -> None:
        print(f"  📱 [Twilio API] Dispatching SMS: '{text}'")


# ─── Adapter (The bridge via Multiple Inheritance) ─────

class TwilioClassAdapter(TwilioSMS):
    """
    Class Adapter using MULTIPLE INHERITANCE (implicit Protocol implementation).
    
    Inherits from the Adaptee (TwilioSMS).
    Implements the Target interface (`send_alert`).
    """
    
    def send_alert(self, message: str) -> None:
        """Translates the Target interface to the Adaptee interface."""
        print("  🔌 Class Adapter intercepting send_alert()...")
        # Because we INHERIT from TwilioSMS, we just call `self`
        formatted_msg = f"URGENT: {message}"
        self.dispatch_text_message(formatted_msg)


# ─── Demo ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("CLASS ADAPTER (Multiple Inheritance)")
    print("=" * 60)
    
    # We instantiate the ADAPTER directly.
    # We don't create a TwilioSMS object and pass it in.
    adapter = TwilioClassAdapter()
    
    # The client works with the adapter seamlessly
    notify_admin(adapter, "Database connection lost!")
    
    print()
    print("  Note: TwilioClassAdapter is a subclass of TwilioSMS.")
    print(f"  isinstance(adapter, TwilioSMS): {isinstance(adapter, TwilioSMS)}")
    
    print("\n✅ Class Adapter demonstrated successfully!")
