"""
D&D 5e Core - SubRace System
Subraces for D&D 5e races
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from ..classes.proficiency import Proficiency
    from .trait import Trait


@dataclass
class SubRace:
    """
    A subrace in D&D 5e (e.g., High Elf, Mountain Dwarf, Lightfoot Halfling).

    Subraces provide additional bonuses and traits beyond the base race.
    """
    index: str
    name: str
    desc: str
    ability_bonuses: Dict[str, int]  # e.g., {"int": 1}
    starting_proficiencies: List['Proficiency']
    racial_traits: List['Trait']

    def __repr__(self):
        return f"{self.name}"

    def get_ability_bonus(self, ability: str) -> int:
        """Get ability bonus for a specific ability"""
        return self.ability_bonuses.get(ability, 0)

