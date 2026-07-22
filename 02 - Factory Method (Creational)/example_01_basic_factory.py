"""
============================================================
Example: Basic Factory with Registry Pattern
Pattern: Factory Method (Creational)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
A document processing system that needs to parse files in multiple
formats (JSON, XML, CSV, YAML). The format is determined at runtime
from the file extension. Adding new formats should require zero
changes to existing code.

PATTERN PARTICIPANTS IN THIS EXAMPLE:
--------------------------------------
- Product → Parser (Protocol)
- ConcreteProducts → JSONParser, XMLParser, CSVParser
- Factory → ParserFactory (registry-based)

KEY INSIGHT:
------------
The registry pattern (dict mapping) is the most Pythonic factory.
New parsers self-register via decorator — zero changes to the factory.

============================================================
"""

from typing import Protocol, Any
import json
import csv
import io


# ─── Product Interface ─────────────────────────────

class Parser(Protocol):
    """All parsers must implement this interface."""

    def parse(self, raw_data: str) -> Any: ...
    def file_extensions(self) -> list[str]: ...


# ─── Concrete Products ─────────────────────────────

class JSONParser:
    """Parses JSON strings into Python dicts/lists."""

    def parse(self, raw_data: str) -> Any:
        return json.loads(raw_data)

    def file_extensions(self) -> list[str]:
        return [".json"]


class CSVParser:
    """Parses CSV strings into list of dicts."""

    def parse(self, raw_data: str) -> list[dict]:
        reader = csv.DictReader(io.StringIO(raw_data))
        return list(reader)

    def file_extensions(self) -> list[str]:
        return [".csv"]


class XMLParser:
    """Simple XML tag extractor (lightweight, no external deps)."""

    def parse(self, raw_data: str) -> dict[str, str]:
        # Minimal XML parsing using string operations
        # In production you'd use xml.etree.ElementTree
        import re
        tags = re.findall(r"<(\w+)>(.*?)</\1>", raw_data)
        return dict(tags)

    def file_extensions(self) -> list[str]:
        return [".xml"]


# ─── Factory (Registry-Based) ──────────────────────

class ParserFactory:
    """
    Registry-based factory.

    Parsers register themselves by format name. The factory creates
    the right parser based on the requested format. Adding new
    formats requires ZERO changes to this class (OCP).
    """

    _registry: dict[str, type] = {}

    @classmethod
    def register(cls, fmt: str, parser_class: type) -> None:
        """Register a parser class for a format name."""
        cls._registry[fmt.lower()] = parser_class

    @classmethod
    def create(cls, fmt: str) -> Parser:
        """Create a parser instance for the given format."""
        fmt_lower = fmt.lower().lstrip(".")
        if fmt_lower not in cls._registry:
            available = ", ".join(sorted(cls._registry.keys()))
            raise ValueError(
                f"Unknown format: '{fmt}'. Available: {available}"
            )
        return cls._registry[fmt_lower]()

    @classmethod
    def available_formats(cls) -> list[str]:
        """List all registered formats."""
        return sorted(cls._registry.keys())


# Register built-in parsers
ParserFactory.register("json", JSONParser)
ParserFactory.register("csv", CSVParser)
ParserFactory.register("xml", XMLParser)


# ─── Adding a NEW format (zero changes to factory!) ─

class INIParser:
    """Parses simple INI-style key=value strings."""

    def parse(self, raw_data: str) -> dict[str, str]:
        result = {}
        for line in raw_data.strip().splitlines():
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                result[key.strip()] = value.strip()
        return result

    def file_extensions(self) -> list[str]:
        return [".ini", ".cfg"]


# Just register — factory code untouched!
ParserFactory.register("ini", INIParser)


# ─── Usage / Demo ──────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("FACTORY METHOD — Registry-Based Parser Factory")
    print("=" * 60)

    # Test data for each format
    test_data = {
        "json": '{"name": "Alice", "age": 30, "city": "NYC"}',
        "csv": "name,age,city\nAlice,30,NYC\nBob,25,LA",
        "xml": "<name>Alice</name><age>30</age><city>NYC</city>",
        "ini": "name = Alice\nage = 30\ncity = NYC",
    }

    print(f"\n  Available formats: {ParserFactory.available_formats()}")

    for fmt, data in test_data.items():
        parser = ParserFactory.create(fmt)
        result = parser.parse(data)
        print(f"\n  [{fmt.upper()}] {parser.__class__.__name__}")
        print(f"    Input:  {data[:50]}...")
        print(f"    Output: {result}")

    # Error handling for unknown format
    print()
    try:
        ParserFactory.create("yaml")
    except ValueError as e:
        print(f"  ⚠️  Expected error: {e}")

    # Verify OCP: we added INI without touching ParserFactory
    assert "ini" in ParserFactory.available_formats()
    ini_parser = ParserFactory.create("ini")
    result = ini_parser.parse("host = localhost\nport = 5432")
    assert result == {"host": "localhost", "port": "5432"}

    print("\n✅ Factory Method demonstrated successfully!")
