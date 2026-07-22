"""
============================================================
Example: Coffee Shop (Object Decorator)
Pattern: Decorator (Structural)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
You run a coffee shop. You have a base `Coffee` object. 
Customers can add various condiments: Milk, Whip, Vanilla, Caramel.
Instead of creating a subclass for every combination (`MilkCoffee`,
`MilkVanillaCoffee`, `DoubleWhipCaramelCoffee`), we use decorators.

Each decorator wraps the previous object, adding to its cost
and description.

KEY INSIGHT:
------------
Decorators have the SAME INTERFACE as the objects they decorate.
This allows them to be stacked infinitely.

============================================================
"""

from typing import Protocol


# ─── Component Interface ───────────────────────────────

class Beverage(Protocol):
    """The Component interface that both base beverages and decorators implement."""
    def get_description(self) -> str: ...
    def cost(self) -> float: ...


# ─── Concrete Components (The Base Objects) ────────────

class DarkRoast:
    def get_description(self) -> str:
        return "Dark Roast Coffee"
        
    def cost(self) -> float:
        return 2.50


class Espresso:
    def get_description(self) -> str:
        return "Espresso"
        
    def cost(self) -> float:
        return 1.99


# ─── Decorator Base Class (Optional but helpful) ───────

class CondimentDecorator:
    """
    Base Decorator. 
    It holds the wrapped component and implements the Beverage protocol.
    (In Python, this base class is optional due to duck typing, but it
    makes the pattern explicit).
    """
    def __init__(self, beverage: Beverage) -> None:
        self._beverage = beverage
        
    def get_description(self) -> str:
        return self._beverage.get_description()
        
    def cost(self) -> float:
        return self._beverage.cost()


# ─── Concrete Decorators ───────────────────────────────

class Milk(CondimentDecorator):
    def get_description(self) -> str:
        return f"{self._beverage.get_description()}, Milk"
        
    def cost(self) -> float:
        return self._beverage.cost() + 0.50


class Whip(CondimentDecorator):
    def get_description(self) -> str:
        return f"{self._beverage.get_description()}, Whip"
        
    def cost(self) -> float:
        return self._beverage.cost() + 0.70


class Vanilla(CondimentDecorator):
    def get_description(self) -> str:
        return f"{self._beverage.get_description()}, Vanilla Syrup"
        
    def cost(self) -> float:
        return self._beverage.cost() + 0.30


# ─── Demo ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("DECORATOR PATTERN - Coffee Shop")
    print("=" * 60)
    
    # 1. Plain Espresso
    beverage1 = Espresso()
    print("  [Order 1]")
    print(f"  Description: {beverage1.get_description()}")
    print(f"  Cost: ${beverage1.cost():.2f}")
    
    # 2. Dark Roast with Double Milk and Whip
    print("\n  [Order 2 - Stacking Decorators]")
    beverage2: Beverage = DarkRoast()
    beverage2 = Milk(beverage2)    # Wrap in Milk
    beverage2 = Milk(beverage2)    # Wrap in Milk again (Double Milk)
    beverage2 = Whip(beverage2)    # Wrap in Whip
    
    print(f"  Description: {beverage2.get_description()}")
    print(f"  Cost: ${beverage2.cost():.2f}")
    
    # 3. Espresso with Vanilla and Milk
    print("\n  [Order 3]")
    beverage3 = Milk(Vanilla(Espresso())) # You can nest them inline!
    
    print(f"  Description: {beverage3.get_description()}")
    print(f"  Cost: ${beverage3.cost():.2f}")
    
    print("\n✅ Decorator pattern demonstrated successfully!")
