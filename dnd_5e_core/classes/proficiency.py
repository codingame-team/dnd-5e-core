"""
D&D 5e Core - Proficiency System
Proficiencies for skills, weapons, armor, tools, etc.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Any


class ProfType(Enum):
    """Types of proficiencies in D&D 5e"""
    SKILL = "Skills"
    ARMOR = "Armor"
    VEHICLE = "Vehicles"
    OTHER = "Other"
    TOOLS = "Artisan's Tools"
    ST = "Saving Throws"  # Saving Throws
    WEAPON = "Weapons"
    MUSIC = "Musical Instruments"
    GAMING = "Gaming Sets"


@dataclass
class Proficiency:
    """
    A proficiency in D&D 5e.

    Proficiencies represent training in:
    - Skills (Athletics, Acrobatics, etc.)
    - Weapons (Simple, Martial, specific weapons)
    - Armor (Light, Medium, Heavy, Shields)
    - Tools (Thieves' tools, Smith's tools, etc.)
    - Saving Throws (STR, DEX, etc.)
    """
    index: str
    name: str
    type: ProfType
    ref: Any  # Reference to Equipment, AbilityType, or other objects
    classes: Optional[List[str]] = None  # Which classes get this proficiency
    races: Optional[List[str]] = None  # Which races get this proficiency
    value: Optional[int] = None  # Bonus value for the proficiency

    def __repr__(self):
        return f"{self.name} ({self.type.value})"

    @property
    def is_skill(self) -> bool:
        """Check if proficiency is a skill"""
        return self.type == ProfType.SKILL

    @property
    def is_weapon(self) -> bool:
        """Check if proficiency is a weapon"""
        return self.type == ProfType.WEAPON

    @property
    def is_armor(self) -> bool:
        """Check if proficiency is armor"""
        return self.type == ProfType.ARMOR

    @property
    def is_tool(self) -> bool:
        """Check if proficiency is a tool"""
        return self.type in (ProfType.TOOLS, ProfType.MUSIC, ProfType.GAMING, ProfType.VEHICLE)

    @property
    def is_saving_throw(self) -> bool:
        """Check if proficiency is a saving throw"""
        return self.type == ProfType.ST

