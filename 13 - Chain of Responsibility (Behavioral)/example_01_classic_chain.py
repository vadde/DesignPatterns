"""
============================================================
Example: Customer Support Chain (Classic GoF)
Pattern: Chain of Responsibility (Behavioral)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
A customer submits a support ticket with a certain severity.
- Severity 1 (Low): Handled by a Chatbot.
- Severity 2 (Medium): Handled by a Human Agent.
- Severity 3 (High): Handled by a Manager.

The client just sends the ticket to the first handler. If that
handler can't process it, it passes it down the chain. The FIRST
handler that can resolve the ticket does so, and the chain stops.

KEY INSIGHT:
------------
Notice the `BaseHandler` class. It implements the boilerplate for
managing the linked list (`set_next`). The concrete handlers only
need to implement the `handle()` logic.

============================================================
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class SupportTicket:
    id: int
    severity: int
    description: str


# ─── Handler Interface / Base Class ─────────────────────

class Handler(ABC):
    """
    The interface and base class for the Chain.
    It manages the `_next_handler` reference.
    """
    def __init__(self) -> None:
        self._next_handler: Optional["Handler"] = None
        
    def set_next(self, handler: "Handler") -> "Handler":
        """
        Sets the next handler in the chain.
        Returning the handler allows for a fluent interface:
        h1.set_next(h2).set_next(h3)
        """
        self._next_handler = handler
        return handler
        
    @abstractmethod
    def handle(self, ticket: SupportTicket) -> Optional[str]:
        """
        If this handler can't process the ticket, it delegates 
        to the next handler (if one exists).
        """
        if self._next_handler:
            return self._next_handler.handle(ticket)
        
        # End of the chain, no one handled it
        return None


# ─── Concrete Handlers ──────────────────────────────────

class ChatbotHandler(Handler):
    def handle(self, ticket: SupportTicket) -> Optional[str]:
        if ticket.severity == 1:
            print(f"  🤖 [Chatbot] Handling ticket {ticket.id}: {ticket.description}")
            return f"Chatbot resolved ticket {ticket.id} automatically."
        
        # Not severity 1, pass it down the chain!
        print(f"  🤖 [Chatbot] Cannot handle severity {ticket.severity}. Passing to Agent...")
        return super().handle(ticket)


class HumanAgentHandler(Handler):
    def handle(self, ticket: SupportTicket) -> Optional[str]:
        if ticket.severity == 2:
            print(f"  🧑‍💼 [Human Agent] Handling ticket {ticket.id}: {ticket.description}")
            return f"Agent resolved ticket {ticket.id}."
            
        print(f"  🧑‍💼 [Human Agent] Cannot handle severity {ticket.severity}. Passing to Manager...")
        return super().handle(ticket)


class ManagerHandler(Handler):
    def handle(self, ticket: SupportTicket) -> Optional[str]:
        if ticket.severity >= 3:
            print(f"  👔 [Manager] Handling urgent ticket {ticket.id}: {ticket.description}")
            return f"Manager resolved urgent ticket {ticket.id}."
            
        return super().handle(ticket)


# ─── Demo ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("CHAIN OF RESPONSIBILITY - Classic (Support Tickets)")
    print("=" * 60)
    
    # 1. Instantiate the handlers
    chatbot = ChatbotHandler()
    agent = HumanAgentHandler()
    manager = ManagerHandler()
    
    # 2. Wire the chain together: Chatbot -> Agent -> Manager
    chatbot.set_next(agent).set_next(manager)
    
    # 3. Create some tickets
    tickets = [
        SupportTicket(101, 1, "How do I reset my password?"),
        SupportTicket(102, 2, "I was overcharged on my last bill."),
        SupportTicket(103, 3, "Production server is ON FIRE!"),
        SupportTicket(104, 0, "Wait, severity 0?"), # An unhandled case
    ]
    
    # 4. Client just sends all tickets to the FRONT of the chain (chatbot)
    for ticket in tickets:
        print(f"\n--- Submitting Ticket {ticket.id} (Severity {ticket.severity}) ---")
        result = chatbot.handle(ticket)
        
        if result:
            print(f"  ✅ Result: {result}")
        else:
            print(f"  ❌ UNHANDLED: No one in the chain could handle ticket {ticket.id}!")
            
    print("\n✅ Chain of Responsibility demonstrated successfully!")
