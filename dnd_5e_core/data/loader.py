"""
D&D 5e Core - Data Loader
Functions to load D&D 5e data from local JSON files
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional, List, Dict, Any


# Default data directory (can be overridden)
_DATA_DIR = None


def set_data_directory(path: str):
    """
    Set the data directory path.

    Args:
        path: Path to the data directory containing JSON files
    """
    global _DATA_DIR
    _DATA_DIR = Path(path)


def get_data_directory() -> Path:
    """
    Get the data directory path.

    Returns:
        Path to data directory
    """
    global _DATA_DIR

    if _DATA_DIR is None:
        # Try to find data directory automatically
        current_file = Path(__file__)

        # Try common locations
        possible_paths = [
            # If data is in the dnd-5e-core package itself (preferred)
            current_file.parent.parent.parent / "data",
            # If used from DnD-5th-Edition-API project (fallback)
            current_file.parent.parent.parent.parent.parent / "DnD-5th-Edition-API" / "data",
            # If data is in current working directory
            Path.cwd() / "data",
        ]

        for path in possible_paths:
            if path.exists() and path.is_dir():
                _DATA_DIR = path
                break

        if _DATA_DIR is None:
            raise FileNotFoundError(
                "Data directory not found. Please use set_data_directory() to specify the path."
            )

    return _DATA_DIR


def load_json_file(category: str, index: str) -> Optional[Dict[str, Any]]:
    """
    Load a JSON file from the data directory.

    Args:
        category: Category (e.g., "monsters", "spells", "weapons")
        index: Item index/name (e.g., "goblin", "fireball")

    Returns:
        Dict with data or None on error
    """
    try:
        data_dir = get_data_directory()
        file_path = data_dir / category / f"{index}.json"

        if not file_path.exists():
            # Silently return None for files not found (e.g., magic items in equipment collection)
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return data
    except Exception as e:
        # Only print error if DEBUG mode is enabled
        if os.getenv('DEBUG'):
            print(f"Error loading {category}/{index}: {e}")
        return None


def list_json_files(category: str) -> List[str]:
    """
    List all JSON files in a category.

    Args:
        category: Category (e.g., "monsters", "spells")

    Returns:
        List of indices (without .json extension)
    """
    try:
        data_dir = get_data_directory()
        category_dir = data_dir / category

        if not category_dir.exists():
            return []

        return [
            f.stem for f in category_dir.glob("*.json")
            if f.is_file()
        ]
    except Exception as e:
        print(f"Error listing {category}: {e}")
        return []


# ===== Loader Functions =====

def load_monster(index: str) -> Optional[Dict[str, Any]]:
    """
    Load monster data from local JSON file.

    Args:
        index: Monster index (e.g., "goblin", "ancient-red-dragon")

    Returns:
        Dict with monster data or None
    """
    return load_json_file("monsters", index)


def load_spell(index: str) -> Optional[Dict[str, Any]]:
    """
    Load spell data from local JSON file.

    Args:
        index: Spell index (e.g., "fireball", "magic-missile")

    Returns:
        Dict with spell data or None
    """
    return load_json_file("spells", index)


def load_weapon(index: str) -> Optional[Dict[str, Any]]:
    """
    Load weapon data from local JSON file.

    Args:
        index: Weapon index (e.g., "longsword", "dagger")

    Returns:
        Dict with weapon data or None
    """
    return load_json_file("weapons", index)


def load_armor(index: str) -> Optional[Dict[str, Any]]:
    """
    Load armor data from local JSON file.

    Args:
        index: Armor index (e.g., "plate-armor", "chain-mail")

    Returns:
        Dict with armor data or None
    """
    return load_json_file("armors", index)


def load_race(index: str) -> Optional[Dict[str, Any]]:
    """
    Load race data from local JSON file.

    Args:
        index: Race index (e.g., "elf", "dwarf", "human")

    Returns:
        Dict with race data or None
    """
    return load_json_file("races", index)


def load_class(index: str) -> Optional[Dict[str, Any]]:
    """
    Load class data from local JSON file.

    Args:
        index: Class index (e.g., "fighter", "wizard", "rogue")

    Returns:
        Dict with class data or None
    """
    return load_json_file("classes", index)


def load_equipment(index: str) -> Optional[Dict[str, Any]]:
    """
    Load equipment data from local JSON file.

    Args:
        index: Equipment index

    Returns:
        Dict with equipment data or None
    """
    return load_json_file("equipment", index)


def list_monsters() -> List[str]:
    """
    Get list of all available monsters from local files.

    Returns:
        List of monster indices
    """
    return list_json_files("monsters")


def list_spells() -> List[str]:
    """
    Get list of all available spells from local files.

    Returns:
        List of spell indices
    """
    return list_json_files("spells")


def list_equipment() -> List[str]:
    """
    Get list of all available equipment from local files.

    Returns:
        List of equipment indices
    """
    return list_json_files("equipment")


def list_weapons() -> List[str]:
    """
    Get list of all available weapons from local files.

    Returns:
        List of weapon indices
    """
    return list_json_files("weapons")


def list_armors() -> List[str]:
    """
    Get list of all available armors from local files.

    Returns:
        List of armor indices
    """
    return list_json_files("armors")


def list_races() -> List[str]:
    """
    Get list of all available races from local files.

    Returns:
        List of race indices
    """
    return list_json_files("races")


def list_classes() -> List[str]:
    """
    Get list of all available classes from local files.

    Returns:
        List of class indices
    """
    return list_json_files("classes")


def clear_cache():
    """
    Note: No cache needed when using local files.
    This function is kept for API compatibility.
    """
    print("No cache to clear (using local JSON files)")



# ===== Helper Functions =====

def parse_dice_notation(dice_str: str) -> tuple[int, int, int]:
    """
    Parse D&D dice notation.

    Args:
        dice_str: Dice string (e.g., "2d6+3", "1d8")

    Returns:
        Tuple of (dice_count, dice_sides, bonus)
    """
    import re

    # Match pattern like "2d6+3" or "1d8-2"
    match = re.match(r'(\d+)d(\d+)([\+\-]\d+)?', dice_str)
    if match:
        dice_count = int(match.group(1))
        dice_sides = int(match.group(2))
        bonus = int(match.group(3)) if match.group(3) else 0
        return dice_count, dice_sides, bonus

    return 1, 6, 0  # Default


def parse_challenge_rating(cr_value: Any) -> float:
    """
    Parse challenge rating value.

    Args:
        cr_value: CR value (can be float, int, or fraction string)

    Returns:
        Float CR value
    """
    if isinstance(cr_value, (int, float)):
        return float(cr_value)

    if isinstance(cr_value, str):
        if '/' in cr_value:
            # Fraction like "1/2", "1/4"
            num, denom = cr_value.split('/')
            return float(num) / float(denom)
        return float(cr_value)

    return 0.0


# ===== Example Usage =====

if __name__ == "__main__":
    # Note: Data directory is auto-detected from dnd-5e-core/data
    # No need to call set_data_directory() unless you have a custom location

    # Example: Load a goblin
    goblin_data = load_monster("goblin")
    if goblin_data:
        print(f"Loaded: {goblin_data.get('name', 'Unknown')}")
        print(f"CR: {goblin_data.get('challenge_rating', 'Unknown')}")
        print(f"HP: {goblin_data.get('hit_points', 'Unknown')}")

    # Example: List all monsters
    monsters = list_monsters()
    print(f"\nTotal monsters available: {len(monsters)}")
    print(f"First 5: {monsters[:5]}")

    # Example: Load fireball spell
    fireball_data = load_spell("fireball")
    if fireball_data:
        print(f"\nLoaded spell: {fireball_data.get('name', 'Unknown')}")
        print(f"Level: {fireball_data.get('level', 'Unknown')}")

