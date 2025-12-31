"""
D&D 5e Core - Data Module
Data loading from local JSON files
"""

from .loader import (
    set_data_directory, get_data_directory,
    load_monster, load_spell, load_weapon, load_armor,
    load_race, load_class, load_equipment,
    list_monsters, list_spells, list_equipment, list_weapons, list_armors,
    list_races, list_classes,
    clear_cache, parse_dice_notation, parse_challenge_rating
)

from .collections import (
    set_collections_directory, get_collections_directory,
    load_collection, populate, get_collection_count, get_collection_item,
    list_all_collections,
    get_monsters_list, get_spells_list, get_classes_list, get_races_list,
    get_equipment_list, get_weapons_list, get_armors_list, get_magic_items_list
)

__all__ = [
    # Data loader functions
    'set_data_directory', 'get_data_directory',
    'load_monster', 'load_spell', 'load_weapon', 'load_armor',
    'load_race', 'load_class', 'load_equipment',
    'list_monsters', 'list_spells', 'list_equipment', 'list_weapons', 'list_armors',
    'list_races', 'list_classes',
    'clear_cache', 'parse_dice_notation', 'parse_challenge_rating',
    # Collections functions
    'set_collections_directory', 'get_collections_directory',
    'load_collection', 'populate', 'get_collection_count', 'get_collection_item',
    'list_all_collections',
    'get_monsters_list', 'get_spells_list', 'get_classes_list', 'get_races_list',
    'get_equipment_list', 'get_weapons_list', 'get_armors_list', 'get_magic_items_list'
]

