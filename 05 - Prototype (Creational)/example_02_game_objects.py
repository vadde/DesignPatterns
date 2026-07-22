"""
============================================================
Example: Game Object Prototypes Registry
Pattern: Prototype (Creational)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
A game engine needs to spawn thousands of enemies, items, and
terrain tiles. Each type starts from a prototype (template) with
base stats, then gets randomized variations. Building each from
scratch with full initialization (loading sprites, calculating
stats) is too slow. Clone and customize instead.

KEY INSIGHT:
------------
A prototype registry (like a spawner catalog) lets you register
base objects once, then rapidly clone + customize. This is how
real game engines handle object pooling and spawning.

============================================================
"""

import copy
import random
from dataclasses import dataclass, field


@dataclass
class Stats:
    health: int
    attack: int
    defense: int
    speed: float


@dataclass
class GameObject:
    name: str
    category: str
    stats: Stats
    abilities: list[str] = field(default_factory=list)
    loot_table: dict[str, float] = field(default_factory=dict)
    position: tuple[float, float] = (0.0, 0.0)

    def clone(self) -> "GameObject":
        return copy.deepcopy(self)

    def randomize(self, variance: float = 0.2) -> "GameObject":
        """Add random variance to stats (for mob variety)."""
        s = self.stats
        factor = lambda: 1.0 + random.uniform(-variance, variance)
        self.stats = Stats(
            health=int(s.health * factor()),
            attack=int(s.attack * factor()),
            defense=int(s.defense * factor()),
            speed=round(s.speed * factor(), 1),
        )
        return self

    def __str__(self) -> str:
        s = self.stats
        return (
            f"{self.name} [{self.category}] "
            f"HP:{s.health} ATK:{s.attack} DEF:{s.defense} SPD:{s.speed} "
            f"@ {self.position}"
        )


class GameObjectSpawner:
    """Prototype registry — stores base prototypes, spawns clones."""

    _prototypes: dict[str, GameObject] = {}

    @classmethod
    def register(cls, key: str, prototype: GameObject) -> None:
        cls._prototypes[key] = prototype

    @classmethod
    def spawn(
        cls,
        key: str,
        position: tuple[float, float] = (0.0, 0.0),
        randomize: bool = True,
    ) -> GameObject:
        if key not in cls._prototypes:
            raise ValueError(f"Unknown prototype: '{key}'")
        obj = cls._prototypes[key].clone()
        obj.position = position
        if randomize:
            obj.randomize()
        return obj

    @classmethod
    def spawn_group(
        cls,
        key: str,
        count: int,
        area: tuple[float, float, float, float],
    ) -> list[GameObject]:
        """Spawn multiple clones in a rectangular area."""
        x_min, y_min, x_max, y_max = area
        return [
            cls.spawn(
                key,
                position=(
                    round(random.uniform(x_min, x_max), 1),
                    round(random.uniform(y_min, y_max), 1),
                ),
            )
            for _ in range(count)
        ]


# ─── Register prototypes ──────────────────────────
GameObjectSpawner.register("goblin", GameObject(
    name="Goblin",
    category="enemy",
    stats=Stats(health=50, attack=10, defense=5, speed=1.2),
    abilities=["slash", "dodge"],
    loot_table={"gold": 0.8, "potion": 0.3, "dagger": 0.05},
))

GameObjectSpawner.register("dragon", GameObject(
    name="Dragon",
    category="boss",
    stats=Stats(health=500, attack=80, defense=40, speed=0.8),
    abilities=["fire_breath", "tail_swipe", "fly"],
    loot_table={"gold": 1.0, "legendary_sword": 0.1, "dragon_scale": 0.5},
))

GameObjectSpawner.register("health_potion", GameObject(
    name="Health Potion",
    category="item",
    stats=Stats(health=0, attack=0, defense=0, speed=0),
    abilities=["heal_50"],
    loot_table={},
))


# ─── Demo ──────────────────────────────────────────
if __name__ == "__main__":
    random.seed(42)  # For reproducible demo output

    print("=" * 60)
    print("PROTOTYPE — Game Object Spawner")
    print("=" * 60)

    # Spawn individual enemies
    print("\n  --- Single Spawns ---")
    g1 = GameObjectSpawner.spawn("goblin", position=(10.0, 20.0))
    g2 = GameObjectSpawner.spawn("goblin", position=(15.0, 22.0))
    boss = GameObjectSpawner.spawn("dragon", position=(100.0, 100.0))
    print(f"  {g1}")
    print(f"  {g2}")
    print(f"  {boss}")

    # Verify independence (different stats due to randomization)
    assert g1.stats.health != g2.stats.health or g1.stats.attack != g2.stats.attack, \
        "Clones should have randomized stats"
    assert g1.position != g2.position, "Clones at different positions"

    # Spawn a group of goblins in an area
    print("\n  --- Group Spawn (5 goblins) ---")
    patrol = GameObjectSpawner.spawn_group("goblin", 5, (0, 0, 50, 50))
    for g in patrol:
        print(f"  {g}")

    # Verify prototype is unmodified
    print("\n  --- Prototype integrity check ---")
    proto = GameObjectSpawner._prototypes["goblin"]
    print(f"  Original prototype: {proto}")
    assert proto.stats.health == 50, "Prototype should be unchanged!"
    assert proto.position == (0.0, 0.0), "Prototype position unchanged!"

    # Items don't need randomization
    print("\n  --- Item spawn (no randomization) ---")
    potion = GameObjectSpawner.spawn("health_potion", position=(5, 5), randomize=False)
    print(f"  {potion}")

    print("\n✅ Game Object Spawner demonstrated successfully!")
