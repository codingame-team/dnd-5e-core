"""
D&D 5e Core - Spellcaster System
Spellcasting abilities and spell slots
"""
from __future__ import annotations

from copy import copy
from dataclasses import dataclass
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .spell import Spell


@dataclass
class SpellCaster:
    """
    Spellcasting ability for characters and monsters.

    Manages:
    - Spell slots (1st through 9th level)
    - Known spells
    - Spellcasting ability and DC
    """
    level: int  # Caster level (not character level for multiclass)
    spell_slots: List[int]  # Available slots for each level [1st, 2nd, ..., 9th]
    learned_spells: List['Spell']  # Spells this caster knows
    dc_type: str  # Spellcasting ability (e.g., "int", "wis", "cha")
    dc_value: Optional[int]  # Spell save DC
    ability_modifier: Optional[int]  # Spellcasting ability modifier

    def __copy__(self):
        """Create a copy of this spellcaster"""
        return SpellCaster(
            self.level,
            self.spell_slots[:],  # Copy the list
            self.learned_spells,  # Spells are shared
            self.dc_type,
            self.dc_value,
            self.ability_modifier
        )

    def __repr__(self):
        return f"SpellCaster(Level {self.level}, DC {self.dc_value})"

    def can_cast(self, spell: 'Spell') -> bool:
        """
        Check if this caster can cast a spell.

        Args:
            spell: The spell to check

        Returns:
            bool: True if spell can be cast
        """
        # Check if spell is known
        if spell not in self.learned_spells:
            return False

        # Cantrips are always castable
        if spell.is_cantrip:
            return True

        # Check if spell slot is available
        if spell.level > len(self.spell_slots):
            return False

        return self.spell_slots[spell.level - 1] > 0

    def use_spell_slot(self, level: int) -> bool:
        """
        Use a spell slot of the given level.

        Args:
            level: Spell slot level (1-9)

        Returns:
            bool: True if slot was used, False if no slots available
        """
        if level < 1 or level > len(self.spell_slots):
            return False

        if self.spell_slots[level - 1] > 0:
            self.spell_slots[level - 1] -= 1
            return True

        return False

    def restore_spell_slot(self, level: int, count: int = 1):
        """
        Restore spell slots (e.g., after short/long rest).

        Args:
            level: Spell slot level (1-9)
            count: Number of slots to restore
        """
        if level < 1 or level > len(self.spell_slots):
            return

        self.spell_slots[level - 1] += count

    def restore_all_slots(self, max_slots: List[int]):
        """
        Restore all spell slots to maximum (long rest).

        Args:
            max_slots: Maximum slots for each level
        """
        self.spell_slots = max_slots[:]

    @property
    def total_slots_remaining(self) -> int:
        """Get total number of spell slots remaining"""
        return sum(self.spell_slots)

    @property
    def highest_slot_available(self) -> int:
        """
        Get the highest spell slot level available.

        Returns:
            int: Highest slot level (1-9), or 0 if no slots
        """
        for level in range(len(self.spell_slots) - 1, -1, -1):
            if self.spell_slots[level] > 0:
                return level + 1
        return 0

    def get_slots_for_level(self, level: int) -> int:
        """
        Get remaining slots for a specific level.

        Args:
            level: Spell level (1-9)

        Returns:
            int: Number of slots remaining
        """
        if level < 1 or level > len(self.spell_slots):
            return 0
        return self.spell_slots[level - 1]

    def knows_spell(self, spell: 'Spell') -> bool:
        """Check if this caster knows a specific spell"""
        return spell in self.learned_spells

    def learn_spell(self, spell: 'Spell'):
        """Add a spell to known spells"""
        if spell not in self.learned_spells:
            self.learned_spells.append(spell)

    def forget_spell(self, spell: 'Spell'):
        """Remove a spell from known spells"""
        if spell in self.learned_spells:
            self.learned_spells.remove(spell)

    @property
    def cantrips(self) -> List['Spell']:
        """Get all known cantrips"""
        return [s for s in self.learned_spells if s.is_cantrip]

    @property
    def leveled_spells(self) -> List['Spell']:
        """Get all known leveled spells (not cantrips)"""
        return [s for s in self.learned_spells if not s.is_cantrip]

