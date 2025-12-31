# D&D 5e API Collections

This directory contains collection index files for Dungeons & Dragons 5th Edition, downloaded from the [D&D 5e API](https://www.dnd5eapi.co/).

## 📊 Contents

These JSON files contain indexes and lists of available resources in the D&D 5e API. They are used to discover what data is available before downloading specific items.

### Collections Available

- **ability-scores.json** - List of 6 ability scores (STR, DEX, CON, INT, WIS, CHA)
- **alignments.json** - List of 9 alignment types
- **armors.json** - Index of 30 armor types
- **backgrounds.json** - List of character backgrounds
- **classes.json** - Index of 12 character classes
- **conditions.json** - List of 15 status conditions
- **damage-types.json** - List of 13 damage types
- **equipment.json** - Index of 237 general equipment items
- **equipment-categories.json** - List of 39 equipment categories
- **feats.json** - Index of special abilities and feats
- **features.json** - Index of 377 class and race features
- **languages.json** - List of 16 languages
- **magic-items.json** - Index of 239 magical items
- **magic-schools.json** - List of 8 schools of magic
- **monsters.json** - Index of 332 monsters
- **proficiencies.json** - Index of 117 skill and tool proficiencies
- **races.json** - Index of 9 playable races
- **rule-sections.json** - Index of 30 rule sections
- **rules.json** - Index of core rules
- **skills.json** - List of 18 skill definitions
- **spells.json** - Index of 319 spells
- **subclasses.json** - Index of 12 subclass options
- **subraces.json** - Index of 4 racial variants
- **traits.json** - Index of 38 racial and background traits
- **weapon-properties.json** - List of 11 weapon properties
- **weapons.json** - Index of 65 weapons

## 📝 Data Format

All collection files follow the same basic structure:

```json
{
  "count": 123,
  "results": [
    {
      "index": "item-slug",
      "name": "Item Name",
      "url": "/api/category/item-slug"
    }
  ]
}
```

### Example: `monsters.json` (excerpt)

```json
{
  "count": 332,
  "results": [
    {
      "index": "aboleth",
      "name": "Aboleth",
      "url": "/api/monsters/aboleth"
    },
    {
      "index": "goblin",
      "name": "Goblin",
      "url": "/api/monsters/goblin"
    }
  ]
}
```

## 🔧 Usage

These collection files are used to:

1. **Discover available resources** - List all items in a category
2. **Download specific data** - Get URLs for individual items
3. **Populate menus and selectors** - Display available options to users
4. **Cache API endpoints** - Avoid repeated API calls for indexes

### Python Example

```python
import json
from pathlib import Path

def load_collection(collection_name: str):
    """Load a collection index file."""
    collections_dir = Path(__file__).parent
    with open(collections_dir / f"{collection_name}.json", "r") as f:
        return json.load(f)

# Get list of all monsters
monsters = load_collection("monsters")
print(f"Total monsters: {monsters['count']}")
for monster in monsters['results']:
    print(f"- {monster['name']} ({monster['index']})")
```

## 🔗 Related

- The actual detailed data for each item is stored in the `../data/` directory
- Use these collection files to find what's available
- Use the `url` field to download or access specific items

## 📚 Source

All data is sourced from the [D&D 5e API](https://www.dnd5eapi.co/).

## 📄 License

This data is made available under the Open Gaming License (OGL) and the System Reference Document (SRD).

