"""
D&D 5e Core - Special Ability System
Special abilities for monsters and characters
"""
from __future__ import annotations

from dataclasses import dataclass, field
from random import randint
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .damage import Damage
    from .condition import Condition
    from ..equipment.weapon import RangeType


@dataclass
class AreaOfEffect:
    """
    Area of effect for spells and abilities.

    Types: sphere, cube, cone, line, cylinder
    """
    type: str  # "sphere", "cube", "cone", "line", "cylinder"
    size: int  # Radius or side length in feet

    def __repr__(self):
        return f"{self.size}-foot {self.type}"


@dataclass
class SpecialAbility:
    """
    A special ability for monsters (e.g., Dragon Breath, Death Burst).

    Special abilities often have:
    - Damage
    - Saving throws
    - Conditions
    - Recharge mechanics
    - Area of effect
    """
    name: str
    desc: str
    damages: List['Damage']
    dc_type: str  # Ability for saving throw (e.g., "dex", "con")
    dc_value: int  # Difficulty class for saving throw
    dc_success: str  # "half" or "none" - what happens on successful save
    recharge_on_roll: Optional[int] = None  # Recharge on d6 roll of X or higher
    range: Optional['RangeType'] = None
    area_of_effect: Optional[AreaOfEffect] = None
    ready: bool = True  # Whether ability is currently available
    effects: Optional[List['Condition']] = None
    targets_count: int = 6  # Maximum number of targets

    def __repr__(self):
        return f"{self.name} (DC {self.dc_value} {self.dc_type})"

    @property
    def recharge_success(self) -> bool:
        """
        Check if ability recharges.

        Returns:
            bool: True if recharge successful (or no recharge needed)
        """
        if self.recharge_on_roll is None:
            return True  # No recharge needed
        return randint(1, 6) >= self.recharge_on_roll

    def use(self):
        """Use this ability (sets ready to False if it needs recharging)"""
        if self.recharge_on_roll is not None:
            self.ready = False

    def try_recharge(self) -> bool:
        """
        Try to recharge this ability.

        Returns:
            bool: True if recharged successfully
        """
        if self.recharge_on_roll is None:
            return True  # Always ready

        if self.recharge_success:
            self.ready = True
            return True
        return False

    def can_use_after_death(self, creature_index: str) -> bool:
        """
        Check if ability can be used after creature's death.

        Some abilities trigger on death (e.g., Death Burst).

        Args:
            creature_index: Index of the creature

        Returns:
            bool: True if can be used after death
        """
        # Special case for Magma Mephit Death Burst
        if creature_index == "magma-mephit" and self.name == "Death Burst":
            return True

        # Add other death-triggered abilities here
        return "death" in self.name.lower() or "burst" in self.name.lower()

    @property
    def total_damage_average(self) -> int:
        """Calculate average total damage"""
        if not self.damages:
            return 0
        return sum(d.average for d in self.damages)

    @property
    def has_area_effect(self) -> bool:
        """Check if ability has area of effect"""
        return self.area_of_effect is not None

