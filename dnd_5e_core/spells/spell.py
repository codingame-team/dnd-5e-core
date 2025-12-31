"""
D&D 5e Core - Spell System
Spells and spellcasting for D&D 5e
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from ..equipment.weapon import DamageType
    from ..mechanics.dice import DamageDice
    from ..combat.special_ability import AreaOfEffect


@dataclass
class Spell:
    """
    A spell in D&D 5e.

    Spells can:
    - Deal damage
    - Heal
    - Apply conditions
    - Buff/debuff

    Spell levels:
    - 0: Cantrips (unlimited use)
    - 1-9: Leveled spells (use spell slots)
    """
    index: str
    name: str
    desc: str
    level: int  # 0 = cantrip, 1-9 = spell level
    allowed_classes: List[str]  # Classes that can learn this spell
    heal_at_slot_level: Optional[Dict[str, str]]  # Healing by slot level
    damage_type: Optional['DamageType']  # Type of damage (for saving throws)
    damage_at_slot_level: Optional[Dict[str, str]]  # Damage by slot level
    damage_at_character_level: Optional[Dict[str, str]]  # Damage by caster level (cantrips)
    dc_type: Optional[str]  # Ability for saving throw (e.g., "dex", "con")
    dc_success: Optional[str]  # "half" or "none" - what happens on successful save
    range: int  # Range in feet
    area_of_effect: Optional['AreaOfEffect']
    school: str  # School of magic (evocation, abjuration, etc.)
    id: int = -1

    def __repr__(self):
        return f"{self.name} (Level {self.level}, {self.school})"

    def __eq__(self, other):
        """Two spells are equal if they have the same index"""
        return self.index == other.index

    @property
    def is_cantrip(self) -> bool:
        """Check if spell is a cantrip (level 0)"""
        return self.level == 0

    @property
    def is_healing(self) -> bool:
        """Check if spell has healing effects"""
        return self.heal_at_slot_level is not None

    @property
    def is_damaging(self) -> bool:
        """Check if spell deals damage"""
        return (self.damage_at_slot_level is not None or
                self.damage_at_character_level is not None)

    @property
    def has_area_effect(self) -> bool:
        """Check if spell has area of effect"""
        return self.area_of_effect is not None

    @property
    def requires_save(self) -> bool:
        """Check if spell requires a saving throw"""
        return self.dc_type is not None

    def get_heal_effect(self, slot_level: int, ability_modifier: int) -> 'DamageDice':
        """
        Get healing dice for a specific spell slot level.

        Args:
            slot_level: The level of spell slot used (1-9)
            ability_modifier: Caster's spellcasting ability modifier

        Returns:
            DamageDice: Healing dice formula
        """
        from ..mechanics.dice import DamageDice

        if not self.heal_at_slot_level:
            return DamageDice(dice="0", bonus=0)

        heal_dice_str = self.heal_at_slot_level.get(str(slot_level + 1), "0")

        # Simple number (no dice)
        if 'd' not in heal_dice_str:
            return DamageDice(dice="0", bonus=int(heal_dice_str))

        # Just dice, no bonus
        if '+' not in heal_dice_str:
            return DamageDice(dice=heal_dice_str, bonus=0)

        # Dice + bonus
        dice, bonus_str = heal_dice_str.split("+")
        bonus = ability_modifier if bonus_str.strip() == "MOD" else int(bonus_str.strip())
        return DamageDice(dice=dice, bonus=bonus)

    def get_spell_damages(self, caster_level: int, ability_modifier: int) -> List['DamageDice']:
        """
        Get damage dice for this spell.

        Args:
            caster_level: Character level (for cantrips) or spell level
            ability_modifier: Caster's spellcasting ability modifier

        Returns:
            List[DamageDice]: List of damage dice formulas
        """
        from ..mechanics.dice import DamageDice

        # Leveled spells use damage_at_slot_level
        if self.damage_at_slot_level:
            damage_dice_str = self.damage_at_slot_level.get(str(self.level), "0")
        # Cantrips use damage_at_character_level
        elif self.damage_at_character_level:
            # Find the highest level <= caster_level
            damage_dice_str = None
            for level in range(caster_level, -1, -1):
                if str(level) in self.damage_at_character_level:
                    damage_dice_str = self.damage_at_character_level.get(str(level))
                    break

            if not damage_dice_str:
                return [DamageDice(dice="0", bonus=0)]
        else:
            return [DamageDice(dice="0", bonus=0)]

        # Parse damage dice string
        if not damage_dice_str or damage_dice_str == "0":
            return [DamageDice(dice="0", bonus=0)]

        # Simple number (no dice)
        if "d" not in damage_dice_str:
            return [DamageDice(dice="0", bonus=int(damage_dice_str))]

        # Multiple damage dice (e.g., "2d6 + 1d8")
        if damage_dice_str.count("d") > 1:
            return [DamageDice(dice=dd.strip(), bonus=0)
                    for dd in damage_dice_str.split("+")]

        # Single damage dice
        if '+' not in damage_dice_str:
            return [DamageDice(dice=damage_dice_str, bonus=0)]

        # Dice + bonus
        dice, bonus_str = damage_dice_str.split("+")
        bonus = ability_modifier if "MOD" in bonus_str else int(bonus_str.strip())
        return [DamageDice(dice=dice.strip(), bonus=bonus)]

    def can_be_cast_by(self, class_name: str) -> bool:
        """
        Check if a class can cast this spell.

        Args:
            class_name: Name of the class (e.g., "wizard", "cleric")

        Returns:
            bool: True if class can cast this spell
        """
        return class_name.lower() in [c.lower() for c in self.allowed_classes]

