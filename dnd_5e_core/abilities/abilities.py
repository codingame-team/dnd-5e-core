"""
D&D 5e Core - Abilities System
The six core abilities: Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AbilityType(Enum):
    """The six core abilities in D&D 5e"""
    STR = "str"
    DEX = "dex"
    CON = "con"
    INT = "int"
    WIS = "wis"
    CHA = "cha"


@dataclass
class Abilities:
    """
    Container for the six core ability scores.

    Standard array: 15, 14, 13, 12, 10, 8
    Point buy: 8-15 (before racial bonuses)

    Ability scores determine modifiers:
        1: -5, 2-3: -4, 4-5: -3, 6-7: -2, 8-9: -1
        10-11: +0, 12-13: +1, 14-15: +2, 16-17: +3, 18-19: +4, 20-21: +5
        etc.
    """
    str: int  # Strength - Athletics, melee attacks
    dex: int  # Dexterity - Acrobatics, ranged attacks, AC
    con: int  # Constitution - HP, concentration saves
    int: int  # Intelligence - Arcana, Investigation
    wis: int  # Wisdom - Perception, Insight, Survival
    cha: int  # Charisma - Persuasion, Deception, Performance

    def get_value_by_name(self, name: str) -> int:
        """
        Get ability value by full name.

        Args:
            name: "Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", or "Charism"

        Returns:
            int: The ability score
        """
        attr_map = {
            "Strength": "str",
            "Dexterity": "dex",
            "Constitution": "con",
            "Intelligence": "int",
            "Wisdom": "wis",
            "Charism": "cha"
        }
        return getattr(self, attr_map.get(name, name.lower()))

    def set_value_by_name(self, name: str, value: int):
        """Set ability value by full name"""
        attr_map = {
            "Strength": "str",
            "Dexterity": "dex",
            "Constitution": "con",
            "Intelligence": "int",
            "Wisdom": "wis",
            "Charism": "cha"
        }
        setattr(self, attr_map.get(name, name.lower()), value)

    def get_value_by_index(self, name: str) -> int:
        """
        Get ability value by index (short name).

        Args:
            name: "str", "dex", "con", "int", "wis", or "cha"

        Returns:
            int: The ability score
        """
        return getattr(self, name)

    def set_value_by_index(self, name: str, value: int):
        """Set ability value by index (short name)"""
        setattr(self, name, value)

    def get_modifier(self, ability: str) -> int:
        """
        Calculate ability modifier from ability score.

        Formula: (score - 10) // 2

        Args:
            ability: "str", "dex", "con", "int", "wis", or "cha"

        Returns:
            int: The ability modifier (-5 to +10 typically)
        """
        score = self.get_value_by_index(ability)
        return (score - 10) // 2

    def __repr__(self):
        return (
            f"STR: {self.str} DEX: {self.dex} CON: {self.con} "
            f"INT: {self.int} WIS: {self.wis} CHA: {self.cha}"
        )

