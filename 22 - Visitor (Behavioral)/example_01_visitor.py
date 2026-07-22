"""
============================================================
Example: Shape Exporter (Classic GoF vs SingleDispatch)
Pattern: Visitor (Behavioral)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
You have a drawing app with `Dot`, `Circle`, and `Rectangle` objects.
You need to add a feature to export these shapes to XML. Later, you
need to export them to JSON.

Instead of adding `export_xml()` and `export_json()` to every shape
(which bloats the shape classes), we create a `Visitor` that extracts
the data from the shapes.

KEY INSIGHT:
------------
We will show TWO methods:
1. The Classic GoF approach (Double Dispatch via `accept()`).
2. The modern Pythonic approach (using `@singledispatch`).

============================================================
"""

from typing import Protocol
from functools import singledispatch


# ==========================================================
# METHOD 1: Classic GoF (Double Dispatch)
# ==========================================================

print("=" * 60)
print("VISITOR PATTERN - Classic GoF")
print("=" * 60)

# ─── Elements ──────────────────────────────────────────

class Shape(Protocol):
    def accept(self, visitor: 'Visitor') -> str: ...

class Dot:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        
    def accept(self, visitor: 'Visitor') -> str:
        # Double Dispatch Step 2: The Element calls the specific 
        # visitor method associated with its class.
        return visitor.visit_dot(self)

class Circle:
    def __init__(self, radius: int) -> None:
        self.radius = radius
        
    def accept(self, visitor: 'Visitor') -> str:
        return visitor.visit_circle(self)


# ─── Visitor Interface & Implementations ───────────────

class Visitor(Protocol):
    def visit_dot(self, dot: Dot) -> str: ...
    def visit_circle(self, circle: Circle) -> str: ...

class XMLExporterVisitor:
    """Extracts state from shapes and returns XML."""
    
    def visit_dot(self, dot: Dot) -> str:
        return f"<dot><x>{dot.x}</x><y>{dot.y}</y></dot>"
        
    def visit_circle(self, circle: Circle) -> str:
        return f"<circle><radius>{circle.radius}</radius></circle>"


# ─── Classic Demo ───────────────

shapes: list[Shape] = [Dot(10, 20), Circle(15)]
xml_visitor = XMLExporterVisitor()

for shape in shapes:
    # Double Dispatch Step 1: The Client calls accept() on the Element
    result = shape.accept(xml_visitor)
    print(f"  Exported: {result}")


# ==========================================================
# METHOD 2: Modern Python (SingleDispatch)
# ==========================================================

print("\n" + "=" * 60)
print("VISITOR PATTERN - Modern Python (@singledispatch)")
print("=" * 60)

# ─── Elements (Notice there is NO accept() method!) ────

class PythonicDot:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

class PythonicCircle:
    def __init__(self, radius: int) -> None:
        self.radius = radius


# ─── Visitor using SingleDispatch ──────────────────────
# @singledispatch gives us method overloading by type!

@singledispatch
def export_json(shape) -> str:
    raise NotImplementedError("Unsupported shape type")

@export_json.register(PythonicDot)
def _(dot: PythonicDot) -> str:
    return f'{{"type": "dot", "x": {dot.x}, "y": {dot.y}}}'

@export_json.register(PythonicCircle)
def _(circle: PythonicCircle) -> str:
    return f'{{"type": "circle", "radius": {circle.radius}}}'


# ─── Modern Demo ───────────────

modern_shapes = [PythonicDot(30, 40), PythonicCircle(50)]

for shape in modern_shapes:
    # Look how clean this is! No accept() boilerplate.
    # Python automatically routes it to the correct registered function.
    result = export_json(shape)
    print(f"  Exported: {result}")

print("\n✅ Visitor pattern demonstrated successfully!")
