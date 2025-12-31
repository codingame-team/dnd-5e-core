"""
D&D 5e Core - Weapon System
Weapon classes and related enums for D&D 5e combat
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, TYPE_CHECKING

from .equipment import Equipment

if TYPE_CHECKING:
    from ..mechanics.dice import DamageDice


class CategoryType(Enum):
    """Weapon category: Simple or Martial"""
    SIMPLE = "Simple"
    MARTIAL = "Martial"


class RangeType(Enum):
    """Weapon range: Melee or Ranged"""
    MELEE = "Melee"
    RANGED = "Ranged"


@dataclass
class DamageType:
    """Type of damage dealt by weapon (e.g., slashing, piercing, bludgeoning)"""
    index: str
    name: str
    desc: str

    def __repr__(self):
        return f"{self.index}"


@dataclass
class WeaponProperty:
    """Weapon property (e.g., finesse, versatile, two-handed)"""
    index: str
    name: str
    desc: str

    def __repr__(self):
        return f"{self.name}"


@dataclass
class WeaponRange:
    """Range for ranged weapons (normal/long)"""
    normal: int
    long: Optional[int]

    def __repr__(self):
        if self.long:
            return f"{self.normal}/{self.long}"
        return f"{self.normal}"


@dataclass
class WeaponThrowRange:
    """Throwing range for thrown weapons"""
    normal: int
    long: int

    def __repr__(self):
        return f"{self.normal}/{self.long}"


@dataclass
class WeaponData(Equipment):
    """
    Weapon data structure for D&D 5e weapons.

    This contains pure business logic for weapons.
    For pygame positioning, use GameEntity wrapper:

        from game_entity import create_game_weapon
        game_weapon = create_game_weapon(weapon, x=10, y=20, image_name="sword.png")
    """
    # Core D&D 5e attributes
    index: str
    name: str
    properties: List[WeaponProperty]
    damage_type: DamageType
    range_type: RangeType
    category_type: CategoryType
    damage_dice: 'DamageDice'  # Forward reference
    damage_dice_two_handed: Optional['DamageDice'] = None
    weapon_range: Optional[WeaponRange] = None
    throw_range: Optional[WeaponThrowRange] = None
    is_magic: bool = False

    # Computed fields
    range: Optional[WeaponRange] = field(default=None, init=False)
    category_range: str = field(init=False)

    def __post_init__(self):
        """Set the combined category and range string and handle aliases"""
        self.category_range = f"{self.category_type.value} {self.range_type.value}"
        # Handle range alias for backward compatibility
        if self.weapon_range is not None:
            self.range = self.weapon_range

    def __repr__(self):
        return self.name

    @property
    def is_melee(self) -> bool:
        """Check if weapon is melee"""
        return self.range_type == RangeType.MELEE

    @property
    def is_ranged(self) -> bool:
        """Check if weapon is ranged"""
        return self.range_type == RangeType.RANGED

    @property
    def is_simple(self) -> bool:
        """Check if weapon is simple"""
        return self.category_type == CategoryType.SIMPLE

    @property
    def is_martial(self) -> bool:
        """Check if weapon is martial"""
        return self.category_type == CategoryType.MARTIAL

    def has_property(self, property_index: str) -> bool:
        """Check if weapon has a specific property"""
        return any(p.index == property_index for p in self.properties)


# Alias for compatibility
Weapon = WeaponData

