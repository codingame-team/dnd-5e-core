"""
D&D 5e Core - Action System
Actions that creatures can take in combat
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .damage import Damage
    from .condition import Condition
    from .special_ability import SpecialAbility


class ActionType(Enum):
    """Types of actions in combat"""
    MELEE = "melee"
    RANGED = "ranged"
    MIXED = "melee+ranged"
    SPECIAL = "special"


@dataclass
class Action:
    """
    An action a creature can take in combat.

    Actions include:
    - Melee attacks (sword, claw, bite)
    - Ranged attacks (bow, crossbow, thrown weapon)
    - Special actions (breath weapons, spells)
    - Multi-attacks (multiple attacks in one turn)
    """
    name: str
    desc: str
    type: ActionType
    damages: Optional[List['Damage']] = None
    effects: Optional[List['Condition']] = None
    multi_attack: Optional[List[Union['Action', 'SpecialAbility']]] = None
    attack_bonus: int = 0
    normal_range: int = 5  # Reach for melee, normal range for ranged
    long_range: Optional[float] = None  # Long range for ranged attacks
    disadvantage: bool = False

    def __repr__(self):
        return f"{self.name} ({self.type.value})"

    @property
    def is_melee(self) -> bool:
        """Check if action is melee"""
        return self.type == ActionType.MELEE

    @property
    def is_ranged(self) -> bool:
        """Check if action is ranged"""
        return self.type == ActionType.RANGED

    @property
    def is_special(self) -> bool:
        """Check if action is special"""
        return self.type == ActionType.SPECIAL

    @property
    def has_multi_attack(self) -> bool:
        """Check if action includes multi-attack"""
        return self.multi_attack is not None and len(self.multi_attack) > 0

    @property
    def total_damage_average(self) -> int:
        """Calculate average total damage from all damage sources"""
        if not self.damages:
            return 0
        return sum(d.average for d in self.damages)

    @property
    def applies_conditions(self) -> bool:
        """Check if action applies any conditions"""
        return self.effects is not None and len(self.effects) > 0

