"""
D&D 5e Core - Combat Module
Contains all combat-related classes and systems
"""

from .damage import Damage
from .condition import Condition
from .action import ActionType, Action
from .special_ability import AreaOfEffect, SpecialAbility
from .combat_system import CombatSystem, execute_combat_turn

__all__ = [
    'Damage',
    'Condition',
    'ActionType', 'Action',
    'AreaOfEffect', 'SpecialAbility',
    'CombatSystem', 'execute_combat_turn'
]

