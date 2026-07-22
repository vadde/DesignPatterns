"""
============================================================
Example: Video Game Saves
Pattern: Memento (Behavioral)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
You are playing an RPG game. Your character has health, mana,
coordinates, and a list of items.

You encounter a boss and hit "Quick Save" (F5).
You die. You hit "Quick Load" (F9) to restore your state.

KEY INSIGHT:
------------
The `GameCaretaker` manages the save files, but it HAS NO IDEA
what is inside them. Only the `RPGGame` (Originator) knows how
to create and read a `GameMemento`. This perfectly preserves
encapsulation!

============================================================
"""

from dataclasses import dataclass
import copy


# ─── Memento ───────────────────────────────────────────

@dataclass(frozen=True)
class GameMemento:
    """
    The Memento.
    It is completely immutable (frozen). It holds a snapshot of state.
    Notice we don't expose any methods to alter this data.
    """
    name: str  # e.g., "Save 1 - Boss Room"
    health: int
    mana: int
    level: int
    inventory: list[str]


# ─── Originator ────────────────────────────────────────

class RPGGame:
    """
    The Originator.
    This is the actual game. It has complex internal state.
    It is the ONLY class that creates and consumes GameMementos.
    """
    def __init__(self) -> None:
        # Complex internal state
        self._health = 100
        self._mana = 50
        self._level = 1
        self._inventory = ["Sword", "Potion"]
        
    def take_damage(self, amount: int) -> None:
        self._health -= amount
        print(f"  ⚔️  Took {amount} damage! Health is now {self._health}.")
        
    def level_up(self) -> None:
        self._level += 1
        self._health = 100
        self._mana = 50
        print(f"  ✨ Leveled up to {self._level}!")
        
    def loot(self, item: str) -> None:
        self._inventory.append(item)
        print(f"  💰 Looted: {item}")

    def __str__(self) -> str:
        return (f"Game State -> Level: {self._level} | "
                f"HP: {self._health} | MP: {self._mana} | "
                f"Inv: {self._inventory}")

    # --- Memento Logic ---

    def save_game(self, save_name: str) -> GameMemento:
        """Creates a snapshot of the current state."""
        print(f"  💾 Saving game: '{save_name}'...")
        # Note: We must DEEP COPY mutable objects like lists!
        return GameMemento(
            name=save_name,
            health=self._health,
            mana=self._mana,
            level=self._level,
            inventory=copy.deepcopy(self._inventory)
        )
        
    def load_game(self, memento: GameMemento) -> None:
        """Restores the state from a snapshot."""
        print(f"  🔄 Loading game: '{memento.name}'...")
        self._health = memento.health
        self._mana = memento.mana
        self._level = memento.level
        self._inventory = copy.deepcopy(memento.inventory)


# ─── Caretaker ─────────────────────────────────────────

class GameCaretaker:
    """
    The Caretaker.
    It manages the save files (mementos), but NEVER looks inside them.
    It just holds onto them and gives them back to the Game when asked.
    """
    def __init__(self, game: RPGGame) -> None:
        self._game = game
        self._saves: list[GameMemento] = []
        
    def quick_save(self) -> None:
        save_name = f"QuickSave_Slot_{len(self._saves) + 1}"
        memento = self._game.save_game(save_name)
        self._saves.append(memento)
        
    def quick_load(self) -> None:
        if not self._saves:
            print("  ❌ No save files found!")
            return
            
        memento = self._saves.pop()  # Load the most recent save
        self._game.load_game(memento)


# ─── Demo ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("MEMENTO PATTERN - Video Game Saves")
    print("=" * 60)
    
    game = RPGGame()
    caretaker = GameCaretaker(game)
    
    print("\n[Starting Game]")
    print(f"  {game}")
    
    print("\n[Progressing...]")
    game.level_up()
    game.loot("Dragon Shield")
    print(f"  {game}")
    
    print("\n[Before Boss Room - Quick Save!]")
    caretaker.quick_save()
    
    print("\n[Fighting Boss...]")
    game.take_damage(80)
    game.loot("Cursed Ring")
    print(f"  {game}")
    game.take_damage(50) # Dead!
    print(f"  {game} (DEAD!)")
    
    print("\n[Rage Quit & Quick Load!]")
    caretaker.quick_load()
    print(f"  {game}")
    
    print("\n✅ Memento pattern demonstrated successfully!")
