# Monstres Étendus de 5e.tools

Ce dossier contient les données des monstres provenant du site [5e.tools](https://5e.tools/), qui ne sont pas inclus dans l'API officielle D&D 5e.

## Fichiers

- **bestiary-sublist-data.json** : Liste des monstres implémentés avec leurs actions et capacités spéciales dans `populate_functions.py`
- **bestiary-sublist-data-all-monsters.json** : Liste complète de tous les monstres disponibles sur 5e.tools

## Structure des données

Les fichiers JSON suivent la structure de 5e.tools, qui est légèrement différente de l'API officielle :

```json
{
  "name": "Orc Eye of Gruumsh",
  "source": "MM",
  "page": 247,
  "size": ["M"],
  "type": {
    "type": "humanoid",
    "tags": ["orc"]
  },
  "alignment": ["C", "E"],
  "ac": [
    {
      "ac": 16,
      "from": ["{@item ring mail|phb}", "{@item shield|phb}"]
    }
  ],
  "hp": {
    "average": 45,
    "formula": "6d8 + 18"
  },
  "speed": {
    "walk": 30
  },
  "str": 16,
  "dex": 12,
  "con": 16,
  "int": 9,
  "wis": 13,
  "cha": 12,
  "cr": "2"
}
```

## Utilisation

### Charger les monstres implémentés

```python
from dnd_5e_core.entities.extended_monsters import get_loader

loader = get_loader()

# Charger tous les monstres implémentés
monsters = loader.load_implemented_monsters()

# Obtenir un monstre par son nom
orc = loader.get_monster_by_name("Orc Eye of Gruumsh")

# Rechercher des monstres
orcs = loader.search_monsters(name_contains="orc", min_cr=1, max_cr=3)
```

### Télécharger les tokens d'images

```python
from dnd_5e_core.utils.token_downloader import download_monster_token, download_tokens_batch

# Télécharger un seul token
download_monster_token("Orc Eye of Gruumsh", source="MM", save_folder="tokens")

# Télécharger plusieurs tokens
monsters_list = [
    ("Orc Eye of Gruumsh", "MM"),
    ("Goblin Boss", "MM"),
    ("Hobgoblin Captain", "MM"),
]
results = download_tokens_batch(monsters_list, save_folder="tokens")
```

## Sources disponibles

- **MM** : Monster Manual
- **VGTM** : Volo's Guide to Monsters
- **MPMM** : Mordenkainen Presents: Monsters of the Multiverse
- **MTF** : Mordenkainen's Tome of Foes
- Et bien d'autres...

## Notes

Les monstres listés dans `bestiary-sublist-data.json` ont leurs actions et capacités spéciales implémentées dans la fonction `get_special_monster_actions()` du fichier `populate_functions.py`.

Pour les autres monstres, les données sont disponibles mais les actions et capacités spéciales doivent être implémentées manuellement.

## Contribution

Pour ajouter un nouveau monstre implémenté :

1. Vérifier qu'il existe dans `bestiary-sublist-data-all-monsters.json`
2. L'ajouter à `bestiary-sublist-data.json`
3. Implémenter ses actions dans `get_special_monster_actions()`
4. Télécharger son token avec `token_downloader.py`

