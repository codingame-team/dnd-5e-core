# Migration des Monstres de 5e.tools vers dnd-5e-core

Ce document décrit la migration des fonctionnalités liées aux monstres de 5e.tools depuis DnD-5th-Edition-API vers dnd-5e-core.

## Vue d'ensemble

Les monstres de 5e.tools sont des créatures qui ne sont pas incluses dans l'API officielle D&D 5e mais qui sont disponibles sur le site https://5e.tools/. Ces monstres ont une structure JSON légèrement différente et nécessitent un traitement spécial.

## Modules migrés

### 1. `dnd_5e_core/entities/extended_monsters.py`

**Classe principale:** `FiveEToolsMonsterLoader`

Ce module gère le chargement et la recherche des monstres depuis les fichiers JSON de 5e.tools.

**Fonctionnalités:**
- Chargement des monstres implémentés (`bestiary-sublist-data.json`)
- Chargement de tous les monstres disponibles (`bestiary-sublist-data-all-monsters.json`)
- Recherche de monstres par nom, source, CR, type
- Statistiques sur les monstres chargés

**Exemple d'utilisation:**
```python
from dnd_5e_core.entities import get_extended_monster_loader

loader = get_extended_monster_loader()

# Récupérer un monstre
orc = loader.get_monster_by_name("Orc Eye of Gruumsh")

# Rechercher des monstres
goblins = loader.search_monsters(name_contains="goblin", min_cr=1, max_cr=3)

# Obtenir des statistiques
stats = loader.get_stats()
print(f"Total: {stats['total']} monstres")
```

### 2. `dnd_5e_core/entities/special_monster_actions.py`

**Classe principale:** `SpecialMonsterActionsBuilder`

Ce module encapsule la logique de construction des actions et capacités spéciales pour chaque monstre de 5e.tools. Il remplace la fonction volumineuse `get_special_monster_actions()` de `populate_functions.py` par une architecture plus modulaire.

**Fonctionnalités:**
- Architecture de builder pattern pour les actions de monstres
- 47 monstres implémentés avec leurs actions complètes
- Vérification de l'implémentation des monstres
- Liste des monstres implémentés

**Note:** Les fonctions de construction individuelles lèvent `NotImplementedError` car elles doivent être appelées depuis `populate_functions.py` avec les bonnes dépendances (request_damage_type, request_spell, etc.).

**Exemple d'utilisation:**
```python
from dnd_5e_core.entities import get_special_actions_builder

builder = get_special_actions_builder()

# Vérifier si un monstre est implémenté
if builder.is_implemented("Orc Eye of Gruumsh"):
    print("Ce monstre a ses actions implémentées")

# Lister tous les monstres implémentés
implemented = builder.get_implemented_monsters()
print(f"{len(implemented)} monstres avec actions")
```

### 3. `dnd_5e_core/utils/token_downloader.py`

**Fonctions principales:**
- `download_image()`: Télécharge une image depuis une URL
- `download_monster_token()`: Télécharge le token d'un monstre depuis 5e.tools
- `download_tokens_batch()`: Télécharge les tokens pour plusieurs monstres

Ce module remplace le script `tools/download_tokens.py` de DnD-5th-Edition-API.

**Exemple d'utilisation:**
```python
from dnd_5e_core.utils import download_monster_token, download_tokens_batch

# Télécharger un seul token
download_monster_token("Orc Eye of Gruumsh", source="MM", save_folder="tokens")

# Télécharger plusieurs tokens
monsters = [
    ("Orc Eye of Gruumsh", "MM"),
    ("Goblin Boss", "MM"),
    ("Hobgoblin Captain", "MM"),
]
results = download_tokens_batch(monsters, save_folder="tokens")
```

### 4. Données JSON

**Emplacement:** `dnd_5e_core/data/monsters/`

Deux fichiers JSON:
- `bestiary-sublist-data.json`: 89 monstres implémentés avec actions
- `bestiary-sublist-data-all-monsters.json`: Tous les monstres disponibles sur 5e.tools

## Migration depuis populate_functions.py

### Avant (DnD-5th-Edition-API)

```python
# Dans populate_functions.py (ligne 488-1400+)
def get_special_monster_actions(name: str) -> tuple[List[Action], List[SpecialAbility], SpellCaster]:
    actions: List[Action] = []
    special_abilities: List[SpecialAbility] = []
    spell_caster: SpellCaster = None
    
    if name == "Orc Eye of Gruumsh":
        # 100+ lignes de code pour ce monstre...
    elif name == "Ogre Bolt Launcher":
        # 50+ lignes de code...
    # ... 40+ autres elif avec 900+ lignes au total
    
    return actions, special_abilities, spell_caster
```

