"""
D&D 5e Core - Race System
Main races for D&D 5e characters
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from ..classes.proficiency import Proficiency
    from .trait import Trait
    from .subrace import SubRace
    from .language import Language


@dataclass
class Race:
    """
    A race in D&D 5e (e.g., Human, Elf, Dwarf, Halfling).

    Races provide:
    - Ability score bonuses
    - Starting proficiencies
    - Languages
    - Racial traits
    - Optional subraces
    """
    index: str
    name: str
    speed: int  # Base walking speed (typically 25 or 30 feet)
    ability_bonuses: Dict[str, int]  # e.g., {"dex": 2, "int": 1}
    alignment: str  # Typical alignment for the race
    age: str  # Description of typical lifespan
    size: str  # "Small" or "Medium"
    size_description: str  # Detailed size description
    starting_proficiencies: List['Proficiency']
    starting_proficiency_options: List[Tuple[int, List['Proficiency']]]  # Choose X from list
    languages: List['Language']
    language_desc: str  # Description of language abilities
    traits: List['Trait']
    subraces: List['SubRace']

    def __repr__(self):
        return f"{self.name}"

    def get_ability_bonus(self, ability: str) -> int:
        """
        Get ability bonus for a specific ability.

        Args:
            ability: "str", "dex", "con", "int", "wis", or "cha"

        Returns:
            int: Bonus to the ability score (0 if no bonus)
        """
        return self.ability_bonuses.get(ability, 0)

    @property
    def has_subraces(self) -> bool:
        """Check if race has subraces"""
        return len(self.subraces) > 0

    @property
    def is_small(self) -> bool:
        """Check if race size is Small"""
        return self.size.lower() == "small"

    @property
    def is_medium(self) -> bool:
        """Check if race size is Medium"""
        return self.size.lower() == "medium"

