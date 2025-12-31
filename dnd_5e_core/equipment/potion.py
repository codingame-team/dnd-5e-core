"""
D&D 5e Core - Potion System
Potion classes for healing, buffs, and other consumables
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from copy import copy
from dataclasses import dataclass
from enum import Enum
from random import randint
from typing import Optional

from .equipment import Cost


# Note: Import sera ajusté après migration complète
# from ..entities.sprite import Sprite


class PotionRarity(Enum):
    """Rarity levels for potions (affects cost and power)"""
    COMMON = 60
    UNCOMMON = 80
    RARE = 95
    VERY_RARE = 99
    LEGENDARY = 100


class Potion(ABC):
    """
    Base class for all potions.

    This contains pure business logic for potions.
    For pygame positioning, use GameEntity wrapper:

        from game_entity import create_game_potion
        game_potion = create_game_potion(potion, x=10, y=20, image_name="potion.png")
    """

    def __init__(
        self,
        name: str,
        rarity: PotionRarity,
        min_cost: int,
        max_cost: int,
        min_level: int = 1
    ):
        self.name = name
        self.rarity = rarity
        self.min_cost = min_cost
        self.max_cost = max_cost
        self.min_level = min_level
        self.cost = Cost(randint(self.min_cost, self.max_cost), "gp")

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        result.rarity = copy(self.rarity)
        result.cost = copy(self.cost)
        return result

    @abstractmethod
    def effect(self) -> str:
        """Return description of potion effect"""
        pass

    def __repr__(self):
        return f"{self.name} ({self.rarity.name})"


class HealingPotion(Potion):
    """
    Potion that restores hit points.

    Uses dice notation for healing amount (e.g., "2d4+2")
    """

    def __init__(
        self,
        name: str,
        rarity: PotionRarity,
        hit_dice: str,
        bonus: int,
        min_cost: int,
        max_cost: int,
        min_level: int = 1
    ):
        super().__init__(name, rarity, min_cost, max_cost, min_level)
        self.hit_dice = hit_dice
        self.bonus = bonus

    def effect(self) -> str:
        return f"Restores {self.min_hp_restored} to {self.max_hp_restored} HP"

    @property
    def min_hp_restored(self) -> int:
        """Minimum HP restored"""
        dice_count, dice_sides = map(int, self.hit_dice.split("d"))
        return self.bonus + dice_count

    @property
    def max_hp_restored(self) -> int:
        """Maximum HP restored"""
        dice_count, dice_sides = map(int, self.hit_dice.split("d"))
        return self.bonus + (dice_count * dice_sides)

    @property
    def score(self) -> float:
        """Average healing value"""
        return (self.min_hp_restored + self.max_hp_restored) / 2


class SpeedPotion(Potion):
    """
    Potion that increases movement speed.

    In D&D 5e, this typically doubles speed and grants other benefits.
    """

    def __init__(
        self,
        name: str,
        rarity: PotionRarity,
        min_cost: int,
        max_cost: int,
        duration: int,  # Duration in seconds
        min_level: int = 1
    ):
        super().__init__(name, rarity, min_cost, max_cost, min_level)
        self.duration = duration

    def effect(self) -> str:
        return f"Increases speed for {self.duration} seconds"


class StrengthPotion(Potion):
    """
    Potion that sets Strength to a specific value.

    In D&D 5e, Potions of Giant Strength set STR to specific values
    (e.g., Hill Giant = 21, Fire Giant = 25)
    """

    def __init__(
        self,
        name: str,
        rarity: PotionRarity,
        min_cost: int,
        max_cost: int,
        value: int,  # Strength value (e.g., 21 for Hill Giant Strength)
        duration: int,  # Duration in seconds
        min_level: int = 1
    ):
        super().__init__(name, rarity, min_cost, max_cost, min_level)
        self.value = value
        self.duration = duration

    def effect(self) -> str:
        minutes = self.duration // 60
        return f"Increases strength to {self.value} for {minutes} minutes"

