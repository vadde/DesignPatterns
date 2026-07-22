"""
============================================================
Example: Payment Gateways & Pythonic Strategies
Pattern: Strategy (Behavioral)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
You have an E-Commerce checkout system. Customers can pay via
Credit Card, PayPal, or Crypto.

Instead of putting all that API logic inside the `ShoppingCart`
class, we inject a Payment Strategy into the cart.

We will show TWO ways to do this in Python:
1. The classic OOP way (Classes)
2. The modern Pythonic way (Functions)

KEY INSIGHT:
------------
The `ShoppingCart` (Context) NEVER changes, no matter how many
new payment methods we invent. It perfectly obeys the Open/Closed Principle.

============================================================
"""

from typing import Callable, Protocol


# ─── Method 1: Classic OOP Strategies ──────────────────

class PaymentStrategy(Protocol):
    """The interface for class-based strategies."""
    def pay(self, amount: float) -> None: ...


class StripeStrategy:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        
    def pay(self, amount: float) -> None:
        print(f"  💳 [Stripe] Processing ${amount:.2f} using API key ending in '...{self.api_key[-4:]}'")


class PayPalStrategy:
    def __init__(self, email: str) -> None:
        self.email = email
        
    def pay(self, amount: float) -> None:
        print(f"  🅿️  [PayPal] Processing ${amount:.2f} for account '{self.email}'")


# ─── Method 2: Pythonic Functional Strategies ──────────

# A strategy can just be a function signature!
FunctionalPaymentStrategy = Callable[[float], None]

def crypto_strategy(amount: float) -> None:
    btc_amount = amount / 60000.0
    print(f"  🪙 [Crypto] Processing {btc_amount:.6f} BTC to wallet '0x1A2B...'")


# ─── The Context ───────────────────────────────────────

class ShoppingCart:
    """
    The Context.
    It takes a strategy (either a class instance or a function)
    and executes it.
    """
    def __init__(self) -> None:
        self.items: list[dict] = []
        self._strategy: PaymentStrategy | FunctionalPaymentStrategy | None = None
        
    def add_item(self, name: str, price: float) -> None:
        self.items.append({"name": name, "price": price})
        
    def set_strategy(self, strategy: PaymentStrategy | FunctionalPaymentStrategy) -> None:
        """Swap the strategy at runtime!"""
        self._strategy = strategy
        
    def checkout(self) -> None:
        if not self._strategy:
            print("  ❌ Cannot checkout: No payment strategy selected!")
            return
            
        total = sum(item["price"] for item in self.items)
        print(f"\n🛒 Checking out {len(self.items)} items. Total: ${total:.2f}")
        
        # Execute the strategy! (Handles both classes and functions)
        if callable(getattr(self._strategy, 'pay', None)):
            self._strategy.pay(total)  # OOP Class
        else:
            self._strategy(total)      # Function


# ─── Demo ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("STRATEGY PATTERN - Payment Gateways")
    print("=" * 60)
    
    cart = ShoppingCart()
    cart.add_item("Mechanical Keyboard", 150.00)
    cart.add_item("Coffee Mug", 20.00)
    
    # 1. Use Stripe
    print("\n--- Paying with Stripe ---")
    stripe = StripeStrategy("sk_live_123456789")
    cart.set_strategy(stripe)
    cart.checkout()
    
    # 2. Swap to PayPal AT RUNTIME
    print("\n--- Swapping to PayPal ---")
    paypal = PayPalStrategy("alice@example.com")
    cart.set_strategy(paypal)
    cart.checkout()
    
    # 3. Use the Pythonic Functional Strategy
    print("\n--- Swapping to Crypto (Function) ---")
    cart.set_strategy(crypto_strategy)
    cart.checkout()
    
    print("\n✅ Strategy pattern demonstrated successfully!")
