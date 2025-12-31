# dnd-5e-core

A complete Python package implementing D&D 5th Edition core rules and mechanics.

This package contains **all game logic** for D&D 5e and is **UI-agnostic** - use it with pygame, ncurses, web, or any other interface.

## ✨ New in Latest Version

**🎉 Integrated D&D 5e Data**: The package now includes **8.7 MB of D&D 5e JSON data** (2000+ files) with:
- 332 monsters
- 319 spells
- 65 weapons
- 30 armors
- 237 equipment items
- And much more!

**🎮 Extended Monsters from 5e.tools**: Access to **89+ additional monsters** from 5e.tools:
- Monsters not in the official API (Orc Eye of Gruumsh, Goblin Boss, etc.)
- 47 monsters with complete actions and abilities implemented
- Support for downloading monster tokens/images
- Advanced search and filtering capabilities

**No external API or database required** - all data is bundled and **auto-detected**.

## Features

### Complete D&D 5e Implementation

- **Entities**: Monster and Character classes with full D&D 5e mechanics
- **Races & Subraces**: All official races with ability bonuses, traits, proficiencies
- **Classes**: All character classes with spellcasting, proficiencies
- **Equipment**: Weapons (with properties, ranges), Armor (AC calculation), Potions
- **Spells**: Complete spellcasting system with spell slots, cantrips, DC
- **Combat**: Actions, Multi-attacks, Special Abilities, Conditions
- **Abilities**: Six core abilities (STR, DEX, CON, INT, WIS, CHA) with modifiers
- **Saving Throws**: Full saving throw system with proficiencies
- **Experience & Leveling**: XP calculation, level progression
- **Challenge Rating**: Encounter difficulty calculation

### Integrated Data

- **✅ Bundled JSON Data**: 2000+ D&D 5e data files included
- **✅ Auto-Detection**: No configuration needed - data is found automatically
- **✅ Offline Mode**: Works without internet connection
- **✅ Complete**: Monsters, spells, weapons, armors, classes, races, and more

## Installation

```bash
pip install dnd-5e-core
```

Or for development:

```bash
git clone https://github.com/codingame-team/dnd-5e-core.git
cd dnd-5e-core
pip install -e .[dev]
```

## Quick Start

### Load D&D 5e Data (New!)

```python
from dnd_5e_core.data import load_monster, list_monsters, load_spell

# List all available monsters
monsters = list_monsters()
print(f"Total monsters: {len(monsters)}")  # 332

# Load a specific monster
goblin = load_monster('goblin')
print(f"Name: {goblin['name']}")
print(f"HP: {goblin['hit_points']}")
print(f"CR: {goblin['challenge_rating']}")

# Load a spell
fireball = load_spell('fireball')
print(f"Spell: {fireball['name']}, Level: {fireball['level']}")
```

**Note**: Data directory is **auto-detected** - no configuration needed!

### Create a Character

```python
from dnd_5e_core.entities import Character
from dnd_5e_core.races import Race
from dnd_5e_core.classes import ClassType
from dnd_5e_core.abilities import Abilities

# Load race and class from API
race = Race.load_from_api("elf")
class_type = ClassType.load_from_api("wizard")

# Create abilities
abilities = Abilities(
    strength=10,
    dexterity=14,
    constitution=12,
    intelligence=16,
    wisdom=13,
    charisma=8
)

# Create character
wizard = Character(
    name="Gandalf",
    race=race,
    class_type=class_type,
    abilities=abilities,
    level=1,
    hit_points=8,
    max_hit_points=8,
    gold=100
)

# Equip weapon
from dnd_5e_core.equipment import Weapon
staff = Weapon.load_from_api("quarterstaff")
wizard.inventory.append(staff)
staff.equipped = True

print(f"{wizard.name} - Level {wizard.level} {wizard.race.name} {wizard.class_type.name}")
print(f"AC: {wizard.armor_class}, HP: {wizard.hit_points}/{wizard.max_hit_points}")
```

### Create a Monster

```python
from dnd_5e_core.entities import Monster

# Load from API
orc = Monster.load_from_api("orc")

print(f"{orc.name} - CR {orc.challenge_rating}")
print(f"AC: {orc.armor_class}, HP: {orc.hit_points}")
print(f"Actions: {[a.name for a in orc.actions]}")
```

### Extended Monsters from 5e.tools (New!)

