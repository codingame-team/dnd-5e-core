"""
D&D 5e Core - Damage System
Damage types and damage calculations for combat
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..equipment.weapon import DamageType
    from ..mechanics.dice import DamageDice


@dataclass
class Damage:
    """
    Represents damage dealt in combat.

    Combines a damage type (slashing, piercing, fire, etc.)
    with a damage dice (e.g., 2d6+3).
    """
    type: 'DamageType'
    dd: 'DamageDice'  # Damage dice

    def __repr__(self):
        return f"{self.dd} {self.type.index}"

    def roll(self) -> int:
        """Roll damage dice to get actual damage dealt"""
        return self.dd.roll()

    @property
    def average(self) -> int:
        """Average damage expected"""
        return self.dd.avg

    @property
    def maximum(self) -> int:
        """Maximum possible damage"""
        return self.dd.max_score

