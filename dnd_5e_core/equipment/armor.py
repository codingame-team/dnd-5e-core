"""
D&D 5e Core - Armor System
Armor classes for D&D 5e
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, TYPE_CHECKING, List

from .equipment import Equipment, Cost, EquipmentCategory


@dataclass
class ArmorData(Equipment):
    armor_class: dict
    str_minimum: int
    stealth_disadvantage: bool

    def __repr__(self):
        return self.name


# Alias for compatibility
Armor = ArmorData

