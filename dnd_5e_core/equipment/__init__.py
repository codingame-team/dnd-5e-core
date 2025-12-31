"""
D&D 5e Core - Equipment Module
Contains all equipment classes (weapons, armor, potions, etc.)
"""

from .equipment import Cost, EquipmentCategory, Equipment, Inventory
from .potion import PotionRarity, Potion, HealingPotion, SpeedPotion, StrengthPotion
from .weapon import (
    CategoryType, RangeType, DamageType,
    WeaponProperty, WeaponRange, WeaponThrowRange, Weapon
)
from .armor import Armor

__all__ = [
    # Base equipment
    'Cost', 'EquipmentCategory', 'Equipment', 'Inventory',
    # Potions
    'PotionRarity', 'Potion', 'HealingPotion', 'SpeedPotion', 'StrengthPotion',
    # Weapon types
    'CategoryType', 'RangeType', 'DamageType',
    'WeaponProperty', 'WeaponRange', 'WeaponThrowRange', 'Weapon',
    # Armor
    'Armor',
]

