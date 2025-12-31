"""
D&D 5e Core - Character Class System
Character classes (Fighter, Wizard, Rogue, etc.) for D&D 5e
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .proficiency import Proficiency
    from ..abilities.abilities import AbilityType
    from ..equipment.equipment import Inventory


@dataclass
class ClassType:
    """
    A character class in D&D 5e (e.g., Fighter, Wizard, Rogue).

    Classes define:
    - Hit die (d6, d8, d10, d12)
    - Proficiencies (weapons, armor, skills, saving throws)
    - Starting equipment
    - Spellcasting ability (if any)
    - Spell slots progression
    """
    index: str
    name: str
    hit_die: int  # Hit die size (6, 8, 10, or 12)
    proficiency_choices: List[Tuple[int, List['Proficiency']]]  # Choose X from list
    proficiencies: List['Proficiency']  # Automatic proficiencies
    saving_throws: List['AbilityType']  # Proficient saving throws
    starting_equipment: List['Inventory']
    starting_equipment_options: List[List['Inventory']]  # Choose one option from each list
    class_levels: List[str]  # URLs to class levels (not yet implemented)
    multi_classing: List[str]  # Multiclassing info (not yet implemented)
    subclasses: List[str]  # Available subclasses (not yet implemented)
    spellcasting_level: int  # Level at which spellcasting starts (0 if non-caster)
    spellcasting_ability: str  # "int", "wis", "cha", or "" if non-caster
    can_cast: bool  # Whether class can cast spells
    spell_slots: Dict  # Spell slots by level
    spells_known: List[int]  # Number of spells known at each level
    cantrips_known: List[int]  # Number of cantrips known at each level

    def __repr__(self):
        return f"{self.name}"

    @property
    def is_spellcaster(self) -> bool:
        """Check if class can cast spells"""
        return self.can_cast

    @property
    def is_full_caster(self) -> bool:
        """Check if class is a full caster (spells at level 1)"""
        return self.spellcasting_level == 1

    @property
    def is_half_caster(self) -> bool:
        """Check if class is a half caster (spells at level 2)"""
        return self.spellcasting_level == 2

    @property
    def is_third_caster(self) -> bool:
        """Check if class is a third caster (spells at level 3)"""
        return self.spellcasting_level == 3

    def get_proficiency_bonus(self, level: int) -> int:
        """
        Calculate proficiency bonus for a given level.

        Args:
            level: Character level (1-20)

        Returns:
            int: Proficiency bonus (+2 to +6)
        """
        if level < 1:
            return 2
        if level <= 4:
            return 2
        if level <= 8:
            return 3
        if level <= 12:
            return 4
        if level <= 16:
            return 5
        return 6


@dataclass
class Feature:
    """A class feature gained at a specific level"""
    index: str
    name: str
    class_type: ClassType
    class_level: int
    prerequisites: List[str]
    desc: List[str]

    def __repr__(self):
        return f"{self.name} (Level {self.class_level})"


@dataclass
class Level:
    """Information about a specific class level"""
    index: str
    class_type: ClassType
    ability_score_bonuses: int  # Number of ASI at this level
    prof_bonus: int
    features: List[Feature]
    class_specific: Dict  # Class-specific info (rage damage, sneak attack, etc.)
    spell_casting: Optional[Dict]  # Spellcasting info for this level

    def __repr__(self):
        return f"{self.class_type.name} Level {self.index}"


@dataclass
class BackGround:
    """Character background (Acolyte, Criminal, Noble, etc.)"""
    index: str
    name: str
    starting_proficiencies: List['Proficiency']
    languages: List  # List of languages
    starting_equipment: List  # List of equipment
    starting_equipment_options: List  # Equipment choices

    def __repr__(self):
        return f"{self.name}"

