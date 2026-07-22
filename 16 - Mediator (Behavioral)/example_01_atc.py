"""
============================================================
Example: Air Traffic Control
Pattern: Mediator (Behavioral)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
Airplanes (Components) need to coordinate landing on a single
Runway. If Airplane A talks directly to Airplane B, Airplane C,
and the Runway, the code becomes tightly coupled spaghetti.

Instead, every Airplane communicates ONLY with the Control Tower
(Mediator). The Control Tower contains the logic to decide who
can land and when.

KEY INSIGHT:
------------
The `Airplane` class does not know about the `Runway` or other
`Airplanes`. It only knows about the `ControlTowerProtocol`.

============================================================
"""

from typing import Protocol


# ─── Mediator Interface ────────────────────────────────

class ControlTowerProtocol(Protocol):
    """The interface that Components use to talk to the Mediator."""
    def notify(self, sender: 'Airplane', event: str) -> None: ...


# ─── Components ────────────────────────────────────────

class Airplane:
    """
    A Component. It only knows about the Mediator.
    It does NOT know about other airplanes or the runway.
    """
    def __init__(self, flight_number: str) -> None:
        self.flight_number = flight_number
        self.mediator: ControlTowerProtocol | None = None
        
    def set_mediator(self, mediator: ControlTowerProtocol) -> None:
        self.mediator = mediator
        
    def request_landing(self) -> None:
        print(f"  ✈️  [Flight {self.flight_number}] Requesting landing clearance...")
        if self.mediator:
            self.mediator.notify(self, "request_landing")
            
    def finish_landing(self) -> None:
        print(f"  ✈️  [Flight {self.flight_number}] Has landed and cleared the runway.")
        if self.mediator:
            self.mediator.notify(self, "landed")


class Runway:
    """Another Component."""
    def __init__(self) -> None:
        self.is_clear = True


# ─── Concrete Mediator ─────────────────────────────────

class JFKControlTower:
    """
    The Concrete Mediator.
    It knows about all the components (Runway, Airplanes) and
    contains the complex business logic of how they interact.
    """
    def __init__(self) -> None:
        self.runway = Runway()
        self.waiting_queue: list[Airplane] = []
        
    def notify(self, sender: Airplane, event: str) -> None:
        """The central hub for all communication."""
        
        if event == "request_landing":
            if self.runway.is_clear:
                print(f"  🗼 [Tower] Runway is clear. Flight {sender.flight_number}, you are cleared to land.")
                self.runway.is_clear = False
            else:
                print(f"  🗼 [Tower] Runway is busy! Flight {sender.flight_number}, please hold.")
                self.waiting_queue.append(sender)
                
        elif event == "landed":
            self.runway.is_clear = True
            
            # If someone is waiting, clear them to land now
            if self.waiting_queue:
                next_flight = self.waiting_queue.pop(0)
                print(f"  🗼 [Tower] Runway now clear. Flight {next_flight.flight_number}, you are cleared to land.")
                self.runway.is_clear = False


# ─── Demo ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("MEDIATOR PATTERN - Air Traffic Control")
    print("=" * 60)
    
    # 1. Create the Mediator
    tower = JFKControlTower()
    
    # 2. Create the Components
    flight1 = Airplane("AA101")
    flight2 = Airplane("DL404")
    flight3 = Airplane("UA909")
    
    # 3. Connect components to the Mediator
    flight1.set_mediator(tower)
    flight2.set_mediator(tower)
    flight3.set_mediator(tower)
    
    # 4. Action!
    # Flight 1 requests to land. Runway is clear.
    flight1.request_landing()
    
    # Flight 2 requests to land. Runway is busy, so it holds.
    flight2.request_landing()
    
    # Flight 3 requests to land. Runway is busy, so it holds.
    flight3.request_landing()
    
    # Flight 1 finishes landing. The tower automatically notifies Flight 2.
    flight1.finish_landing()
    
    # Flight 2 finishes landing. The tower automatically notifies Flight 3.
    flight2.finish_landing()
    
    flight3.finish_landing()
    
    print("\n✅ Mediator pattern demonstrated successfully!")
