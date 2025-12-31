"""
D&D 5e Core - Condition System
Status conditions that can affect characters and monsters
"""
from __future__ import annotations

from copy import copy
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..abilities.abilities import AbilityType


@dataclass
class Condition:
    """
    A condition affecting a creature in D&D 5e.

    Common conditions:
    - Blinded, Charmed, Deafened, Frightened
    - Grappled, Incapacitated, Invisible, Paralyzed
    - Petrified, Poisoned, Prone, Restrained
    - Stunned, Unconscious, Exhausted
    """
    index: str  # Condition identifier (e.g., "poisoned", "stunned")
    name: str = ""
    desc: str = ""
    dc_type: Optional['AbilityType'] = None  # Ability for saving throw
    dc_value: Optional[int] = None  # DC for saving throw
    creature: Optional[object] = None  # Source creature (forward ref to avoid circular import)

    def __copy__(self):
        """Create a copy of this condition"""
        return Condition(
            self.index,
            self.name,
            self.desc,
            self.dc_type,
            self.dc_value,
            self.creature
        )

    def __repr__(self):
        if self.dc_type and self.dc_value:
            return f"{self.name} (DC {self.dc_value} {self.dc_type})"
        return f"{self.name}"

    @property
    def is_blinded(self) -> bool:
        return self.index == "blinded"

    @property
    def is_charmed(self) -> bool:
        return self.index == "charmed"

    @property
    def is_frightened(self) -> bool:
        return self.index == "frightened"

    @property
    def is_grappled(self) -> bool:
        return self.index == "grappled"

    @property
    def is_paralyzed(self) -> bool:
        return self.index == "paralyzed"

    @property
    def is_poisoned(self) -> bool:
        return self.index == "poisoned"

    @property
    def is_prone(self) -> bool:
        return self.index == "prone"

    @property
    def is_restrained(self) -> bool:
        return self.index == "restrained"

    @property
    def is_stunned(self) -> bool:
        return self.index == "stunned"

    @property
    def is_unconscious(self) -> bool:
        return self.index == "unconscious"

