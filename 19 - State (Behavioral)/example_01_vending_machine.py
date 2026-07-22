"""
============================================================
Example: Vending Machine FSM
Pattern: State (Behavioral)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
A Vending Machine has 3 states:
1. NoCoinState
2. HasCoinState
3. DispensingState

If you press "Dispense" while in NoCoinState, it errors.
If you insert a coin while in HasCoinState, it refunds the extra coin.
Instead of having massive `if/else` blocks in the VendingMachine,
we put the logic inside the State classes themselves.

KEY INSIGHT:
------------
The State objects have a reference back to the Context (VendingMachine).
This allows them to call `self.machine.set_state(...)` to trigger
transitions.

============================================================
"""

from abc import ABC, abstractmethod


# ─── Context ───────────────────────────────────────────

class VendingMachine:
    """
    The Context. It maintains a reference to the current state.
    It delegates all work to the state object.
    """
    def __init__(self, inventory_count: int) -> None:
        self.inventory_count = inventory_count
        # Start in the NoCoinState
        self._state: State = NoCoinState(self)
        
    def set_state(self, state: 'State') -> None:
        """Called by the States to trigger transitions."""
        print(f"  🔄 [Transition] Changing state to: {type(state).__name__}")
        self._state = state
        
    # Expose the API to the user, but delegate to the state!
    def insert_coin(self) -> None:
        self._state.insert_coin()
        
    def eject_coin(self) -> None:
        self._state.eject_coin()
        
    def press_button(self) -> None:
        self._state.press_button()
        
    def dispense(self) -> None:
        self._state.dispense()


# ─── State Interface ───────────────────────────────────

class State(ABC):
    """
    Base State class. Every state must know about the Context
    so it can trigger transitions.
    """
    def __init__(self, machine: VendingMachine) -> None:
        self.machine = machine
        
    @abstractmethod
    def insert_coin(self) -> None: pass
    @abstractmethod
    def eject_coin(self) -> None: pass
    @abstractmethod
    def press_button(self) -> None: pass
    @abstractmethod
    def dispense(self) -> None: pass


# ─── Concrete States ───────────────────────────────────

class NoCoinState(State):
    def insert_coin(self) -> None:
        print("  🪙 Coin inserted.")
        # TRANSITION!
        self.machine.set_state(HasCoinState(self.machine))
        
    def eject_coin(self) -> None:
        print("  ❌ Cannot eject. You haven't inserted a coin.")
        
    def press_button(self) -> None:
        print("  ❌ Cannot dispense. Insert a coin first.")
        
    def dispense(self) -> None:
        print("  ❌ Pay first!")


class HasCoinState(State):
    def insert_coin(self) -> None:
        print("  ❌ You already inserted a coin. Returning extra coin.")
        
    def eject_coin(self) -> None:
        print("  🪙 Coin returned.")
        # TRANSITION!
        self.machine.set_state(NoCoinState(self.machine))
        
    def press_button(self) -> None:
        print("  🟩 Button pressed...")
        if self.machine.inventory_count > 0:
            # TRANSITION!
            self.machine.set_state(DispensingState(self.machine))
            # Trigger the internal dispense action immediately
            self.machine.dispense()
        else:
            print("  ❌ Out of stock! Returning coin.")
            self.machine.set_state(NoCoinState(self.machine))
            
    def dispense(self) -> None:
        print("  ❌ Press the button first.")


class DispensingState(State):
    def insert_coin(self) -> None:
        print("  ❌ Please wait, already dispensing.")
        
    def eject_coin(self) -> None:
        print("  ❌ Sorry, you already pressed the button.")
        
    def press_button(self) -> None:
        print("  ❌ Already dispensing!")
        
    def dispense(self) -> None:
        print("  🍬 Dispensing candy!")
        self.machine.inventory_count -= 1
        print(f"  [Inventory: {self.machine.inventory_count} left]")
        # TRANSITION! (Back to start)
        self.machine.set_state(NoCoinState(self.machine))


# ─── Demo ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("STATE PATTERN - Vending Machine")
    print("=" * 60)
    
    machine = VendingMachine(inventory_count=2)
    
    print("\n--- Scenario 1: Successful Purchase ---")
    machine.insert_coin()
    machine.press_button()
    
    print("\n--- Scenario 2: Try to break it ---")
    machine.press_button() # No coin!
    machine.insert_coin()
    machine.insert_coin() # Double coin!
    machine.eject_coin()  # Changed mind
    
    print("\n--- Scenario 3: Buy last item & Out of stock ---")
    machine.insert_coin()
    machine.press_button() # Buys the 2nd (last) item
    
    machine.insert_coin()
    machine.press_button() # Fails gracefully!
    
    print("\n✅ State pattern demonstrated successfully!")
