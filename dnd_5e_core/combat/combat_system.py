"""
D&D 5e Core - Combat System
Centralized combat logic used by all game versions
"""

from typing import List, Optional, Tuple, Callable, TYPE_CHECKING
from random import choice, sample, randint
import re

if TYPE_CHECKING:
    from ..entities import Character, Monster
    from ..spells import Spell
    from ..equipment import Weapon, Armor, HealingPotion
    from .special_ability import SpecialAbility
    from .action import Action, ActionType

from ..equipment import RangeType


class CombatSystem:
    """Centralized combat system for D&D 5e"""

    def __init__(self, verbose: bool = True, message_callback: Optional[Callable[[str], None]] = None):
        """
        Initialize combat system

        Args:
            verbose: If True, print messages directly. If False, use callback
            message_callback: Optional callback function for messages (for ncurses, pygame, etc.)
        """
        self.verbose = verbose
        self.message_callback = message_callback
        self.ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    def log_message(self, message: str, clean_ansi: bool = False):
        """
        Log a message either by printing or calling callback
        Handles multi-line messages by splitting them

        Args:
            message: Message to log (can contain newlines)
            clean_ansi: If True, remove ANSI color codes
        """
        if not message:
            return

        # Clean ANSI codes if requested
        if clean_ansi:
            message = self.ansi_escape.sub('', message).strip()

        # Split multi-line messages and send each line separately
        lines = message.strip().split('\n')

        for line in lines:
            line = line.strip()
            if not line:  # Skip empty lines
                continue

            if self.message_callback:
                self.message_callback(line)
            elif self.verbose:
                print(line)

    def monster_turn(self,
                     monster: 'Monster',
                     alive_monsters: List['Monster'],
                     alive_chars: List['Character'],
                     party: List['Character'],
                     round_num: int) -> None:
        """
        Execute a monster's turn in combat

        Args:
            monster: The attacking monster
            alive_monsters: List of alive monsters
            alive_chars: List of alive characters
            party: Full party list
            round_num: Current round number
        """
        # 1. Check if monster can heal allies
        healing_spells = []
        if hasattr(monster, 'is_spell_caster') and monster.is_spell_caster:
            if hasattr(monster, 'sc') and hasattr(monster.sc, 'learned_spells'):
                healing_spells = [s for s in monster.sc.learned_spells
                                  if hasattr(s, 'heal_at_slot_level') and s.heal_at_slot_level
                                  and monster.sc.spell_slots[s.level - 1] > 0]

        # Priority 1: Heal if allies are injured
        if any(m for m in alive_monsters if m.hit_points < 0.5 * m.max_hit_points) and healing_spells:
            max_spell_level = max([s.level for s in healing_spells])
            spell = choice([s for s in healing_spells if s.level == max_spell_level])
            target_monster = min(alive_monsters, key=lambda m: m.hit_points)

            try:
                if spell.range == 5:
                    heal_msg = monster.cast_heal(spell, spell.level - 1, [target_monster])
                else:
                    heal_msg = monster.cast_heal(spell, spell.level - 1, alive_monsters)

                if heal_msg:
                    self.log_message(heal_msg, clean_ansi=True)

                if not spell.is_cantrip:
                    monster.sc.spell_slots[spell.level - 1] -= 1
            except Exception:
                pass
            return

        # Select targets
        melee_chars = [c for i, c in enumerate(alive_chars) if i < 3]
        ranged_chars = [c for i, c in enumerate(alive_chars) if i >= 3]

        if not melee_chars and not ranged_chars:
            return

        # 2. Prepare spells
        castable_spells = []
        if hasattr(monster, 'is_spell_caster') and monster.is_spell_caster:
            if hasattr(monster, 'sc') and hasattr(monster.sc, 'learned_spells'):
                cantrip_spells = [s for s in monster.sc.learned_spells
                                  if not s.level and hasattr(s, 'damage_type') and s.damage_type]
                slot_spells = [s for s in monster.sc.learned_spells
                               if s.level and monster.sc.spell_slots[s.level - 1] > 0
                               and hasattr(s, 'damage_type') and s.damage_type]
                castable_spells = cantrip_spells + slot_spells

        # 3. Check special attacks
        available_special_attacks = []
        if hasattr(monster, 'sa') and monster.sa:
            if round_num > 0:
                for special_attack in monster.sa:
                    if hasattr(special_attack, 'recharge_on_roll') and special_attack.recharge_on_roll:
                        special_attack.ready = special_attack.recharge_success
            available_special_attacks = [a for a in monster.sa if hasattr(a, 'ready') and a.ready]

        # Priority 2: Cast attack spell
        if castable_spells:
            target_char = choice(ranged_chars) if ranged_chars else choice(melee_chars)
            attack_spell = max(castable_spells, key=lambda s: s.level)

            try:
                attack_msg, damage = monster.cast_attack(target_char, attack_spell, verbose=False)

                if attack_msg:
                    self.log_message(attack_msg, clean_ansi=True)

                if damage > 0:
                    target_char.hit_points -= damage

                if target_char.hit_points <= 0:
                    if target_char in alive_chars:
                        alive_chars.remove(target_char)
                    target_char.status = "DEAD"
                    self.log_message(f"{target_char.name} is KILLED!")

                if not attack_spell.is_cantrip:
                    monster.sc.spell_slots[attack_spell.level - 1] -= 1
            except Exception:
                # Fallback to simple attack
                self._simple_monster_attack(monster, melee_chars, ranged_chars, alive_chars)

        # Priority 3: Use special attack
        elif available_special_attacks:
            self._monster_special_attack(monster, available_special_attacks,
                                        melee_chars, ranged_chars, alive_chars, party)

        # Priority 4: Normal melee attack
        else:
            self._monster_normal_attack(monster, melee_chars, ranged_chars, alive_chars)

    def _monster_special_attack(self, monster, available_special_attacks,
                               melee_chars, ranged_chars, alive_chars, party):
        """Execute monster special attack"""
        special_attack = max(available_special_attacks,
                             key=lambda a: sum([d.dd.score(success_type=a.dc_success)
                                               for d in a.damages]) if hasattr(a, 'damages') else 0)

        # Determine targets
        targets_count = getattr(special_attack, 'targets_count', 1)
        if targets_count >= len(party):
            self.log_message(f"{monster.name} uses {special_attack.name.upper()} on whole party!")
            target_chars = party
        else:
            attack_range = getattr(special_attack, 'range', None)
            if attack_range == RangeType.MELEE and melee_chars:
                target_chars = sample(melee_chars, min(targets_count, len(melee_chars)))
            elif attack_range == RangeType.RANGED and ranged_chars:
                target_chars = sample(ranged_chars, min(targets_count, len(ranged_chars)))
            else:
                available = melee_chars + ranged_chars
                target_chars = sample(available, min(targets_count, len(available)))

            targets = ", ".join([char.name for char in target_chars])
            self.log_message(f"{monster.name} uses {special_attack.name.upper()} on {targets}!")

        # Execute on each target
        for target_char in target_chars:
            if target_char in alive_chars:
                try:
                    attack_msg, damage = monster.special_attack(target_char, special_attack, verbose=False)

                    if attack_msg:
                        self.log_message(attack_msg, clean_ansi=True)

                    if damage > 0:
                        target_char.hit_points -= damage

                    if target_char.hit_points <= 0:
                        if target_char in alive_chars:
                            alive_chars.remove(target_char)
                        target_char.status = "DEAD"
                        self.log_message(f"{target_char.name} is KILLED!")
                except Exception:
                    # Fallback
                    damage = randint(1, 8)
                    target_char.hit_points -= damage
                    self.log_message(f"{monster.name} hits {target_char.name} for {damage} damage!")

    def _monster_normal_attack(self, monster, melee_chars, ranged_chars, alive_chars):
        """Execute normal monster attack"""
        target_char = choice(melee_chars) if melee_chars else choice(alive_chars)

        from .action import ActionType
        melee_attacks = []
        if hasattr(monster, 'actions') and monster.actions:
            melee_attacks = [a for a in monster.actions
                             if hasattr(a, 'type') and a.type in (ActionType.MELEE, ActionType.MIXED)]

        if melee_attacks:
            try:
                attack_msg, damage = monster.attack(target=target_char, actions=melee_attacks, verbose=False)

                if attack_msg:
                    self.log_message(attack_msg, clean_ansi=True)

                if damage > 0:
                    target_char.hit_points -= damage

                if target_char.hit_points <= 0:
                    if target_char in alive_chars:
                        alive_chars.remove(target_char)
                    target_char.status = "DEAD"
                    self.log_message(f"{target_char.name} is KILLED!")
            except Exception:
                self._simple_monster_attack(monster, melee_chars, ranged_chars, alive_chars)
        else:
            self._simple_monster_attack(monster, melee_chars, ranged_chars, alive_chars)

    def _simple_monster_attack(self, monster, melee_chars, ranged_chars, alive_chars):
        """Simple fallback attack"""
        target = choice(melee_chars) if melee_chars else choice(alive_chars)
        damage = randint(1, 8)
        target.hit_points -= damage
        self.log_message(f"{monster.name} attacks {target.name} for {damage} damage!")

        if target.hit_points <= 0:
            if target in alive_chars:
                alive_chars.remove(target)
            target.status = "DEAD"
            self.log_message(f"{target.name} is KILLED!")

    def character_turn(self,
                      character: 'Character',
                      alive_chars: List['Character'],
                      alive_monsters: List['Monster'],
                      party: List['Character'],
                      weapons: Optional[List] = None,
                      armors: Optional[List] = None,
                      equipments: Optional[List] = None,
                      potions: Optional[List] = None) -> None:
        """
        Execute a character's turn in combat

        Args:
            character: The attacking character
            alive_chars: List of alive characters
            alive_monsters: List of alive monsters
            party: Full party list
            weapons: Available weapons for treasure
            armors: Available armors for treasure
            equipments: Available equipment for treasure
            potions: Available potions for treasure
        """
        if not alive_monsters:
            return

        # 1. Check if can heal party members
        healing_spells = []
        if hasattr(character, 'is_spell_caster') and character.is_spell_caster:
            if hasattr(character, 'sc') and hasattr(character.sc, 'learned_spells'):
                healing_spells = [s for s in character.sc.learned_spells
                                  if hasattr(s, 'heal_at_slot_level') and s.heal_at_slot_level
                                  and character.sc.spell_slots[s.level - 1] > 0]

        # Priority 1: Heal if needed
        if healing_spells and any(c for c in alive_chars if c.hit_points < 0.5 * c.max_hit_points):
            max_spell_level = max([s.level for s in healing_spells])
            spell = choice([s for s in healing_spells if s.level == max_spell_level])
            target_char = min(alive_chars, key=lambda c: c.hit_points)

            try:
                best_slot_level = character.get_best_slot_level(heal_spell=spell, target=target_char) if hasattr(character, 'get_best_slot_level') else spell.level - 1

                if spell.range == 5:
                    heal_msg = character.cast_heal(spell, best_slot_level, [target_char])
                else:
                    heal_msg = character.cast_heal(spell, best_slot_level, party)

                if heal_msg:
                    self.log_message(heal_msg, clean_ansi=True)

                if not spell.is_cantrip:
                    if hasattr(character, 'update_spell_slots'):
                        character.update_spell_slots(spell, best_slot_level)
            except Exception:
                pass
            return

        # Priority 2: Drink potion if low HP
        if hasattr(character, 'healing_potions') and character.hit_points < 0.3 * character.max_hit_points and character.healing_potions:
            try:
                potion = character.choose_best_potion() if hasattr(character, 'choose_best_potion') else character.healing_potions[0]

                drink_msg, success, hp_restored = character.drink(potion, verbose=False)

                if drink_msg:
                    self.log_message(drink_msg, clean_ansi=True)

                # Remove from inventory
                if hasattr(character, 'inventory'):
                    p_idx = next((i for i, item in enumerate(character.inventory)
                                 if item is not None and item == potion), None)
                    if p_idx is not None:
                        character.inventory[p_idx] = None

                remaining = len(character.healing_potions) if hasattr(character, 'healing_potions') else 0
                self.log_message(f"{character.name} has {remaining} remaining potions")
            except Exception:
                pass
            return

        # Priority 3: Handle restrained condition
        monster = self._select_target_monster(character, alive_chars, alive_monsters)

        # Priority 4: Attack
        in_melee = character in alive_chars[:3] if alive_chars else True

        try:
            self.log_message(f"{character.name} attacks {monster.name.title()}!")
            attack_msg, damage = character.attack(monster=monster, in_melee=in_melee, verbose=False)

            if attack_msg:
                self.log_message(attack_msg, clean_ansi=True)

            if damage > 0:
                monster.hit_points -= damage

            # Check for death
            if monster.hit_points <= 0:
                if monster in alive_monsters:
                    alive_monsters.remove(monster)
                self.log_message(f"{monster.name.title()} is KILLED!")

                # Victory rewards
                self._handle_victory(character, monster, weapons, armors, equipments, potions)
        except Exception:
            # Fallback
            damage = randint(1, 8) + character.level
            monster.hit_points -= damage
            self.log_message(f"{character.name} attacks {monster.name.title()} for {damage} damage!")

            if monster.hit_points <= 0:
                if monster in alive_monsters:
                    alive_monsters.remove(monster)
                self.log_message(f"{monster.name.title()} is KILLED!")

    def _select_target_monster(self, character, alive_chars, alive_monsters):
        """Select target monster, considering restrained condition"""
        restrained_effects = []
        if hasattr(character, 'conditions'):
            restrained_effects = [e for e in character.conditions
                                  if hasattr(e, 'index') and e.index == "restrained"
                                  and hasattr(e, 'creature') and e.creature]

        if restrained_effects:
            effect = restrained_effects[0]
            try:
                if hasattr(character, 'saving_throw') and character.saving_throw(effect.dc_type.value, effect.dc_value):
                    self.log_message(f"{character.name} is not restrained anymore from {effect.creature.name}!")
                    character.conditions.clear()
                    return min(alive_monsters, key=lambda m: m.hit_points)
                else:
                    return effect.creature
            except Exception:
                return min(alive_monsters, key=lambda m: m.hit_points)
        else:
            return min(alive_monsters, key=lambda m: m.hit_points)

    def _handle_victory(self, character, monster, weapons, armors, equipments, potions):
        """Handle victory rewards"""
        # XP and Gold
        if hasattr(character, 'victory'):
            try:
                victory_msg, xp, gold = character.victory(monster, verbose=False)
                if victory_msg:
                    self.log_message(victory_msg, clean_ansi=True)
            except Exception:
                pass

        # Treasure
        if hasattr(character, 'treasure') and weapons is not None:
            try:
                treasure_msg, item = character.treasure(weapons or [], armors or [],
                                                        equipments or [], potions or [], verbose=False)
                if treasure_msg:
                    self.log_message(treasure_msg, clean_ansi=True)
            except Exception:
                pass

        # Track kills
        if not hasattr(character, "kills"):
            character.kills = []
        character.kills.append(monster)


# Convenience function for simple combat execution
def execute_combat_turn(attacker,
                       alive_chars: List,
                       alive_monsters: List,
                       party: List,
                       round_num: int = 0,
                       verbose: bool = True,
                       message_callback: Optional[Callable] = None,
                       **kwargs) -> None:
    """
    Execute a single combat turn for an attacker

    Args:
        attacker: Character or Monster taking their turn
        alive_chars: List of alive characters
        alive_monsters: List of alive monsters
        party: Full party list
        round_num: Current round number
        verbose: Whether to print messages
        message_callback: Callback for messages (for UI)
        **kwargs: Additional arguments (weapons, armors, etc. for treasure)
    """
    combat = CombatSystem(verbose=verbose, message_callback=message_callback)

    from ..entities import Monster

    if isinstance(attacker, Monster):
        combat.monster_turn(attacker, alive_monsters, alive_chars, party, round_num)
    else:
        combat.character_turn(attacker, alive_chars, alive_monsters, party, **kwargs)

