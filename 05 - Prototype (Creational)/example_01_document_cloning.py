"""
============================================================
Example: Document Cloning with Deep Copy
Pattern: Prototype (Creational)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
A document management system where users create documents from
templates. Instead of building each document from scratch (loading
fonts, styles, headers, footers), clone a template and customize.

KEY INSIGHT:
------------
Deep copy creates a fully independent clone. Modifying the clone
has ZERO effect on the original (or any other clones).

============================================================
"""

import copy
from dataclasses import dataclass, field


@dataclass
class Style:
    font: str = "Arial"
    size: int = 12
    color: str = "#000000"
    bold: bool = False


@dataclass
class Document:
    """A document that can be cloned from a template."""
    title: str
    content: str
    author: str
    styles: dict[str, Style] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)

    def clone(self) -> "Document":
        """Prototype method — deep copy to ensure full independence."""
        return copy.deepcopy(self)

    def __str__(self) -> str:
        styles_str = ", ".join(f"{k}:{v.font}/{v.size}" for k, v in self.styles.items())
        return (
            f"Document('{self.title}' by {self.author}, "
            f"tags={self.tags}, styles=[{styles_str}])"
        )


# ─── Template Registry ─────────────────────────────

class TemplateRegistry:
    """Registry of document templates (prototypes)."""

    _templates: dict[str, Document] = {}

    @classmethod
    def register(cls, name: str, template: Document) -> None:
        cls._templates[name] = template

    @classmethod
    def create_from(cls, name: str, **overrides: str) -> Document:
        """Clone a template and apply overrides."""
        if name not in cls._templates:
            raise ValueError(f"Template '{name}' not found")
        doc = cls._templates[name].clone()
        for key, value in overrides.items():
            setattr(doc, key, value)
        return doc


# ─── Demo ──────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("PROTOTYPE — Document Cloning")
    print("=" * 60)

    # Create a rich template (expensive to build from scratch)
    report_template = Document(
        title="Quarterly Report Template",
        content="[Report content placeholder]",
        author="Template",
        styles={
            "heading": Style(font="Helvetica", size=24, bold=True),
            "body": Style(font="Georgia", size=11, color="#333333"),
            "footer": Style(font="Arial", size=8, color="#999999"),
        },
        tags=["report", "quarterly"],
        metadata={"version": "1.0", "department": "Engineering"},
    )
    TemplateRegistry.register("report", report_template)

    # Clone and customize — much faster than rebuilding from scratch
    print("\n  --- Cloning from template ---")
    q1_report = TemplateRegistry.create_from(
        "report", title="Q1 2025 Report", author="Alice"
    )
    q1_report.tags.append("Q1")
    q1_report.metadata["quarter"] = "Q1"
    print(f"  Clone 1: {q1_report}")

    q2_report = TemplateRegistry.create_from(
        "report", title="Q2 2025 Report", author="Bob"
    )
    q2_report.tags.append("Q2")
    q2_report.styles["heading"].color = "#0066cc"
    print(f"  Clone 2: {q2_report}")

    # Verify deep independence
    print("\n  --- Independence check ---")
    print(f"  Template tags: {report_template.tags}")
    print(f"  Q1 tags:       {q1_report.tags}")
    print(f"  Q2 tags:       {q2_report.tags}")
    print(f"  Template heading color: {report_template.styles['heading'].color}")
    print(f"  Q2 heading color:       {q2_report.styles['heading'].color}")

    assert "Q1" not in report_template.tags, "Template should be unmodified!"
    assert "Q2" not in q1_report.tags, "Q1 should be independent of Q2!"
    assert report_template.styles["heading"].color == "#000000", "Template style unchanged!"
    assert q2_report.styles["heading"].color == "#0066cc", "Clone style changed!"

    print("\n✅ Document Cloning demonstrated successfully!")