```python
from dnd_5e_core.entities import get_extended_monster_loader

# Load the monster loader
loader = get_extended_monster_loader()

# Search for monsters
goblins = loader.search_monsters(name_contains="goblin", min_cr=1, max_cr=3)
print(f"Found {len(goblins)} goblin variants")

# Get a specific monster with full data
orc_eye = loader.get_monster_by_name("Orc Eye of Gruumsh")
print(f"{orc_eye['name']} - CR {orc_eye['cr']}")
print(f"HP: {orc_eye['hp']['average']}, Source: {orc_eye['source']}")

# Get statistics
stats = loader.get_stats()
print(f"Total extended monsters: {stats['total']}")
print(f"Sources: {list(stats['by_source'].keys())}")

# Download monster tokens
from dnd_5e_core.utils import download_monster_token

download_monster_token("Orc Eye of Gruumsh", source="MM", save_folder="tokens")
```

### Combat System

```python
from dnd_5e_core.combat import CombatSystem

combat = CombatSystem()

# Add participants
combat.add_character(wizard)
combat.add_monster(orc)

# Start combat
combat.start()

# Combat round
while not combat.is_finished():
    current_actor = combat.current_turn()

    if isinstance(current_actor, Character):
        # Character attacks monster
        target = combat.get_monsters()[0]
        action = current_actor.actions[0]
        damage = current_actor.attack(target, action)
        print(f"{current_actor.name} attacks {target.name} for {damage} damage!")

    elif isinstance(current_actor, Monster):
        # Monster attacks character
        target = combat.get_characters()[0]
        action = current_actor.actions[0]
        damage = current_actor.attack(target, action)
        print(f"{current_actor.name} attacks {target.name} for {damage} damage!")

    combat.next_turn()

winners = combat.get_winners()
print(f"Combat finished! Winners: {[w.name for w in winners]}")
```

### Spellcasting

```python
from dnd_5e_core.spells import Spell

# Character must have spellcasting ability
if wizard.is_spell_caster:
    # Load spell from API
    fireball = Spell.load_from_api("fireball")

    # Check if can cast
    if wizard.can_cast(fireball):
        # Cast spell at target
        damage = wizard.cast_attack(orc, fireball)
        print(f"{wizard.name} casts Fireball on {orc.name} for {damage} damage!")

        # Saving throw
        if orc.saving_throw(dc_type=fireball.dc_type, dc_value=wizard.dc_value):
            print(f"{orc.name} succeeded saving throw!")
```

## Architecture

This package follows **separation of concerns**:

### What this package DOES:
- All D&D 5e game rules and mechanics
- Character/Monster creation and management
- Combat resolution and damage calculation
- Spell casting and effects
- Equipment management
- Saving throws, ability checks
- Experience and leveling
- Data loading from D&D 5e API

### What this package DOES NOT do:
- User interface (no pygame, no ncurses, no GUI)
- Game loop management
- Graphics rendering
- Sound effects
- Input handling
- Save file management (provides serialization only)

### Your application provides:
- UI layer (console, GUI, web, etc.)
- Game state management
- User input handling
- Rendering and display
- Save/load game state using provided serialization

## Usage in Your Project

```python
# Your game imports dnd-5e-core for game logic
from dnd_5e_core.entities import Character, Monster
from dnd_5e_core.combat import CombatSystem

# You provide the UI
import pygame  # or curses, or tkinter, or web framework

# Game loop (you control this)
while running:
    # Handle input (your code)
    key = get_user_input()

    # Call game logic (dnd-5e-core)
    if key == "attack":
        damage = player.attack(monster)

    # Render (your code)
    render_game_state(player, monster)
```

## Data Sources

The package can load data from:
1. **D&D 5e API** (https://www.dnd5eapi.co/) - Default
2. **Local JSON files** - For offline mode
3. **Custom data** - Implement your own loader

## Testing

```bash
pytest tests/
```

## Documentation

See `/docs` folder for detailed documentation:
- Entity System
- Combat Mechanics
- Spellcasting System
- Equipment Guide
- **Extended Monsters from 5e.tools** - See [EXTENDED_MONSTERS_MIGRATION.md](docs/EXTENDED_MONSTERS_MIGRATION.md)
- API Reference

## License

MIT License - See LICENSE file for details

## Contributing

See CONTRIBUTING.md for guidelines.

## Credits

Based on D&D 5th Edition rules © Wizards of the Coast.
This is a fan-made implementation for educational purposes.
