"""
============================================================
Example: Text Editor Undo/Redo
Pattern: Command (Behavioral)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
You are building a text editor. You need to support Ctrl+Z (Undo)
and Ctrl+Y (Redo).

To do this, every modification to the text cannot just be a simple
string mutation. Instead, every action (typing, deleting, pasting)
must be encapsulated in a `Command` object that knows how to:
1. `execute()`: Apply the change.
2. `undo()`: Reverse the change.

The editor keeps two stacks: a History stack (for undo) and a 
Redo stack.

KEY INSIGHT:
------------
This is the absolute best, textbook use-case for the Command pattern.
A simple Python callback/lambda cannot easily store the state required
to reverse an action. A Command class handles this perfectly.

============================================================
"""

from abc import ABC, abstractmethod


# ─── Receiver ──────────────────────────────────────────

class TextDocument:
    """The Receiver. The object being manipulated."""
    def __init__(self) -> None:
        self.text = ""
        
    def __str__(self) -> str:
        return f"Document: '{self.text}'"


# ─── Command Interface ─────────────────────────────────

class Command(ABC):
    """The Command interface."""
    def __init__(self, document: TextDocument) -> None:
        self.document = document
        
    @abstractmethod
    def execute(self) -> None:
        """Applies the command."""
        pass
        
    @abstractmethod
    def undo(self) -> None:
        """Reverses the command."""
        pass


# ─── Concrete Commands ─────────────────────────────────

class TypeTextCommand(Command):
    def __init__(self, document: TextDocument, text_to_add: str) -> None:
        super().__init__(document)
        self.text_to_add = text_to_add
        
    def execute(self) -> None:
        self.document.text += self.text_to_add
        print(f"  [Command] Typed: '{self.text_to_add}'")
        
    def undo(self) -> None:
        # To undo, we slice off the length of the text we added
        slice_length = len(self.text_to_add)
        self.document.text = self.document.text[:-slice_length]
        print(f"  [Command] Undid typing: removed '{self.text_to_add}'")


class DeleteTextCommand(Command):
    def __init__(self, document: TextDocument, length_to_delete: int) -> None:
        super().__init__(document)
        self.length_to_delete = length_to_delete
        self._deleted_text = ""  # State required for undo!
        
    def execute(self) -> None:
        # Save what we are about to delete so we can undo it later
        if len(self.document.text) >= self.length_to_delete:
            self._deleted_text = self.document.text[-self.length_to_delete:]
            self.document.text = self.document.text[:-self.length_to_delete]
        else:
            self._deleted_text = self.document.text
            self.document.text = ""
            
        print(f"  [Command] Deleted: '{self._deleted_text}'")
        
    def undo(self) -> None:
        # To undo a deletion, we just append the saved text back
        self.document.text += self._deleted_text
        print(f"  [Command] Undid deletion: restored '{self._deleted_text}'")


# ─── Invoker ───────────────────────────────────────────

class TextEditor:
    """The Invoker. Manages command execution and the history stacks."""
    def __init__(self, document: TextDocument) -> None:
        self.document = document
        self.history: list[Command] = []
        self.redo_stack: list[Command] = []
        
    def execute_command(self, command: Command) -> None:
        """Executes a command and pushes it to history."""
        command.execute()
        self.history.append(command)
        # Any new action clears the redo stack!
        self.redo_stack.clear()
        
    def undo(self) -> None:
        """Pops the last command, calls undo(), and pushes to redo stack."""
        if not self.history:
            print("  [Editor] Nothing to undo.")
            return
            
        command = self.history.pop()
        command.undo()
        self.redo_stack.append(command)
        
    def redo(self) -> None:
        """Pops the last undone command, calls execute(), and pushes to history."""
        if not self.redo_stack:
            print("  [Editor] Nothing to redo.")
            return
            
        command = self.redo_stack.pop()
        command.execute()
        self.history.append(command)


# ─── Demo ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("COMMAND PATTERN - Undo/Redo History")
    print("=" * 60)
    
    doc = TextDocument()
    editor = TextEditor(doc)
    
    print("\n--- 1. Typing ---")
    editor.execute_command(TypeTextCommand(doc, "Hello "))
    editor.execute_command(TypeTextCommand(doc, "World!"))
    print(f"Current State: {doc}")
    
    print("\n--- 2. Deleting ---")
    editor.execute_command(DeleteTextCommand(doc, 6)) # Delete "World!"
    print(f"Current State: {doc}")
    
    print("\n--- 3. Undo ---")
    editor.undo() # Restores "World!"
    print(f"Current State: {doc}")
    
    editor.undo() # Removes "Hello "
    print(f"Current State: {doc}")
    
    print("\n--- 4. Redo ---")
    editor.redo() # Types "Hello " again
    print(f"Current State: {doc}")
    
    print("\n--- 5. New Action Clears Redo Stack ---")
    # We still have one thing we *could* redo (World!), but if we type 
    # something new, the redo stack is cleared (standard editor behavior).
    editor.execute_command(TypeTextCommand(doc, "Python!"))
    print(f"Current State: {doc}")
    
    editor.redo() # Should do nothing
    
    print("\n✅ Command pattern (Undo/Redo) demonstrated successfully!")
