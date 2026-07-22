"""
============================================================
Example: Pythonic Event Emitter
Pattern: Observer (Behavioral)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
You have a `ShoppingCart` object. When a user completes checkout,
several things need to happen:
1. Send an email receipt.
2. Update inventory.
3. Log the transaction.

Instead of writing all that logic inside `ShoppingCart.checkout()`,
we make the Cart an "Event Emitter" (Subject). It just broadcasts
the "checkout_complete" event. Other systems subscribe to this event.

KEY INSIGHT:
------------
Instead of using full classes for Observers (like the GoF book),
we use Python's first-class functions (callbacks). This is the
standard way to write Observers in modern Python.

============================================================
"""

from typing import Any, Callable, Dict, List

# Type alias for our observer callbacks
ObserverCallback = Callable[[Dict[str, Any]], None]


# ─── Subject (Publisher / Event Emitter) ───────────────

class EventEmitter:
    """
    A generic Publisher that can handle multiple types of events.
    (Very similar to Node.js EventEmitter).
    """
    def __init__(self) -> None:
        # A dictionary mapping event names to lists of callbacks
        self._events: Dict[str, List[ObserverCallback]] = {}
        
    def on(self, event_name: str, callback: ObserverCallback) -> None:
        """Subscribe to an event (Attach)."""
        if event_name not in self._events:
            self._events[event_name] = []
        self._events[event_name].append(callback)
        print(f"  [System] Attached callback '{callback.__name__}' to event '{event_name}'")
        
    def off(self, event_name: str, callback: ObserverCallback) -> None:
        """Unsubscribe from an event (Detach)."""
        if event_name in self._events and callback in self._events[event_name]:
            self._events[event_name].remove(callback)
            print(f"  [System] Detached callback '{callback.__name__}' from event '{event_name}'")
            
    def emit(self, event_name: str, event_data: Dict[str, Any]) -> None:
        """Broadcast an event to all subscribers (Notify)."""
        if event_name in self._events:
            print(f"\n  📢 [EventEmitter] Broadcasting '{event_name}'...")
            for callback in self._events[event_name]:
                callback(event_data)


# ─── Concrete Subject (The Shopping Cart) ──────────────

class ShoppingCart(EventEmitter):
    """
    Our specific business logic class. It inherits the emit/on methods.
    """
    def __init__(self, user_id: str) -> None:
        super().__init__()
        self.user_id = user_id
        self.items: List[str] = []
        
    def add_item(self, item: str) -> None:
        self.items.append(item)
        
    def checkout(self) -> None:
        print(f"\n  🛒 [Cart] {self.user_id} is checking out with {self.items}...")
        
        # We do NOT send emails or update inventory here!
        # We just EMIT the event and let the observers handle the rest.
        
        event_data = {
            "user_id": self.user_id,
            "items": self.items,
            "total_items": len(self.items)
        }
        self.emit("checkout_complete", event_data)
        
        self.items.clear()


# ─── Observers (Just plain functions!) ─────────────────

def send_email_receipt(data: Dict[str, Any]) -> None:
    print(f"  ✉️  [EmailService] Sending receipt to {data['user_id']} for {data['total_items']} items.")

def update_inventory(data: Dict[str, Any]) -> None:
    print(f"  📦 [InventoryService] Deducting stock for: {data['items']}")

def log_transaction(data: Dict[str, Any]) -> None:
    print(f"  📝 [Logger] Transaction logged: User {data['user_id']} bought {data['total_items']} items.")


# ─── Demo ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("OBSERVER PATTERN - Pythonic Event Emitter")
    print("=" * 60)
    
    # 1. Setup the Subject
    cart = ShoppingCart("Alice")
    
    # 2. Attach Observers (Wire up the app)
    cart.on("checkout_complete", send_email_receipt)
    cart.on("checkout_complete", update_inventory)
    cart.on("checkout_complete", log_transaction)
    
    # 3. Use the app!
    cart.add_item("Laptop")
    cart.add_item("Mouse")
    
    # When checkout runs, it will trigger all 3 observers automatically.
    cart.checkout()
    
    # 4. Detach an observer (Alice opts out of emails)
    print("\n[Detaching Email Service]")
    cart.off("checkout_complete", send_email_receipt)
    
    cart.add_item("Keyboard")
    cart.checkout() # Only Inventory and Logger will run this time!
    
    print("\n✅ Observer pattern demonstrated successfully!")
