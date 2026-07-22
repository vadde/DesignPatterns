"""
============================================================
Example: Device & Remote Control Bridge
Pattern: Bridge (Structural)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
You have devices (TV, Radio) and remote controls (Basic, Advanced).
Instead of creating `BasicTVRemote`, `AdvancedTVRemote`, `BasicRadioRemote`,
you separate them into two hierarchies connected by a bridge.

- Abstraction: Remote Control (High-level operations like toggle_power)
- Implementation: Device (Low-level operations like set_volume, enable)

KEY INSIGHT:
------------
You can add a new Device (e.g., SmartSpeaker) without touching ANY Remote code.
You can add a new Remote (e.g., VoiceRemote) without touching ANY Device code.
They vary completely independently.

============================================================
"""

from typing import Protocol

# ─── IMPLEMENTATION HIERARCHY (Low-Level) ───────────────

class Device(Protocol):
    """The Implementation interface."""
    def is_enabled(self) -> bool: ...
    def enable(self) -> None: ...
    def disable(self) -> None: ...
    def get_volume(self) -> int: ...
    def set_volume(self, percent: int) -> None: ...
    def get_channel(self) -> int: ...
    def set_channel(self, channel: int) -> None: ...


class TV:
    """Concrete Implementation 1"""
    def __init__(self) -> None:
        self._on = False
        self._volume = 30
        self._channel = 1
        
    def is_enabled(self) -> bool:
        return self._on
        
    def enable(self) -> None:
        self._on = True
        
    def disable(self) -> None:
        self._on = False
        
    def get_volume(self) -> int:
        return self._volume
        
    def set_volume(self, percent: int) -> None:
        self._volume = max(0, min(100, percent))
        
    def get_channel(self) -> int:
        return self._channel
        
    def set_channel(self, channel: int) -> None:
        self._channel = channel
        
    def __str__(self) -> str:
        state = "ON" if self._on else "OFF"
        return f"📺 TV is {state} (Vol: {self._volume}, Ch: {self._channel})"


class Radio:
    """Concrete Implementation 2"""
    def __init__(self) -> None:
        self._on = False
        self._volume = 50
        self._frequency = 88.1  # MHz instead of channels, but adapted to the interface
        
    def is_enabled(self) -> bool:
        return self._on
        
    def enable(self) -> None:
        self._on = True
        
    def disable(self) -> None:
        self._on = False
        
    def get_volume(self) -> int:
        return self._volume
        
    def set_volume(self, percent: int) -> None:
        self._volume = max(0, min(100, percent))
        
    def get_channel(self) -> int:
        return int(self._frequency * 10)
        
    def set_channel(self, channel: int) -> None:
        self._frequency = channel / 10.0
        
    def __str__(self) -> str:
        state = "ON" if self._on else "OFF"
        return f"📻 Radio is {state} (Vol: {self._volume}, Freq: {self._frequency}MHz)"


# ─── ABSTRACTION HIERARCHY (High-Level) ─────────────────

class RemoteControl:
    """
    The Base Abstraction.
    It holds a reference to the Implementation (Device) -- THIS IS THE BRIDGE!
    """
    def __init__(self, device: Device) -> None:
        self.device = device  # <--- The Bridge
        
    def toggle_power(self) -> None:
        if self.device.is_enabled():
            self.device.disable()
        else:
            self.device.enable()
            
    def volume_down(self) -> None:
        self.device.set_volume(self.device.get_volume() - 10)
        
    def volume_up(self) -> None:
        self.device.set_volume(self.device.get_volume() + 10)
        
    def channel_down(self) -> None:
        self.device.set_channel(self.device.get_channel() - 1)
        
    def channel_up(self) -> None:
        self.device.set_channel(self.device.get_channel() + 1)


class AdvancedRemoteControl(RemoteControl):
    """
    Refined Abstraction.
    Adds new features without touching the Device interface.
    """
    def mute(self) -> None:
        self.device.set_volume(0)


# ─── Demo ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("BRIDGE PATTERN")
    print("=" * 60)
    
    # 1. Use Basic Remote with TV
    tv = TV()
    remote = RemoteControl(tv)
    
    print("  [Using Basic Remote with TV]")
    remote.toggle_power()
    remote.volume_up()
    print(f"  {tv}")
    
    print("\n  [Switching to Advanced Remote for the SAME TV]")
    advanced_remote = AdvancedRemoteControl(tv)
    advanced_remote.mute()
    print(f"  {tv}")
    
    # 2. Use Advanced Remote with Radio
    print("\n  [Using Advanced Remote with Radio]")
    radio = Radio()
    radio_remote = AdvancedRemoteControl(radio)
    
    radio_remote.toggle_power()
    radio_remote.channel_up()
    radio_remote.channel_up()
    print(f"  {radio}")
    
    print("\n✅ Bridge pattern demonstrated successfully!")
