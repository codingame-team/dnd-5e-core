"""
D&D 5e Core - Dice Mechanics
Handles dice rolling and damage calculations
"""
from __future__ import annotations

from dataclasses import dataclass
from random import randint
from typing import Optional


@dataclass
class DamageDice:
    """
    Represents a dice roll formula (e.g., "2d6+3", "1d8", "3d10-2")
    Used for damage, healing, and other random calculations in D&D 5e.

    Examples:
        - "1d6" → 1 six-sided die
        - "2d8+5" → 2 eight-sided dice plus 5
        - "3d10-2" → 3 ten-sided dice minus 2
    """
    dice: str
    bonus: int = 0

    def __repr__(self):
        if self.bonus > 0:
            return f"{self.dice}+{self.bonus}"
        elif self.bonus < 0:
            return f"{self.dice}{self.bonus}"
        return f"{self.dice}"

    @property
    def max_score(self) -> int:
        """Maximum possible roll value"""
        if "d" not in self.dice:
            return int(self.dice) + self.bonus

        # Extract the base dice notation (remove any +/- in the dice string)
        dice_part = self.dice
        dice_bonus = 0

        if "+" in self.dice:
            dice_part, bonus_str = self.dice.split("+")
            dice_bonus = int(bonus_str)
        elif "-" in self.dice:
            dice_part, bonus_str = self.dice.split("-")
            dice_bonus = -int(bonus_str)

        dice_count, dice_sides = map(int, dice_part.split("d"))
        return self.bonus + dice_bonus + (dice_count * dice_sides)

    def __eq__(self, other):
        return self.max_score == other.max_score

    def __lt__(self, other):
        return self.max_score < other.max_score

    def __gt__(self, other):
        return self.max_score > other.max_score

    def roll(self) -> int:
        """
        Roll the dice and return the result.

        Returns:
            int: The rolled value (minimum 0)
        """
        # Handle simple number (no dice)
        if "d" not in self.dice:
            return max(0, int(self.dice) + self.bonus)

        # Handle bonus in dice string (e.g., "2d6+3")
        if "+" in self.dice:
            dice_part, bonus_part = self.dice.split("+")
            dice_count, dice_sides = map(int, dice_part.split("d"))
            total = sum([randint(1, dice_sides) for _ in range(dice_count)])
            total += int(bonus_part) + self.bonus
            return max(0, total)

        # Handle negative bonus in dice string (e.g., "2d6-2")
        elif "-" in self.dice:
            dice_part, bonus_part = self.dice.split("-")
            dice_count, dice_sides = map(int, dice_part.split("d"))
            total = sum([randint(1, dice_sides) for _ in range(dice_count)])
            total -= int(bonus_part)
            total += self.bonus
            return max(0, total)

        # Standard dice notation (e.g., "2d6")
        else:
            dice_count, dice_sides = map(int, self.dice.split("d"))
            total = sum([randint(1, dice_sides) for _ in range(dice_count)])
            total += self.bonus
            return max(0, total)

    @property
    def avg_bad(self) -> int:
        """Average expected roll value"""
        if "d" not in self.dice:
            return int(self.dice) + self.bonus

        # Extract the base dice notation (remove any +/- in the dice string)
        dice_part = self.dice
        dice_bonus = 0

        if "+" in self.dice:
            dice_part, bonus_str = self.dice.split("+")
            dice_bonus = int(bonus_str)
        elif "-" in self.dice:
            dice_part, bonus_str = self.dice.split("-")
            dice_bonus = -int(bonus_str)

        dice_count, dice_sides = map(int, dice_part.split("d"))
        return self.bonus + dice_bonus + (dice_count * (dice_sides + 1) // 2)

    @property
    def avg(self) -> int:
        dice_count, roll_dice = map(int, self.dice.split("d"))
        bonus = self.bonus if self.bonus else 0
        return bonus + dice_count * roll_dice // 2

    def score(self, success_type: str = "none") -> float:
        """
        Calculate expected score with success type modifier.

        Args:
            success_type: "none" (full damage) or "half" (half damage on save)

        Returns:
            float: Expected score value
        """
        if "d" not in self.dice:
            factor = 1.0 if success_type.lower() == "none" else 0.5
            return (int(self.dice) + self.bonus) * factor

        dice_count, dice_sides = map(int, self.dice.split("d"))
        factor = 1.0 if success_type.lower() == "none" else 0.5
        expected = (self.bonus + dice_sides * (1 + dice_count)) * factor / 2
        return expected

