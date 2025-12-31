"""
D&D 5e Core - Collection Loader
Functions to load D&D 5e API collection indexes from local JSON files
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict, Any, Optional


# Default collections directory
_COLLECTIONS_DIR = None


def set_collections_directory(path: str):
    """
    Set the collections directory path.

    Args:
        path: Path to the collections directory containing JSON files
    """
    global _COLLECTIONS_DIR
    _COLLECTIONS_DIR = Path(path)


def get_collections_directory() -> Path:
    """
    Get the collections directory path.

    Returns:
        Path to collections directory
    """
    global _COLLECTIONS_DIR

    if _COLLECTIONS_DIR is None:
        # Try to find collections directory automatically
        current_file = Path(__file__)

        # Try common locations
        possible_paths = [
            # If collections is in the dnd-5e-core package itself (preferred)
            current_file.parent.parent.parent / "collections",
            # If used from DnD-5th-Edition-API project (fallback)
            current_file.parent.parent.parent.parent.parent / "DnD-5th-Edition-API" / "collections",
            # If collections is in current working directory
            Path.cwd() / "collections",
        ]

        for path in possible_paths:
            if path.exists() and path.is_dir():
                _COLLECTIONS_DIR = path
                break
        else:
            raise FileNotFoundError(
                f"Collections directory not found. Tried: {possible_paths}\n"
                f"Use set_collections_directory() to specify the location."
            )

    return _COLLECTIONS_DIR


def load_collection(collection_name: str, collections_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load a collection index file.

    Args:
        collection_name: Name of the collection (e.g., 'monsters', 'spells')
        collections_path: Optional custom path to collections directory

    Returns:
        Dictionary with 'count' and 'results' keys

    Raises:
        FileNotFoundError: If collection file doesn't exist
    """
    if collections_path:
        collections_dir = Path(collections_path)
    else:
        collections_dir = get_collections_directory()

    file_path = collections_dir / f"{collection_name}.json"

    if not file_path.exists():
        raise FileNotFoundError(f"Collection file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def populate(collection_name: str, key_name: str = "results",
             with_url: bool = False, collection_path: Optional[str] = None) -> List:
    """
    Load and extract data from a collection file.

    This function maintains compatibility with the original populate() function
    from DnD-5th-Edition-API.

    Args:
        collection_name: Name of the collection file (without .json extension)
        key_name: Key to extract from the JSON (default: 'results')
        with_url: If True, return tuples of (index, url), otherwise just indexes
        collection_path: Optional custom path to collections directory

    Returns:
        List of indexes or (index, url) tuples

    Example:
        >>> monsters = populate('monsters', 'results')
        >>> ['aboleth', 'goblin', ...]
        >>>
        >>> monsters_with_urls = populate('monsters', 'results', with_url=True)
        >>> [('aboleth', '/api/monsters/aboleth'), ...]
    """
    data = load_collection(collection_name, collection_path)

    collection_json_list = data.get(key_name, [])

    if with_url:
        data_list = [(json_data['index'], json_data['url'])
                     for json_data in collection_json_list]
    else:
        data_list = [json_data['index'] for json_data in collection_json_list]

    return data_list


def get_collection_count(collection_name: str, collection_path: Optional[str] = None) -> int:
    """
    Get the count of items in a collection.

    Args:
        collection_name: Name of the collection
        collection_path: Optional custom path to collections directory

    Returns:
        Number of items in the collection
    """
    data = load_collection(collection_name, collection_path)
    return data.get('count', 0)


def get_collection_item(collection_name: str, index: str,
                        collection_path: Optional[str] = None) -> Optional[Dict[str, str]]:
    """
    Get a specific item from a collection by its index.

    Args:
        collection_name: Name of the collection
        index: Index/slug of the item to find
        collection_path: Optional custom path to collections directory

    Returns:
        Dictionary with 'index', 'name', and 'url' keys, or None if not found
    """
    data = load_collection(collection_name, collection_path)
    results = data.get('results', [])

    for item in results:
        if item['index'] == index:
            return item

    return None


def list_all_collections(collections_path: Optional[str] = None) -> List[str]:
    """
    List all available collection files.

    Args:
        collections_path: Optional custom path to collections directory

    Returns:
        List of collection names (without .json extension)
    """
    if collections_path:
        collections_dir = Path(collections_path)
    else:
        collections_dir = get_collections_directory()

    collection_files = sorted(collections_dir.glob("*.json"))
    return [f.stem for f in collection_files if f.name != "README.md"]


# Convenience functions for common collections

def get_monsters_list(with_url: bool = False) -> List:
    """Get list of all monsters."""
    return populate('monsters', 'results', with_url=with_url)


def get_spells_list(with_url: bool = False) -> List:
    """Get list of all spells."""
    return populate('spells', 'results', with_url=with_url)


def get_classes_list(with_url: bool = False) -> List:
    """Get list of all classes."""
    return populate('classes', 'results', with_url=with_url)


def get_races_list(with_url: bool = False) -> List:
    """Get list of all races."""
    return populate('races', 'results', with_url=with_url)


def get_equipment_list(with_url: bool = False) -> List:
    """Get list of all equipment."""
    return populate('equipment', 'results', with_url=with_url)


def get_weapons_list(with_url: bool = False) -> List:
    """Get list of all weapons."""
    return populate('weapons', 'results', with_url=with_url)


def get_armors_list(with_url: bool = False) -> List:
    """Get list of all armors."""
    return populate('armors', 'results', with_url=with_url)


def get_magic_items_list(with_url: bool = False) -> List:
    """Get list of all magic items."""
    return populate('magic-items', 'results', with_url=with_url)


if __name__ == "__main__":
    # Example usage
    print("Available collections:")
    for collection in list_all_collections():
        count = get_collection_count(collection)
        print(f"  - {collection}: {count} items")

    print("\nExample: First 5 monsters:")
    monsters = get_monsters_list()
    for monster in monsters[:5]:
        print(f"  - {monster}")

