"""
D&D 5e Core - Equipment System
Base classes for all equipment (weapons, armor, potions, etc.)
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Union



@dataclass
class Cost:
    """
    Represents the cost of an item in D&D 5e currency.

    Supported units:
        - cp: Copper pieces (1 cp = 1 cp)
        - sp: Silver pieces (1 sp = 10 cp)
        - ep: Electrum pieces (1 ep = 50 cp)
        - gp: Gold pieces (1 gp = 100 cp)
        - pp: Platinum pieces (1 pp = 1000 cp)
    """
    quantity: int
    unit: str

    @property
    def value(self) -> int:
        """Value in copper pieces"""
        rates = {"cp": 1, "sp": 10, "ep": 50, "gp": 100, "pp": 1000}
        return self.quantity * rates.get(self.unit, 1)

    def __repr__(self):
        return f"{self.quantity} {self.unit}"


@dataclass
class EquipmentCategory:
    """
    Category of equipment (e.g., "weapon", "armor", "potion", "adventuring-gear")
    """
    index: str
    name: str
    url: str

    def __repr__(self):
        return f"{self.index}"


@dataclass
class Equipment:
    """
    Base class for all equipment in D&D 5e.

    All equipment has:
        - A position (inherited from Sprite) for dungeon/inventory placement
        - A cost
        - A weight
        - A category
        - An equipped status
    """
    index: str
    name: str
    cost: Cost
    weight: int
    desc: Optional[List[str]]
    category: EquipmentCategory
    equipped: bool

    @property
    def price(self) -> int:
        """Buy price in copper pieces"""
        return self.cost.value

    @property
    def sell_price(self) -> int:
        """Sell price (typically half of buy price) in copper pieces"""
        return self.cost.value // 2

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"#{self.id} {self.index} ({self.category})"


@dataclass
class Inventory:
    """
    Inventory entry (quantity + equipment/category)
    """
    quantity: str
    equipment: Union[Equipment, EquipmentCategory]

    def __repr__(self):
        return f"{self.quantity} {self.equipment.index}"

