"""
============================================================
Example: Serializer Factory — Multi-Format Serialization
Pattern: Factory Method (Creational)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
An API needs to serialize response data in different formats
(JSON, XML, YAML-like) based on the Accept header. Each format
has its own serializer, but the API handler shouldn't know about
the concrete serializer classes.

PATTERN PARTICIPANTS IN THIS EXAMPLE:
--------------------------------------
- Product → Serializer (ABC)
- ConcreteProducts → JSONSerializer, XMLSerializer, PlainTextSerializer
- Creator → SerializerFactory (classmethod-based)

KEY INSIGHT:
------------
The factory method here is a @classmethod alternative constructor
pattern — very Pythonic. `Serializer.for_content_type("application/json")`
reads like natural English.

============================================================
"""

from abc import ABC, abstractmethod
from typing import Any


# ─── Product (Abstract) ────────────────────────────

class Serializer(ABC):
    """Abstract serializer — all formats implement this."""

    @abstractmethod
    def serialize(self, data: dict[str, Any]) -> str:
        """Convert a dict to a formatted string."""
        ...

    @abstractmethod
    def content_type(self) -> str:
        """Return the MIME content type."""
        ...

    # ─── Factory Method (classmethod) ──────────────
    @classmethod
    def for_content_type(cls, content_type: str) -> "Serializer":
        """
        Factory method: create the right serializer for a content type.

        This is the Pythonic 'alternative constructor' pattern.
        """
        registry: dict[str, type[Serializer]] = {
            "application/json": JSONSerializer,
            "text/xml": XMLSerializer,
            "application/xml": XMLSerializer,
            "text/plain": PlainTextSerializer,
        }
        normalized = content_type.lower().strip()
        if normalized not in registry:
            raise ValueError(
                f"Unsupported content type: '{content_type}'. "
                f"Supported: {list(registry.keys())}"
            )
        return registry[normalized]()


# ─── Concrete Products ─────────────────────────────

class JSONSerializer(Serializer):
    """Serializes data as JSON."""

    def serialize(self, data: dict[str, Any]) -> str:
        import json
        return json.dumps(data, indent=2)

    def content_type(self) -> str:
        return "application/json"


class XMLSerializer(Serializer):
    """Serializes data as simple XML."""

    def serialize(self, data: dict[str, Any]) -> str:
        lines = ["<response>"]
        for key, value in data.items():
            lines.append(f"  <{key}>{value}</{key}>")
        lines.append("</response>")
        return "\n".join(lines)

    def content_type(self) -> str:
        return "text/xml"


class PlainTextSerializer(Serializer):
    """Serializes data as key=value plain text."""

    def serialize(self, data: dict[str, Any]) -> str:
        return "\n".join(f"{k}: {v}" for k, v in data.items())

    def content_type(self) -> str:
        return "text/plain"


# ─── Simulated API Handler ─────────────────────────

def handle_request(data: dict[str, Any], accept_header: str) -> str:
    """
    Simulated API endpoint.

    The handler doesn't know about JSONSerializer, XMLSerializer, etc.
    It only talks to the Serializer interface through the factory method.
    """
    serializer = Serializer.for_content_type(accept_header)
    body = serializer.serialize(data)
    return f"Content-Type: {serializer.content_type()}\n\n{body}"


# ─── Usage / Demo ──────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("FACTORY METHOD — Serializer Factory")
    print("=" * 60)

    sample_data = {
        "id": 42,
        "name": "Alice",
        "email": "alice@example.com",
        "active": True,
    }

    # Simulate different clients requesting different formats
    accept_headers = [
        "application/json",
        "text/xml",
        "text/plain",
    ]

    for accept in accept_headers:
        print(f"\n  --- Request: Accept: {accept} ---")
        response = handle_request(sample_data, accept)
        print(f"{response}")

    # Error handling
    print("\n  --- Request: Accept: text/html ---")
    try:
        handle_request(sample_data, "text/html")
    except ValueError as e:
        print(f"  ⚠️  {e}")

    # Verify polymorphism: handler never imports concrete classes
    s1 = Serializer.for_content_type("application/json")
    s2 = Serializer.for_content_type("text/xml")
    assert isinstance(s1, JSONSerializer)
    assert isinstance(s2, XMLSerializer)
    assert s1.content_type() != s2.content_type()

    print("\n✅ Serializer Factory demonstrated successfully!")
