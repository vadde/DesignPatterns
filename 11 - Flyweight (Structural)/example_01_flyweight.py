"""
============================================================
Example: Forest Simulator (Tree Models vs Placements)
Pattern: Flyweight (Structural)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
You are building a game that needs to render a forest with millions
of trees. If every tree contains its own 3D mesh and texture data,
you will run out of RAM instantly.

Solution:
1. Extract the shared data (name, color, texture) into a Flyweight (`TreeModel`).
2. Keep the unique data (x, y coordinates) in a Context class (`Tree`).
3. Use a Factory to ensure we only create one `TreeModel` per type.

KEY INSIGHT:
------------
Notice how `draw()` requires the extrinsic state (canvas, x, y) to
be passed in as arguments. The Flyweight itself has no idea WHERE it is.

============================================================
"""

from typing import Dict, List


# ─── 1. Flyweight (Intrinsic State) ─────────────────────────

class TreeModel:
    """
    The Flyweight. It contains state that is shared across many trees.
    This object should be IMMUTABLE.
    (Imagine `texture` is a massive 10MB byte array).
    """
    def __init__(self, name: str, color: str, texture: str) -> None:
        self.name = name
        self.color = color
        self.texture = texture
        
    def draw(self, canvas: str, x: int, y: int) -> None:
        """
        The operation. It takes the EXTRINSIC state (x, y) as arguments!
        """
        print(f"  🌳 Drawing [{self.name}] colored '{self.color}' at ({x}, {y})")


# ─── 2. Flyweight Factory ──────────────────────────────────

class TreeFactory:
    """
    Manages the Flyweights. Ensures we only ever create ONE instance
    of a specific TreeModel.
    """
    _tree_models: Dict[str, TreeModel] = {}

    @classmethod
    def get_tree_model(cls, name: str, color: str, texture: str) -> TreeModel:
        # Create a unique key for this combination of intrinsic state
        key = f"{name}_{color}_{texture}"
        
        if key not in cls._tree_models:
            print(f"  [Factory] Cache miss: Creating new TreeModel for '{key}'")
            cls._tree_models[key] = TreeModel(name, color, texture)
        else:
            print(f"  [Factory] Cache hit: Returning existing TreeModel for '{key}'")
            
        return cls._tree_models[key]


# ─── 3. Context (Extrinsic State) ──────────────────────────

class Tree:
    """
    The Context. It contains the extrinsic state (x, y) and a reference
    to the Flyweight (model). 
    This object is very lightweight (just a few bytes).
    """
    def __init__(self, x: int, y: int, model: TreeModel) -> None:
        self.x = x
        self.y = y
        self.model = model
        
    def draw(self, canvas: str) -> None:
        # Pass the extrinsic state to the Flyweight
        self.model.draw(canvas, self.x, self.y)


# ─── 4. Client Code ────────────────────────────────────────

class Forest:
    """The client that spawns the objects."""
    def __init__(self) -> None:
        self.trees: List[Tree] = []

    def plant_tree(self, x: int, y: int, name: str, color: str, texture: str) -> None:
        # Get the flyweight from the factory (reuses if it already exists)
        model = TreeFactory.get_tree_model(name, color, texture)
        
        # Create the lightweight context object
        tree = Tree(x, y, model)
        self.trees.append(tree)
        
    def draw(self, canvas: str) -> None:
        for tree in self.trees:
            tree.draw(canvas)


# ─── Demo ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("FLYWEIGHT PATTERN - Forest Simulator")
    print("=" * 60)
    
    forest = Forest()
    
    print("\n  [Planting Oaks]")
    # Plant 3 Oaks. Notice the factory output: 1 cache miss, 2 cache hits.
    forest.plant_tree(10, 20, "Oak", "Green", "oak_texture.png")
    forest.plant_tree(15, 25, "Oak", "Green", "oak_texture.png")
    forest.plant_tree(50, 80, "Oak", "Green", "oak_texture.png")
    
    print("\n  [Planting Pines]")
    # Plant 2 Pines.
    forest.plant_tree(100, 200, "Pine", "Dark Green", "pine_texture.png")
    forest.plant_tree(105, 205, "Pine", "Dark Green", "pine_texture.png")
    
    print("\n  [Drawing the Forest]")
    forest.draw("MainCanvas")
    
    print("\n  [Memory Analysis]")
    num_trees = len(forest.trees)
    num_models = len(TreeFactory._tree_models)
    print(f"  Total Trees (Contexts) created: {num_trees}")
    print(f"  Total TreeModels (Flyweights) in memory: {num_models}")
    
    # We have 5 trees, but only 2 heavy model objects!
    assert num_trees == 5
    assert num_models == 2
    
    # Prove that the oaks share the exact same model instance
    oak1 = forest.trees[0]
    oak2 = forest.trees[1]
    assert oak1.model is oak2.model, "Flyweights are not being shared!"
    
    print("\n✅ Flyweight pattern demonstrated successfully!")
