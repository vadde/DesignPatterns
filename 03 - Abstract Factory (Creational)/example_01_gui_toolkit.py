"""
============================================================
Example: Cross-Platform GUI Toolkit Factory
Pattern: Abstract Factory (Creational)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
A cross-platform desktop app needs to render native-looking UI
widgets (buttons, checkboxes, text inputs) for Windows, macOS,
and Linux. Each platform has its own look and feel, but all widgets
must come from the SAME platform — no mixing Mac buttons with
Windows checkboxes.

KEY INSIGHT:
------------
Abstract Factory guarantees family consistency. Swap the factory,
and ALL products change together. The client code never knows
which platform it's running on.

============================================================
"""

from abc import ABC, abstractmethod
from typing import Protocol
import sys


# ─── Abstract Products ─────────────────────────────

class Button(Protocol):
    def render(self) -> str: ...
    def on_click(self, handler: str) -> str: ...

class Checkbox(Protocol):
    def render(self) -> str: ...
    def toggle(self) -> str: ...

class TextInput(Protocol):
    def render(self) -> str: ...
    def set_value(self, text: str) -> str: ...


# ─── Abstract Factory ──────────────────────────────

class GUIFactory(ABC):
    """Abstract factory — declares creation methods for each widget type."""

    @abstractmethod
    def create_button(self, label: str) -> Button: ...

    @abstractmethod
    def create_checkbox(self, label: str) -> Checkbox: ...

    @abstractmethod
    def create_text_input(self, placeholder: str) -> TextInput: ...


# ─── macOS Family ───────────────────────────────────

class MacButton:
    def __init__(self, label: str) -> None:
        self.label = label

    def render(self) -> str:
        return f"  🍎 [  {self.label}  ] (rounded macOS button)"

    def on_click(self, handler: str) -> str:
        return f"  🍎 Button '{self.label}' → {handler}"


class MacCheckbox:
    def __init__(self, label: str) -> None:
        self.label = label
        self.checked = False

    def render(self) -> str:
        icon = "☑" if self.checked else "☐"
        return f"  🍎 {icon} {self.label} (macOS checkbox)"

    def toggle(self) -> str:
        self.checked = not self.checked
        return self.render()


class MacTextInput:
    def __init__(self, placeholder: str) -> None:
        self.placeholder = placeholder
        self.value = ""

    def render(self) -> str:
        display = self.value or self.placeholder
        return f"  🍎 ╭─────────────────╮\n     │ {display:<15} │ (macOS input)\n     ╰─────────────────╯"

    def set_value(self, text: str) -> str:
        self.value = text
        return self.render()


class MacFactory(GUIFactory):
    def create_button(self, label: str) -> Button:
        return MacButton(label)

    def create_checkbox(self, label: str) -> Checkbox:
        return MacCheckbox(label)

    def create_text_input(self, placeholder: str) -> TextInput:
        return MacTextInput(placeholder)


# ─── Windows Family ────────────────────────────────

class WinButton:
    def __init__(self, label: str) -> None:
        self.label = label

    def render(self) -> str:
        return f"  🪟 [ {self.label} ] (flat Windows button)"

    def on_click(self, handler: str) -> str:
        return f"  🪟 Button '{self.label}' → {handler}"


class WinCheckbox:
    def __init__(self, label: str) -> None:
        self.label = label
        self.checked = False

    def render(self) -> str:
        icon = "[x]" if self.checked else "[ ]"
        return f"  🪟 {icon} {self.label} (Windows checkbox)"

    def toggle(self) -> str:
        self.checked = not self.checked
        return self.render()


class WinTextInput:
    def __init__(self, placeholder: str) -> None:
        self.placeholder = placeholder
        self.value = ""

    def render(self) -> str:
        display = self.value or self.placeholder
        return f"  🪟 |{display:<17}| (Windows input)"

    def set_value(self, text: str) -> str:
        self.value = text
        return self.render()


class WindowsFactory(GUIFactory):
    def create_button(self, label: str) -> Button:
        return WinButton(label)

    def create_checkbox(self, label: str) -> Checkbox:
        return WinCheckbox(label)

    def create_text_input(self, placeholder: str) -> TextInput:
        return WinTextInput(placeholder)


# ─── Factory Selector ──────────────────────────────

def get_factory(platform: str = "") -> GUIFactory:
    """Select the right factory based on platform."""
    if not platform:
        platform = sys.platform
    factories: dict[str, type[GUIFactory]] = {
        "darwin": MacFactory,
        "mac": MacFactory,
        "win32": WindowsFactory,
        "windows": WindowsFactory,
    }
    factory_class = factories.get(platform, MacFactory)
    return factory_class()


# ─── Application (Client) ──────────────────────────

def render_login_form(factory: GUIFactory) -> None:
    """
    The application code doesn't know which platform's widgets
    it's using. It only talks to the abstract factory + products.
    """
    print("  ── Login Form ──")
    username = factory.create_text_input("Enter username")
    password = factory.create_text_input("Enter password")
    remember = factory.create_checkbox("Remember me")
    submit = factory.create_button("Sign In")

    print(username.render())
    print(password.render())
    print(remember.render())
    print(submit.render())


# ─── Demo ──────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("ABSTRACT FACTORY — Cross-Platform GUI Toolkit")
    print("=" * 60)

    for platform in ["mac", "windows"]:
        print(f"\n  ═══ Platform: {platform.upper()} ═══")
        factory = get_factory(platform)
        render_login_form(factory)

    # Key point: the SAME render_login_form() code works with
    # BOTH factories — zero platform-specific code in the client
    print()
    assert isinstance(get_factory("mac"), MacFactory)
    assert isinstance(get_factory("windows"), WindowsFactory)

    print("✅ Abstract Factory demonstrated successfully!")
