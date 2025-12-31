"""
D&D 5e Core - Language System
Languages for D&D 5e races and characters
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Language:
    """
    A language in D&D 5e (e.g., Common, Elvish, Draconic).

    Languages can be:
    - Standard (Common, Dwarvish, Elvish, etc.)
    - Exotic (Abyssal, Celestial, Deep Speech, etc.)
    """
    index: str
    name: str
    desc: str
    type: str  # "Standard" or "Exotic"
    typical_speakers: List[str]
    script: str  # Writing system (e.g., "Common", "Elvish", "Dwarvish")

    def __repr__(self):
        return f"{self.name} ({self.type})"

    @property
    def is_standard(self) -> bool:
        """Check if language is standard"""
        return self.type.lower() == "standard"

    @property
    def is_exotic(self) -> bool:
        """Check if language is exotic"""
        return self.type.lower() == "exotic"