### Après (avec dnd-5e-core)

```python
# Dans populate_functions.py
from dnd_5e_core.entities import get_special_actions_builder, get_extended_monster_loader

# Obtenir les instances
loader = get_extended_monster_loader()
builder = get_special_actions_builder()

# Utiliser le loader pour récupérer les données JSON
monster_data = loader.get_monster_by_name("Orc Eye of Gruumsh")

# Vérifier si les actions sont implémentées
if builder.is_implemented("Orc Eye of Gruumsh"):
    # La logique de construction reste dans populate_functions.py
    # mais le builder structure l'architecture
    actions, special_abilities, spell_caster = get_special_monster_actions("Orc Eye of Gruumsh")
```

## Avantages de la migration

1. **Séparation des responsabilités:**
   - Chargement des données → `extended_monsters.py`
   - Construction des actions → `special_monster_actions.py`
   - Téléchargement des images → `token_downloader.py`

2. **Réutilisabilité:**
   - Les modules peuvent être utilisés par tous les projets du workspace
   - Les données JSON sont centralisées

3. **Maintenabilité:**
   - Architecture modulaire au lieu d'une fonction volumineuse
   - Facilite l'ajout de nouveaux monstres
   - Meilleure organisation du code

4. **Testabilité:**
   - Tests unitaires possibles pour chaque module
   - Script de test fourni: `test_extended_monsters.py`

## Prochaines étapes

### Pour intégrer dans DnD-5th-Edition-API

1. Modifier `populate_functions.py` pour utiliser `dnd-5e-core`:
   ```python
   # Ajouter en haut du fichier
   from dnd_5e_core.entities import get_extended_monster_loader, get_special_actions_builder
   
   # Remplacer la fonction get_special_monster_actions()
   # par des appels au builder
   ```

2. Mettre à jour les scripts qui utilisent `tools/download_tokens.py`:
   ```python
   # Remplacer
   from tools.download_tokens import download_image
   
   # Par
   from dnd_5e_core.utils import download_monster_token
   ```

3. Supprimer les fichiers obsolètes:
   - `maze/other_monsters/bestiary-sublist-data.json` (déplacé vers dnd-5e-core)
   - `maze/other_monsters/bestiary-sublist-data-all-monsters.json` (déplacé vers dnd-5e-core)
   - `tools/download_tokens.py` (remplacé par `token_downloader.py`)

### Pour étendre la fonctionnalité

1. **Ajouter un nouveau monstre implémenté:**
   - Ajouter son nom dans `_register_action_builders()` de `special_monster_actions.py`
   - Créer une fonction `_build_nouveau_monstre()`
   - L'implémenter dans `populate_functions.py`

2. **Télécharger des tokens manquants:**
   ```python
   from dnd_5e_core.entities import get_extended_monster_loader
   from dnd_5e_core.utils import download_tokens_batch
   
   loader = get_extended_monster_loader()
   monsters = loader.load_implemented_monsters()
   
   # Créer la liste des tuples (nom, source)
   monster_list = [(m['name'], m['source']) for m in monsters]
   
   # Télécharger tous les tokens
   download_tokens_batch(monster_list, save_folder="images/monsters/tokens")
   ```

## Tests

Exécuter les tests:
```bash
cd /Users/display/PycharmProjects/dnd-5e-core
python test_extended_monsters.py
```

Résultats attendus:
- ✓ Chargement de 89 monstres implémentés
- ✓ 47 monstres avec actions implémentées
- ✓ Recherche et filtrage fonctionnels
- ⚠ 3 monstres avec actions mais absents du JSON (normal, ils sont dans l'API officielle)

## Sources de données

- **5e.tools**: https://5e.tools/
- **Fichiers JSON**: Extraits du site 5e.tools
- **Images (tokens)**: https://5e.tools/img/bestiary/tokens/{SOURCE}/{MONSTER_NAME}.webp

## Statistiques

- **Total de monstres dans le JSON**: 89
- **Monstres avec actions implémentées**: 47
- **Sources représentées**: MM, MPMM, VGTM
- **Types de créatures**: 12 types différents

## Support

Pour toute question ou problème, consulter:
- `dnd_5e_core/data/monsters/README.md` - Documentation des données
- `test_extended_monsters.py` - Exemples d'utilisation
- `populate_functions.py` - Implémentation des actions dans DnD-5th-Edition-API

