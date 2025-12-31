# D&D 5e JSON Data

This directory contains JSON data files for Dungeons & Dragons 5th Edition, downloaded from the [D&D 5e API](https://www.dnd5eapi.co/).

## 📊 Contents

### Core Game Data
- **monsters/** - 332 monster stat blocks (CR 0 to 30)
- **spells/** - 319 spells (cantrips to 9th level)
- **classes/** - 12 character classes
- **races/** - 9 playable races
- **subclasses/** - 12 subclass options
- **subraces/** - 4 racial variants

### Equipment & Items
- **weapons/** - 65 weapons (simple and martial)
- **armors/** - 30 armor types
- **equipment/** - 237 general equipment items
- **magic-items/** - 239 magical items
- **equipment-categories/** - 39 equipment categories

### Character Options
- **features/** - 377 class and race features
- **traits/** - 38 racial and background traits
- **proficiencies/** - 117 skill and tool proficiencies
- **backgrounds/** - Character backgrounds
- **feats/** - Special abilities and feats

### Rules & Reference
- **skills/** - 18 skill definitions
- **ability-scores/** - 6 ability scores (STR, DEX, CON, INT, WIS, CHA)
- **alignments/** - 9 alignment types
- **conditions/** - 15 status conditions
- **damage-types/** - 13 damage types
- **magic-schools/** - 8 schools of magic
- **weapon-properties/** - 11 weapon properties
- **languages/** - 16 languages
- **rules/** - Core rules
- **rule-sections/** - 30 rule sections

### Other
- **names/** - Name lists for character generation

## 📝 Data Format

All data files are in JSON format following the D&D 5e API schema.

Example: `monsters/goblin.json`
```json
{
  "index": "goblin",
  "name": "Goblin",
  "size": "Small",
  "type": "humanoid",
  "armor_class": 15,
  "hit_points": 7,
  "challenge_rating": 0.25,
  "xp": 50,
  ...
}
```

## 🔄 Updates

These files were downloaded from the D&D 5e API on various dates:
- Initial download: March 15, 2022
- Monsters update: May 10, 2023
- Classes update: January 15, 2023
- Spells update: January 12, 2023
- Weapons update: July 2, 2024

## 📖 Usage

The `dnd_5e_core.data` module provides convenient loader functions:

```python
from dnd_5e_core.data import load_monster, list_monsters

# List all available monsters
monsters = list_monsters()
print(f"Total monsters: {len(monsters)}")  # 332

# Load a specific monster
goblin = load_monster("goblin")
print(f"Name: {goblin['name']}")
print(f"HP: {goblin['hit_points']}")
print(f"CR: {goblin['challenge_rating']}")
```

## 📜 License

The D&D 5e API data is provided under the [Open Game License (OGL)](https://dnd.wizards.com/resources/systems-reference-document).

All data is copyright Wizards of the Coast and is used in accordance with the OGL.

## 🔗 Source

Original data source: [D&D 5e API](https://www.dnd5eapi.co/)

Download script: See `DnD-5th-Edition-API/download_json.py` for the original download script.

## 📊 Statistics

- **Total Files**: ~2,000+ JSON files
- **Total Size**: ~8.7 MB
- **Categories**: 27 different categories
- **Last Updated**: December 23, 2024 (migrated to dnd-5e-core)

