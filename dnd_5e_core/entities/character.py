"""
D&D 5e Core - Character Entity
Player character class for D&D 5e
"""
from __future__ import annotations

from dataclasses import dataclass, field
from math import floor
from random import randint, choice
from typing import List, Optional, TYPE_CHECKING

# Import classes needed at runtime (for isinstance checks)
from ..equipment.weapon import Weapon
from ..equipment.armor import Armor

if TYPE_CHECKING:
	from ..abilities.abilities import Abilities
	from ..races.race import Race
	from ..races.subrace import SubRace
	from ..classes.class_type import ClassType
	from ..classes.proficiency import Proficiency, ProfType
	from ..equipment.equipment import Equipment
	from ..equipment.potion import HealingPotion, SpeedPotion, StrengthPotion, Potion
	from ..spells.spellcaster import SpellCaster
	from ..spells.spell import Spell
	from ..combat.condition import Condition
	from ..mechanics.dice import DamageDice
	from .monster import Monster


@dataclass
class Character:
	"""
	A player character in D&D 5e.

	Characters have all the complexity of D&D 5e:
	- Race and class
	- Abilities and proficiencies
	- Equipment and inventory
	- Spellcasting (if applicable)
	- Conditions and effects
	- XP and leveling

	Note: This is game logic only. UI layer handles Sprite positioning.
	"""
	name: str
	race: 'Race'
	subrace: Optional['SubRace']
	ethnic: str
	gender: str
	height: str
	weight: str
	age: int
	class_type: 'ClassType'
	proficiencies: List['Proficiency']
	abilities: 'Abilities'
	ability_modifiers: 'Abilities'
	hit_points: int
	max_hit_points: int
	speed: int
	haste_timer: float
	hasted: bool
	xp: int
	level: int
	inventory: List[Optional['Equipment']]
	gold: int
	sc: Optional['SpellCaster'] = None
	conditions: Optional[List['Condition']] = None
	st_advantages: Optional[List[str]] = None
	ac_bonus: int = 0
	multi_attack_bonus: int = 0
	str_effect_modifier: int = -1
	str_effect_timer: float = 0.0
	status: str = "OK"
	id_party: int = -1
	OUT: bool = False
	kills: List['Monster'] = field(default_factory=list)

	def __eq__(self, other):
		if not isinstance(other, Character):
			return NotImplemented
		return self.name == other.name

	def __repr__(self):
		race_display = self.subrace.name if self.subrace else self.race.name
		weapon_name = self.weapon.name if self.weapon else "None"
		armor_name = self.armor.name if self.armor else "None"
		return f"{self.name} (Level {self.level} {race_display} {self.class_type.name}, AC {self.armor_class}, HP {self.hit_points}/{self.max_hit_points})"

	# ===== Properties =====

	@property
	def is_alive(self) -> bool:
		"""Check if character is alive"""
		return self.hit_points > 0

	@property
	def is_dead(self) -> bool:
		"""Check if character is dead"""
		return self.hit_points <= 0

	@property
	def weapon(self) -> Optional['Weapon']:
		"""Get equipped weapon"""
		equipped_weapons = [item for item in self.inventory if item and isinstance(item, Weapon) and item.equipped]
		return equipped_weapons[0] if equipped_weapons else None

	@property
	def armor(self) -> Optional['Armor']:
		"""Get equipped armor (not shield)"""
		from ..equipment.armor import Armor
		equipped_armors = [item for item in self.inventory if item and isinstance(item, Armor) and item.equipped and item.index != 'shield']
		return equipped_armors[0] if equipped_armors else None

	@property
	def shield(self) -> Optional['Armor']:
		"""Get equipped shield"""
		from ..equipment.armor import Armor
		equipped_shields = [item for item in self.inventory if item and isinstance(item, Armor) and item.equipped and item.index == 'shield']
		return equipped_shields[0] if equipped_shields else None

	@property
	def healing_potions(self) -> List['HealingPotion']:
		"""Get all healing potions in inventory"""
		from ..equipment.potion import HealingPotion
		return [item for item in self.inventory if item and isinstance(item, HealingPotion)]

	@property
	def speed_potions(self) -> List['SpeedPotion']:
		"""Get all speed potions in inventory"""
		from ..equipment.potion import SpeedPotion
		return [item for item in self.inventory if item and isinstance(item, SpeedPotion)]

	@property
	def is_spell_caster(self) -> bool:
		"""Check if character can cast spells"""
		return self.sc is not None

	@property
	def dc_value(self) -> int:
		"""Calculate spell save DC"""
		if not self.is_spell_caster:
			return 0

		spell_ability_mod = self.ability_modifiers.get_value_by_index(self.class_type.spellcasting_ability)
		prof_bonus = self.proficiency_bonus
		return 8 + spell_ability_mod + prof_bonus

	@property
	def proficiency_bonus(self) -> int:
		"""Calculate proficiency bonus based on level"""
		return self.class_type.get_proficiency_bonus(self.level)

	@property
	def in_dungeon(self) -> bool:
		"""Check if character is in a dungeon"""
		return self.id_party != -1

	def _get_ability(self, attr: str) -> int:
		"""Get total ability score (base + racial bonus)"""
		base = getattr(self.abilities, attr)
		racial_bonus = self.race.ability_bonuses.get(attr, 0)
		if self.subrace:
			racial_bonus += self.subrace.ability_bonuses.get(attr, 0)
		return base + racial_bonus

	@property
	def strength(self) -> int:
		"""Get effective strength (including potion effects)"""
		if self.str_effect_modifier != -1:
			return self.str_effect_modifier
		return self._get_ability("str")

	@property
	def dexterity(self) -> int:
		"""Get effective dexterity"""
		return self._get_ability("dex")

	@property
	def constitution(self) -> int:
		"""Get effective constitution"""
		return self._get_ability("con")

	@property
	def intelligence(self) -> int:
		"""Get effective intelligence"""
		return self._get_ability("int")

	@property
	def wisdom(self) -> int:
		"""Get effective wisdom"""
		return self._get_ability("wis")

	@property
	def charism(self) -> int:
		"""Get effective charisma"""
		return self._get_ability("cha")

	@property
	def multi_attacks(self) -> int:
		"""Calculate number of attacks per turn"""
		if self.class_type.index == "fighter":
			if self.level < 5:
				attack_counts = 1
			elif self.level < 11:
				attack_counts = 2
			else:
				attack_counts = 3
		elif self.class_type.index in ("paladin", "ranger", "monk", "barbarian"):
			attack_counts = 2 if self.level >= 5 else 1
		else:
			attack_counts = 1

		return attack_counts + self.multi_attack_bonus

	@property
	def armor_class(self):
		equipped_armors: List[Armor] = [item for item in self.inventory if isinstance(item, Armor) and item.equipped and item.name != "Shield"]
		equipped_shields: List[Armor] = [item for item in self.inventory if isinstance(item, Armor) and item.name == "Shield" and item.equipped]
		ac: int = (sum([item.armor_class["base"] for item in equipped_armors]) if equipped_armors else 10)
		ac += sum([item.armor_class["base"] for item in equipped_shields])
		return ac + self.ac_bonus if hasattr(self, "ac_bonus") else ac

	@property
	def damage_dice(self) -> 'DamageDice':
		"""Get damage dice from equipped weapon"""
		from ..mechanics.dice import DamageDice

		if not self.weapon:
			return DamageDice("1d2", 0)  # Unarmed

		# Use two-handed damage if available and no shield equipped
		if self.weapon.damage_dice_two_handed and not self.shield:
			return self.weapon.damage_dice_two_handed

		return self.weapon.damage_dice

	@property
	def prof_weapons(self) -> List['Weapon']:
		"""Get all proficient weapons"""
		from ..classes.proficiency import ProfType
		weapons = []
		for p in self.proficiencies:
			if p.type == ProfType.WEAPON:
				if isinstance(p.ref, list):
					weapons.extend(p.ref)
				else:
					weapons.append(p.ref)
		return [w for w in weapons if w is not None]

	@property
	def prof_armors(self) -> List['Armor']:
		"""Get all proficient armors"""
		from ..classes.proficiency import ProfType
		armors = []
		for p in self.proficiencies:
			if p.type == ProfType.ARMOR:
				if isinstance(p.ref, list):
					armors.extend(p.ref)
				else:
					armors.append(p.ref)
		return [a for a in armors if a is not None]

	# ===== Methods =====

	def can_cast(self, spell: Spell) -> bool:
		return self.is_spell_caster and spell in self.sc.learned_spells and (self.sc.spell_slots[spell.level - 1] > 0 or spell.is_cantrip)

	def drink(self, potion: 'Potion') -> bool:
		"""
		Drink a potion and apply its effects.

		Args:
			potion: The potion to drink

		Returns:
			bool: True if potion was successfully drunk
		"""
		from ..equipment.potion import HealingPotion, SpeedPotion, StrengthPotion
		import time
		from random import randint

		if not hasattr(potion, "min_level"):
			potion.min_level = 1

		if self.level < potion.min_level:
			return False

		if isinstance(potion, StrengthPotion):
			self.str_effect_modifier = potion.value
			self.str_effect_timer = time.time()
		elif isinstance(potion, SpeedPotion):
			self.hasted = True
			self.haste_timer = time.time()
			self.speed *= 2
			self.ac_bonus = 2
			self.multi_attack_bonus = 1
			if not hasattr(self, "st_advantages"):
				self.st_advantages = []
			self.st_advantages += ["dex"]
		else:  # HealingPotion
			hp_to_recover = self.max_hit_points - self.hit_points
			dice_count, roll_dice = map(int, potion.hit_dice.split("d"))
			hp_restored = potion.bonus + sum([randint(1, roll_dice) for _ in range(dice_count)])
			self.hit_points = min(self.hit_points + hp_restored, self.max_hit_points)

		return True

	def equip(self, item) -> bool:
		"""
		Equip or unequip an item (weapon or armor).

		Args:
			item: The item to equip/unequip

		Returns:
			bool: True if item was successfully equipped/unequipped
		"""
		from ..equipment.armor import Armor
		from ..equipment.weapon import Weapon

		if isinstance(item, Armor):
			if item.index == "shield":
				if self.shield:
					if item == self.shield:
						# un-equip shield
						item.equipped = not item.equipped
						return True
					else:
						# Cannot equip - already have shield equipped
						return False
				else:
					if self.weapon:
						is_two_handed = [p for p in self.weapon.properties if p.index == "two-handed"]
						if is_two_handed:
							# Cannot equip shield with 2-handed weapon
							return False
						else:
							# equip shield
							item.equipped = not item.equipped
							return True
					else:
						# equip shield
						item.equipped = not item.equipped
						return True
			else:
				if self.armor:
					if item == self.armor:
						# un-equip armor
						item.equipped = not item.equipped
						return True
					else:
						# Cannot equip - already have armor equipped
						return False
				else:
					if self.strength < item.str_minimum:
						# Cannot equip - not strong enough
						return False
					else:
						# equip armor
						item.equipped = not item.equipped
						return True
		elif isinstance(item, Weapon):
			if self.weapon:
				if item == self.weapon:
					# un-equip weapon
					item.equipped = not item.equipped
					return True
				else:
					# Cannot equip - already have weapon equipped
					return False
			else:
				is_two_handed = [p for p in item.properties if p.index == "two-handed"]
				if is_two_handed and self.shield:
					# Cannot equip 2-handed weapon with shield
					return False
				else:
					# equip weapon
					item.equipped = not item.equipped
					return True
		else:
			# Cannot equip this type of item
			return False

	def victory(self, monster: 'Monster', gold_reward: int = 0):
		"""
		Handle victory over a monster.

		Args:
			monster: The defeated monster
			gold_reward: Gold found (optional)
		"""
		self.xp += monster.xp
		self.kills.append(monster)
		if gold_reward > 0:
			self.gold += gold_reward

	def take_damage(self, damage: int):
		"""Take damage"""
		self.hit_points = max(0, self.hit_points - damage)

	def heal(self, amount: int):
		"""Heal hit points"""
		self.hit_points = min(self.max_hit_points, self.hit_points + amount)

	@property
	def is_full(self) -> bool:
		return all(item for item in self.inventory)

	def treasure(self, weapons, armors, equipments: List[Equipment], potions, solo_mode=False):
		if self.is_full:
			return
		free_slot = min([i for i, item in enumerate(self.inventory) if item is None])
		treasure_dice = randint(1, 3)
		if treasure_dice == 1:
			self.inventory[free_slot] = choice(potions)
		elif treasure_dice == 2:
			new_weapon: Weapon = choice(self.prof_weapons)
			self.inventory[free_slot] = new_weapon
		else:
			if self.prof_armors:
				new_armor: Armor = choice(self.prof_armors)
				if new_armor.armor_class["base"] > self.armor_class:
					for item in self.inventory:
						if isinstance(item, Armor) and item.equipped:
							item.equipped = False  # new_armor.equipped = True
				self.inventory[free_slot] = new_armor

	def get_best_slot_level(self, heal_spell: Spell, target: Character) -> int:
		max_slot_level = max(i for i, slot in enumerate(self.sc.spell_slots) if slot)
		best_slot_level = None
		max_score = 0
		for slot_level in range(heal_spell.level - 1, max_slot_level + 1):
			dd: DamageDice = heal_spell.get_heal_effect(slot_level, self.sc.ability_modifier)
			score = min(target.hit_points + dd.avg, target.max_hit_points) / dd.avg
			if score > max_score:
				max_score = score
				best_slot_level = slot_level
		return best_slot_level

	def cast_heal(self, spell: Spell, slot_level: int, targets: List[Character]):
		ability_modifier: int = int(self.ability_modifiers.get_value_by_index(name=self.class_type.spellcasting_ability))
		dd: DamageDice = spell.get_heal_effect(slot_level=slot_level, ability_modifier=ability_modifier)
		for char in targets:
			if char.hit_points < char.max_hit_points:
				hp_gained: int = min(dd.roll(), char.max_hit_points - char.hit_points)
				char.hit_points += hp_gained

	def cast_attack(self, spell: Spell, monster: Monster) -> int:
		ability_modifier: int = int(self.ability_modifiers.get_value_by_index(name=self.class_type.spellcasting_ability))
		damage_dices: List[DamageDice] = spell.get_spell_damages(caster_level=self.level, ability_modifier=ability_modifier)
		damage_roll: int = 0
		for dd in damage_dices:
			damage_roll += dd.roll()
		if spell.dc_type:
			st_success: bool = monster.saving_throw(dc_type=self.class_type.spellcasting_ability, dc_value=self.dc_value)
			if st_success:
				if spell.dc_success == "half":
					damage_roll //= 2
				elif spell.dc_success == "none":
					damage_roll = 0
		return damage_roll

	def update_spell_slots(self, spell: Spell, slot_level: Optional[int] = None):
		slot_level: int = slot_level + 1 if slot_level else spell.level
		if self.class_type.name == "Warlock":
			# all of your spell slots are the same level
			for level, slot in enumerate(self.sc.spell_slots):
				if slot:
					self.sc.spell_slots[level] -= 1
		else:
			self.sc.spell_slots[slot_level - 1] -= 1

	def attack(self, monster: Optional['Monster'] = None, character: Optional['Character'] = None, in_melee: bool = True, cast: bool = True, actions: Optional[List] = None) -> int:
		"""
		Attack a monster or character.

		Pure business logic - no UI output.
		The caller is responsible for displaying attack messages using dnd_5e_core.ui.

		Args:
			monster: Target monster
			character: Target character (for PvP)
			in_melee: Whether in melee range
			cast: Whether to use spells if available
			actions: Available actions (unused, for compatibility)

		Returns:
			int: Total damage dealt
		"""
		# Determine target (prioritize monster parameter for backward compatibility)
		target = monster if monster is not None else character
		if target is None:
			return 0

		def prof_bonus(x):
			return x // 5 + 2 if x < 5 else (x - 5) // 4 + 3

		damage_roll = 0
		castable_spells: List['Spell'] = []

		# Check for castable spells
		if self.is_spell_caster:
			cantric_spells: List['Spell'] = [s for s in self.sc.learned_spells if not s.level]
			slot_spells: List['Spell'] = [s for s in self.sc.learned_spells if s.level and self.sc.spell_slots[s.level - 1] > 0 and s.damage_type]
			castable_spells = cantric_spells + slot_spells

		# Use spell if available and not in melee
		if cast and castable_spells and not in_melee:
			attack_spell: 'Spell' = max(castable_spells, key=lambda s: s.level)
			damage_roll = self.cast_attack(attack_spell, target)
			if not attack_spell.is_cantrip:
				self.update_spell_slots(spell=attack_spell)
		else:
			# Melee/weapon attacks
			damage_multi = 0
			for _ in range(self.multi_attacks):
				if self.hit_points <= 0:
					break

				attack_roll = (randint(1, 20) + self.ability_modifiers.get_value_by_index("str") + prof_bonus(self.level))

				if attack_roll >= target.armor_class:
					damage_roll = self.damage_dice.roll()

				if damage_roll:
					# UI layer should display attack message:
					# attack_type = (self.weapon.damage_type.index.replace("ing", "es") if self.weapon else "punches")
					# cprint(f"{color.RED}{self.name}{color.END} {attack_type} {color.GREEN}{target.name}{color.END} for {damage_roll} hit points!")

					# Check if restrained (damage to self)
					if any([e for e in (self.conditions or []) if e.index == "restrained"]):
						damage_roll //= 2
						self.hit_points -= damage_roll
						# UI layer should display: f"{self.name} inflicts himself {damage_roll} hit points!"
						if self.hit_points <= 0:
							pass  # UI layer should display: f"{self.name} *** IS DEAD ***!"
					damage_multi += damage_roll
				else:
					pass  # UI layer should display: f"{self.name} misses {target.name}!"

			damage_roll = damage_multi

		return damage_roll

	def saving_throw(self, dc_type: str, dc_value: int) -> bool:
		"""
		Perform a saving throw against a spell or effect.

		Pure business logic - no UI output.

		Args:
			dc_type: Ability type for ST (e.g., 'dex', 'con', 'wis')
			dc_value: Difficulty class to beat

		Returns:
			bool: True if saving throw succeeds
		"""

		def ability_mod(x):
			return (x - 10) // 2

		def prof_bonus(x):
			return x // 5 + 2 if x < 5 else (x - 5) // 4 + 3

		st_type: str = f"saving-throw-{dc_type}"
		prof_modifiers: List[int] = [p.value for p in self.proficiencies if st_type == p.index]

		if prof_modifiers:
			ability_modifier: int = prof_modifiers[0]
		else:
			ability_modifier: int = (ability_mod(self.abilities.get_value_by_index(dc_type)) + prof_bonus(self.level))

		# Check for advantage on this saving throw
		has_advantage = (hasattr(self, "st_advantages") and self.st_advantages and dc_type in self.st_advantages)

		if has_advantage:
			# Roll with advantage (best of 2 rolls)
			return any(randint(1, 20) + ability_modifier > dc_value for _ in range(2))
		else:
			return randint(1, 20) + ability_modifier > dc_value

	def gain_level(self, tome_spells: List = None, verbose: bool = False) -> tuple:
		"""
		Gain a level with optional ability changes and spell learning.

		Args:
			tome_spells: List of Spell objects available to learn from (for spellcasters)
			verbose: If True, print messages to console. If False, only return messages.

		Returns:
			tuple: (messages: str, new_spells: List[Spell])
				- messages: Newline-separated string of level-up events
				- new_spells: List of newly learned spells (empty if not a spellcaster)
		"""
		from random import randint
		from copy import deepcopy

		display_msg: List[str] = []
		new_spells = []

		# Increase level
		self.level += 1

		# Calculate HP gain
		level_up_hit_die = {12: 7, 10: 6, 8: 5, 6: 4}
		hp_gained = randint(1, level_up_hit_die[self.class_type.hit_die]) + self.ability_modifiers.con
		hp_gained = max(1, hp_gained)
		self.max_hit_points += hp_gained
		self.hit_points += hp_gained

		display_msg.append(f"New level #{self.level} gained!!!")
		display_msg.append(f"{self.name} gained {hp_gained} hit points")

		# Handle ability score changes due to aging (PROCEDURE GAINLOST from original Wizardry)
		attrs = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charism"]
		for attr in attrs:
			val = self.abilities.get_value_by_name(name=attr)
			if randint(0, 3) % 4:  # 75% chance
				if randint(0, 129) < self.age // 52:  # Age check (age in weeks)
					# Lose ability due to age
					if val == 18 and randint(0, 5) != 4:
						continue
					val -= 1
					if attr == "Constitution" and val == 2:
						display_msg.append("** YOU HAVE DIED OF OLD AGE **")
						self.status = "LOST"
						self.hit_points = 0
					else:
						display_msg.append(f"You lost {attr}")
				elif val < 18:
					# Gain ability
					val += 1
					display_msg.append(f"You gained {attr}")
			self.abilities.set_value_by_name(name=attr, value=val)

		# Handle spell learning for spellcasters
		if self.class_type.can_cast and tome_spells:
			available_spell_levels = [
				i + 1 for i, slot in enumerate(self.class_type.spell_slots[self.level]) if slot > 0
			]

			# Calculate new spells to learn
			if self.level > 1:
				new_spells_known_count = (
					self.class_type.spells_known[self.level - 1] -
					self.class_type.spells_known[self.level - 2]
				)
				new_cantrip_count = 0
				if self.class_type.cantrips_known:
					new_cantrip_count = (
						self.class_type.cantrips_known[self.level - 1] -
						self.class_type.cantrips_known[self.level - 2]
					)
			else:
				new_spells_known_count = self.class_type.spells_known[0] if self.class_type.spells_known else 0
				new_cantrip_count = self.class_type.cantrips_known[0] if self.class_type.cantrips_known else 0

			# Filter learnable spells
			learnable_spells = [
				s for s in tome_spells
				if s.level <= max(available_spell_levels)
				and s not in self.sc.learned_spells
				and hasattr(s, 'damage_type') and s.damage_type
			]

			# Update spell slots
			self.sc.spell_slots = deepcopy(self.class_type.spell_slots[self.level])

			# Sort by level (highest first)
			learnable_spells.sort(key=lambda s: s.level, reverse=True)

			# Learn new spells
			new_spells_count = 0
			while learnable_spells and (new_spells_known_count > 0 or new_cantrip_count > 0):
				learned_spell = learnable_spells.pop()

				if learned_spell.level == 0 and new_cantrip_count > 0:
					new_cantrip_count -= 1
					self.sc.learned_spells.append(learned_spell)
					new_spells.append(learned_spell)
					new_spells_count += 1
					display_msg.append(f"Learned cantrip: {learned_spell.name}")
				elif learned_spell.level > 0 and new_spells_known_count > 0:
					new_spells_known_count -= 1
					self.sc.learned_spells.append(learned_spell)
					new_spells.append(learned_spell)
					new_spells_count += 1
					display_msg.append(f"Learned spell: {learned_spell.name} (level {learned_spell.level})")

			if new_spells_count:
				display_msg.append(f"You learned {new_spells_count} new spell(s)!!!")
		elif self.class_type.can_cast:
			# Update spell slots even if no tome_spells provided
			if self.level <= len(self.class_type.spell_slots):
				self.sc.spell_slots = deepcopy(self.class_type.spell_slots[self.level])

		# Format messages
		messages = '\n'.join(display_msg)

		# Print if verbose
		if verbose:
			print(messages)

		return messages, new_spells

	def attack(self, monster, in_melee: bool = True, cast: bool = True, verbose: bool = False) -> tuple:
		"""
		Attack a monster with weapon or spell.

		Args:
			monster: Monster to attack
			in_melee: If True, melee combat. If False, ranged combat.
			cast: If True, can cast spells. If False, only weapon attacks.
			verbose: If True, print messages. If False, only return them.

		Returns:
			tuple: (messages: str, damage: int)
		"""
		from random import randint

		display_msg: List[str] = []
		damage_roll = 0

		def prof_bonus(x):
			return x // 5 + 2 if x < 5 else (x - 5) // 4 + 3

		# Try to cast spell if possible
		castable_spells = []
		if self.is_spell_caster:
			cantrip_spells = [s for s in self.sc.learned_spells if not s.level]
			slot_spells = [s for s in self.sc.learned_spells if s.level and self.sc.spell_slots[s.level - 1] > 0 and hasattr(s, 'damage_type') and s.damage_type]
			castable_spells = cantrip_spells + slot_spells

		if cast and castable_spells and not in_melee:
			# Cast spell attack
			attack_spell = max(castable_spells, key=lambda s: s.level)
			spell_msg, damage_roll = self.cast_attack(attack_spell, monster, verbose=False)
			display_msg.append(spell_msg)
			if not attack_spell.is_cantrip:
				self.update_spell_slots(spell=attack_spell)
		else:
			# Weapon attack
			damage_multi = 0
			for _ in range(self.multi_attacks):
				if self.hit_points <= 0:
					break
				attack_roll = randint(1, 20) + self.ability_modifiers.get_value_by_index("str") + prof_bonus(self.level)
				if attack_roll >= monster.armor_class:
					damage_roll = self.damage_dice.roll()
					if damage_roll:
						attack_type = self.weapon.damage_type.index.replace("ing", "es") if self.weapon and hasattr(self.weapon, 'damage_type') else "punches"
						display_msg.append(f"{self.name} {attack_type} {monster.name} for {damage_roll} hit points!")

						# Check restrained condition
						if self.conditions and any(e.index == "restrained" for e in self.conditions):
							damage_roll //= 2
							self.hit_points -= damage_roll
							display_msg.append(f"{self.name} inflicts himself {damage_roll} hit points!")
							if self.hit_points <= 0:
								display_msg.append(f"{self.name} *** IS DEAD ***!")
						damage_multi += damage_roll
				else:
					display_msg.append(f"{self.name} misses {monster.name}!")
			damage_roll = damage_multi

		messages = '\n'.join(display_msg)
		if verbose:
			print(messages)

		return messages, damage_roll

	def cast_attack(self, spell, target, verbose: bool = False) -> tuple:
		"""
		Cast an offensive spell on a target.

		Args:
			spell: Spell to cast
			target: Target (Monster or Character)
			verbose: If True, print messages. If False, only return them.

		Returns:
			tuple: (messages: str, damage: int)
		"""
		from random import randint

		display_msg: List[str] = []
		total_damage = 0

		display_msg.append(f"{self.name} CAST SPELL ** {spell.name.upper()} ** on {target.name}")

		ability_modifier = int(self.ability_modifiers.get_value_by_index(name=self.class_type.spellcasting_ability))
		damages = spell.get_spell_damages(caster_level=self.level, ability_modifier=ability_modifier)

		if spell.dc_type:
			# Saving throw spell
			if target.saving_throw(dc_type=spell.dc_type, dc_value=self.dc_value):
				if spell.dc_success == "half":
					for damage in damages:
						total_damage += damage.roll() // 2
					display_msg.append(f"{target.name} resists the Spell!")
					display_msg.append(f"{target.name} is hit for {total_damage} hit points!")
				else:
					display_msg.append(f"{target.name} resists the Spell!")
			else:
				for damage in damages:
					total_damage += damage.roll()
				display_msg.append(f"{target.name} is hit for {total_damage} hit points!")
		else:
			# Direct attack spell
			def prof_bonus(x):
				return x // 5 + 2 if x < 5 else (x - 5) // 4 + 3

			attack_roll = randint(1, 20) + ability_modifier + prof_bonus(self.level)
			if attack_roll >= target.armor_class:
				for damage in damages:
					total_damage += damage.roll()
				display_msg.append(f"{target.name} is hit for {total_damage} hit points!")
			else:
				display_msg.append(f"{self.name} misses {target.name}!")

		messages = '\n'.join(display_msg)
		if verbose:
			print(messages)

		return messages, total_damage

	def victory(self, monster, solo_mode: bool = False, verbose: bool = False) -> tuple:
		"""
		Handle victory over a monster (XP and gold gain).

		Args:
			monster: Defeated monster
			solo_mode: If True, also gain gold
			verbose: If True, print messages. If False, only return them.

		Returns:
			tuple: (messages: str, xp_gained: int, gold_gained: int)
		"""
		from random import randint
		from math import floor

		display_msg: List[str] = []

		# Gain XP
		self.xp += monster.xp
		if hasattr(self, 'kills'):
			self.kills.append(monster)

		# Gain gold if solo mode
		gold_gained = 0
		gold_msg = ""
		if solo_mode:
			gold_dice = randint(1, 3)
			if gold_dice == 1:
				max_gold = max(1, floor(10 * monster.xp / monster.level))
				gold_gained = randint(1, max_gold + 1)
				gold_msg = f" and found {gold_gained} gp!"
				self.gold += gold_gained

		display_msg.append(f"{self.name} gained {monster.xp} XP{gold_msg}!")

		messages = '\n'.join(display_msg)
		if verbose:
			print(messages)

		return messages, monster.xp, gold_gained

	def drink(self, potion, verbose: bool = False) -> tuple:
		"""
		Drink a potion.

		Args:
			potion: Potion to drink
			verbose: If True, print messages. If False, only return them.

		Returns:
			tuple: (messages: str, success: bool, hp_restored: int)
		"""
		from random import randint
		import time
		from ..equipment import HealingPotion, SpeedPotion, StrengthPotion

		display_msg: List[str] = []
		hp_restored = 0

		# Check level requirement
		if not hasattr(potion, "min_level"):
			potion.min_level = 1
		if self.level < potion.min_level:
			messages = ""
			if verbose:
				print(messages)
			return messages, False, 0

		# Apply potion effects
		if isinstance(potion, StrengthPotion):
			self.str_effect_modifier = potion.value
			if hasattr(self, 'str_effect_timer'):
				self.str_effect_timer = time.time()
			display_msg.append(f"{self.name} drinks {potion.name} and gains *strength*!")

		elif isinstance(potion, SpeedPotion):
			if hasattr(self, 'hasted'):
				self.hasted = True
			if hasattr(self, 'haste_timer'):
				self.haste_timer = time.time()
			self.speed *= 2
			if hasattr(self, 'ac_bonus'):
				self.ac_bonus = 2
			if hasattr(self, 'multi_attack_bonus'):
				self.multi_attack_bonus = 1
			if not hasattr(self, "st_advantages"):
				self.st_advantages = []
			self.st_advantages += ["dex"]
			display_msg.append(f"{self.name} drinks {potion.name} potion and is *hasted*!")

		else:
			# Healing potion
			hp_to_recover = self.max_hit_points - self.hit_points
			if hasattr(potion, 'hit_dice'):
				dice_count, roll_dice = map(int, potion.hit_dice.split("d"))
				hp_restored = potion.bonus + sum([randint(1, roll_dice) for _ in range(dice_count)])
			else:
				# Fallback for potions without hit_dice
				hp_restored = randint(2, 7)

			self.hit_points = min(self.hit_points + hp_restored, self.max_hit_points)

			if hp_to_recover <= hp_restored:
				display_msg.append(f"{self.name} drinks {potion.name} potion and is *fully* healed!")
			else:
				display_msg.append(f"{self.name} drinks {potion.name} potion and has {min(hp_to_recover, hp_restored)} hit points restored!")

		messages = '\n'.join(display_msg)
		if verbose:
			print(messages)

		return messages, True, hp_restored

	def equip(self, item, verbose: bool = False) -> tuple:
		"""
		Equip or unequip an item (weapon, armor, shield).

		Args:
			item: Item to equip/unequip
			verbose: If True, print messages. If False, only return them.

		Returns:
			tuple: (messages: str, success: bool)
		"""
		from ..equipment import Armor, Weapon

		display_msg: List[str] = []
		success = False

		if isinstance(item, Armor):
			if item.index == "shield":
				# Shield logic
				if self.used_shield:
					if item == self.used_shield:
						# Un-equip shield
						item.equipped = not item.equipped
						display_msg.append(f"{self.name} un-equipped {item.name}")
						success = True
					else:
						display_msg.append(f"Hero cannot equip {item.name} - Please un-equip {self.used_shield.name} first!")
				else:
					if self.used_weapon:
						is_two_handed = any(p.index == "two-handed" for p in self.used_weapon.properties if hasattr(self.used_weapon, 'properties'))
						if is_two_handed:
							display_msg.append(f"Hero cannot equip {item.name} with a 2-handed weapon - Please un-equip {self.used_weapon.name} first!")
						else:
							# Equip shield
							item.equipped = not item.equipped
							display_msg.append(f"{self.name} equipped {item.name}")
							success = True
					else:
						# Equip shield
						item.equipped = not item.equipped
						display_msg.append(f"{self.name} equipped {item.name}")
						success = True
			else:
				# Armor logic
				if self.used_armor:
					if item == self.used_armor:
						# Un-equip armor
						item.equipped = not item.equipped
						display_msg.append(f"{self.name} un-equipped {item.name}")
						success = True
					else:
						display_msg.append(f"Hero cannot equip {item.name} - Please un-equip {self.used_armor.name} first!")
				else:
					if hasattr(item, 'str_minimum') and self.strength < item.str_minimum:
						display_msg.append(f"Hero cannot equip {item.name} - Minimum strength required is {item.str_minimum}!")
					else:
						# Equip armor
						item.equipped = not item.equipped
						display_msg.append(f"{self.name} equipped {item.name}")
						success = True

		elif isinstance(item, Weapon):
			if self.used_weapon:
				if item == self.used_weapon:
					# Un-equip weapon
					item.equipped = not item.equipped
					display_msg.append(f"{self.name} un-equipped {item.name}")
					success = True
				else:
					display_msg.append(f"Hero cannot equip {item.name} - Please un-equip {self.used_weapon.name} first!")
			else:
				is_two_handed = any(p.index == "two-handed" for p in item.properties if hasattr(item, 'properties'))
				if is_two_handed and self.used_shield:
					display_msg.append(f"Hero cannot equip {item.name} with a shield - Please un-equip {self.used_shield.name} first!")
				else:
					# Equip weapon
					item.equipped = not item.equipped
					display_msg.append(f"{self.name} equipped {item.name}")
					success = True
		else:
			display_msg.append(f"Hero cannot equip {item.name}!")

		messages = '\n'.join(display_msg)
		if verbose:
			print(messages)

		return messages, success

	def treasure(self, weapons, armors, equipments, potions, solo_mode: bool = False, verbose: bool = False) -> tuple:
		"""
		Find random treasure.

		Args:
			weapons: Available weapons
			armors: Available armors
			equipments: Available equipment
			potions: Available potions
			solo_mode: Solo mode flag
			verbose: If True, print messages. If False, only return them.

		Returns:
			tuple: (messages: str, found_item)
		"""
		from random import randint, choice
		from ..equipment import Armor, Weapon, HealingPotion

		display_msg: List[str] = []
		found_item = None

		if self.is_full:
			display_msg.append(f"{self.name}'s inventory is full - no treasure!!!")
		else:
			free_slot = min([i for i, item in enumerate(self.inventory) if item is None])
			treasure_dice = randint(1, 3)

			if treasure_dice == 1:
				# Potion
				potion = choice(potions)
				display_msg.append(f"{self.name} found a {potion.name} potion!")
				self.inventory[free_slot] = potion
				found_item = potion

			elif treasure_dice == 2:
				# Weapon
				new_weapon = choice(self.prof_weapons)
				if not self.weapon or (hasattr(new_weapon, 'damage_dice') and hasattr(self.weapon, 'damage_dice') and new_weapon.damage_dice > self.weapon.damage_dice):
					display_msg.append(f"{self.name} found a better weapon {new_weapon.name}!")
				else:
					display_msg.append(f"{self.name} found a lesser weapon {new_weapon.name}!")
				self.inventory[free_slot] = new_weapon
				found_item = new_weapon

			else:
				# Armor
				if self.prof_armors:
					new_armor = choice(self.prof_armors)
					if hasattr(new_armor, 'armor_class') and new_armor.armor_class.get("base", 0) > self.armor_class:
						display_msg.append(f"{self.name} found a better armor {new_armor.name}!")
						for item in self.inventory:
							if isinstance(item, Armor) and item.equipped:
								item.equipped = False
					else:
						display_msg.append(f"{self.name} found a lesser armor {new_armor.name}!")
					self.inventory[free_slot] = new_armor
					found_item = new_armor

		messages = '\n'.join(display_msg)
		if verbose:
			print(messages)

		return messages, found_item

	def cancel_haste_effect(self, verbose: bool = False) -> tuple:
		"""
		Cancel haste effect from speed potion.

		Args:
			verbose: If True, print messages. If False, only return them.

		Returns:
			tuple: (messages: str,)
		"""
		display_msg: List[str] = []

		if hasattr(self, 'hasted'):
			self.hasted = False

		# Reset speed based on race
		if hasattr(self, 'race') and hasattr(self.race, 'index'):
			self.speed = 25 if self.race.index in ["dwarf", "halfling", "gnome"] else 30
		else:
			self.speed = 30

		if hasattr(self, 'ac_bonus'):
			self.ac_bonus = 0
		if hasattr(self, 'multi_attack_bonus'):
			self.multi_attack_bonus = 0

		if not hasattr(self, "st_advantages"):
			self.st_advantages = []
		if "dex" in self.st_advantages:
			self.st_advantages.remove("dex")

		display_msg.append(f"{self.name} is no longer *hasted*!")

		messages = '\n'.join(display_msg)
		if verbose:
			print(messages)

		return (messages,)

	def cancel_strength_effect(self, verbose: bool = False) -> tuple:
		"""
		Cancel strength effect from strength potion.

		Args:
			verbose: If True, print messages. If False, only return them.

		Returns:
			tuple: (messages: str,)
		"""
		display_msg: List[str] = []

		if hasattr(self, 'str_effect_modifier'):
			self.str_effect_modifier = -1

		display_msg.append(f"{self.name} is no longer *strong*!")

		messages = '\n'.join(display_msg)
		if verbose:
			print(messages)

		return (messages,)

	def update_spell_slots(self, spell, slot_level: int = None):
		"""
		Update spell slots after casting a spell.

		Args:
			spell: Spell that was cast
			slot_level: Optional specific slot level to use
		"""
		if not self.is_spell_caster:
			return

		slot_level = slot_level + 1 if slot_level else spell.level

		# Warlock uses different slot mechanics
		if hasattr(self.class_type, 'name') and self.class_type.name == "Warlock":
			# Warlock implementation would go here
			pass
		else:
			# Standard spellcaster
			if slot_level > 0 and slot_level <= len(self.sc.spell_slots):
				self.sc.spell_slots[slot_level - 1] -= 1

	@property
	def multi_attacks(self) -> int:
		"""
		Calculate number of attacks per round based on class and level.
		"""
		if not hasattr(self, 'class_type'):
			return 1

		if hasattr(self.class_type, 'index'):
			if self.class_type.index == "fighter":
				attack_counts = 1 if self.level < 5 else 2 if self.level < 11 else 3
			elif self.class_type.index in ("paladin", "ranger", "monk", "barbarian"):
				attack_counts = 1 if self.level < 5 else 2
			else:
				attack_counts = 1
		else:
			attack_counts = 1

		if hasattr(self, "multi_attack_bonus"):
			return attack_counts + self.multi_attack_bonus
		return attack_counts

	@property
	def used_armor(self):
		"""Get currently equipped armor (excluding shield)."""
		from ..equipment import Armor
		equipped_armors = [item for item in self.inventory if isinstance(item, Armor) and item.equipped and item.name != "Shield"]
		return equipped_armors[0] if equipped_armors else None

	@property
	def used_shield(self):
		"""Get currently equipped shield."""
		from ..equipment import Armor
		equipped_shields = [item for item in self.inventory if isinstance(item, Armor) and item.name == "Shield" and item.equipped]
		return equipped_shields[0] if equipped_shields else None

	@property
	def used_weapon(self):
		"""Get currently equipped weapon."""
		equipped_weapons = [item for item in self.inventory if isinstance(item, Weapon) and item.equipped]
		return equipped_weapons[0] if equipped_weapons else None

	@property
	def is_full(self) -> bool:
		"""Check if inventory is full."""
		return all(item for item in self.inventory)

	@property
	def prof_weapons(self):
		"""Get all weapons this character is proficient with."""
		weapons = []
		if hasattr(self, 'proficiencies'):
			for p in self.proficiencies:
				if hasattr(p, 'type') and hasattr(p, 'ref'):
					from ..classes import ProfType
					if p.type == ProfType.WEAPON:
						weapons += p.ref if isinstance(p.ref, list) else [p.ref]
		return list(filter(None, weapons))

	@property
	def prof_armors(self):
		"""Get all armors this character is proficient with."""
		armors = []
		if hasattr(self, 'proficiencies'):
			for p in self.proficiencies:
				if hasattr(p, 'type') and hasattr(p, 'ref'):
					from ..classes import ProfType
					if p.type == ProfType.ARMOR:
						armors += p.ref if isinstance(p.ref, list) else [p.ref]
		return list(filter(None, armors))

	def saving_throw(self, dc_type: str, dc_value: int) -> bool:
		"""
		Make a saving throw.

		Args:
			dc_type: Ability type for saving throw (str, dex, con, etc.)
			dc_value: Difficulty class

		Returns:
			bool: True if saving throw succeeds
		"""
		from random import randint

		def ability_mod(x):
			return (x - 10) // 2

		def prof_bonus(x):
			return x // 5 + 2 if x < 5 else (x - 5) // 4 + 3

		st_type = f"saving-throw-{dc_type}"
		prof_modifiers = []

		if hasattr(self, 'proficiencies'):
			prof_modifiers = [p.value for p in self.proficiencies if hasattr(p, 'index') and st_type == p.index]

		if prof_modifiers:
			ability_modifier = prof_modifiers[0]
		else:
			ability_modifier = ability_mod(self.abilities.get_value_by_index(dc_type)) + prof_bonus(self.level)

		# Check for advantage
		if hasattr(self, "st_advantages") and dc_type in self.st_advantages:
			return any(randint(1, 20) + ability_modifier > dc_value for _ in range(2))
		else:
			return randint(1, 20) + ability_modifier > dc_value

	def choose_best_potion(self):
		"""
		Choose the best healing potion based on HP to recover.

		Returns:
			HealingPotion: The best potion to use
		"""
		from ..equipment import HealingPotion

		hp_to_recover = self.max_hit_points - self.hit_points
		healing_potions = [p for p in self.inventory if isinstance(p, HealingPotion)]

		if not healing_potions:
			return None

		available_potions = [
			p for p in healing_potions
			if p.max_hp_restored >= hp_to_recover and
			hasattr(p, "min_level") and
			self.level >= p.min_level
		]

		if available_potions:
			# Choose potion that heals just enough (avoid waste)
			return min(available_potions, key=lambda p: p.max_hp_restored)
		else:
			# Choose best available potion
			return max(healing_potions, key=lambda p: p.max_hp_restored)

	def choose_best_potion(self):
		"""
		Choose the best healing potion based on HP to recover.

		Returns:
			HealingPotion: The best potion to use
		"""
		from ..equipment import HealingPotion

		hp_to_recover = self.max_hit_points - self.hit_points
		healing_potions = [p for p in self.inventory if isinstance(p, HealingPotion)]

		if not healing_potions:
			return None

		available_potions = [
			p for p in healing_potions
			if p.max_hp_restored >= hp_to_recover and
			hasattr(p, "min_level") and
			self.level >= p.min_level
		]

		return (
			min(available_potions, key=lambda p: p.max_hp_restored)
			if available_potions
			else max(healing_potions, key=lambda p: p.max_hp_restored)
		)

	def cancel_haste_effect(self):
		"""Cancel the haste effect and reset attributes."""
		self.hasted = False
		self.speed = 25 if self.race.index in ["dwarf", "halfling", "gnome"] else 30
		self.ac_bonus = 0
		self.multi_attack_bonus = 0
		if not hasattr(self, "st_advantages"):
			self.st_advantages = ["dex"]
		if "dex" in self.st_advantages:
			self.st_advantages.remove("dex")

	def cancel_strength_effect(self):
		"""Cancel the strength effect."""
		self.str_effect_modifier = -1

