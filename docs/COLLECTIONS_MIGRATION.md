# Migration des Collections - dnd-5e-core

## 📚 Résumé

Le dossier `collections/` a été migré depuis `DnD-5th-Edition-API` vers `dnd-5e-core` pour centraliser toutes les données D&D 5e dans un seul package.

**Date de migration:** 23 décembre 2025

---

## 🎯 Objectif

Centraliser les fichiers de collections d'index de l'API D&D 5e dans le package `dnd-5e-core` pour :
- ✅ Éviter la duplication de données entre projets
- ✅ Faciliter la maintenance et les mises à jour
- ✅ Permettre une meilleure réutilisation du code
- ✅ Créer un package Python autonome et complet

---

## 📁 Structure Avant/Après

### Avant la Migration

```
DnD-5th-Edition-API/
├── collections/
│   ├── ability-scores.json
│   ├── alignments.json
│   ├── monsters.json
│   ├── spells.json
│   └── ... (26 fichiers)
└── populate_functions.py  # Utilise collections/

dnd-5e-core/
└── (pas de collections)
```

### Après la Migration

```
dnd-5e-core/
├── collections/                    # ✅ NOUVEAU
│   ├── README.md                   # Documentation des collections
│   ├── ability-scores.json
│   ├── alignments.json
│   ├── monsters.json
│   ├── spells.json
│   └── ... (26 fichiers)
└── dnd_5e_core/
    └── data/
        ├── collections.py          # ✅ NOUVEAU MODULE
        ├── loader.py
        └── __init__.py             # Mis à jour

DnD-5th-Edition-API/
├── collections/                    # Conservé pour compatibilité
└── populate_functions.py           # Peut maintenant importer de dnd-5e-core
```

---

## 🔧 Nouveau Module: `collections.py`

Un nouveau module `dnd_5e_core/data/collections.py` a été créé pour gérer les collections.

### Fonctions Principales

```python
from dnd_5e_core.data import (
    populate,                    # Fonction compatible avec l'ancien code
    load_collection,             # Charger une collection complète
    get_collection_count,        # Obtenir le nombre d'items
    get_collection_item,         # Obtenir un item spécifique
    list_all_collections,        # Lister toutes les collections disponibles
)

# Fonctions de convenance
from dnd_5e_core.data import (
    get_monsters_list,
    get_spells_list,
    get_classes_list,
    get_races_list,
    get_equipment_list,
    get_weapons_list,
    get_armors_list,
    get_magic_items_list,
)
```

---

## 📝 Guide de Migration du Code

### Ancien Code (DnD-5th-Edition-API)

```python
from populate_functions import populate

# Charger la liste des monstres
monsters = populate(collection_name='monsters', key_name='results')

# Avec URLs
monsters_with_urls = populate(
    collection_name='monsters', 
    key_name='results', 
    with_url=True
)
```

### Nouveau Code (dnd-5e-core)

```python
from dnd_5e_core.data import populate, get_monsters_list

# Option 1: Utiliser populate() (compatible)
monsters = populate('monsters', 'results')
monsters_with_urls = populate('monsters', 'results', with_url=True)

# Option 2: Utiliser la fonction de convenance (recommandé)
monsters = get_monsters_list()
monsters_with_urls = get_monsters_list(with_url=True)
```

### Exemple Avancé

```python
from dnd_5e_core.data import (
    load_collection,
    get_collection_count,
    get_collection_item,
    list_all_collections
)

# Lister toutes les collections disponibles
collections = list_all_collections()
print(f"Collections disponibles: {collections}")

# Obtenir le nombre de monstres
monster_count = get_collection_count('monsters')
print(f"Nombre de monstres: {monster_count}")

# Charger toute la collection
monsters_data = load_collection('monsters')
print(f"Count: {monsters_data['count']}")
print(f"Results: {len(monsters_data['results'])}")

# Obtenir un monstre spécifique
goblin = get_collection_item('monsters', 'goblin')
print(f"Goblin: {goblin['name']}, URL: {goblin['url']}")
```

---

## 🔄 Configuration du Chemin

Le module `collections.py` détecte automatiquement le chemin des collections. Vous pouvez aussi le définir manuellement :

```python
from dnd_5e_core.data import set_collections_directory

# Définir un chemin personnalisé
set_collections_directory('/path/to/collections')
```

Le module recherche automatiquement dans :
1. `dnd-5e-core/collections/` (préféré)
2. `DnD-5th-Edition-API/collections/` (fallback)
3. `./collections/` (répertoire courant)

---

## 📊 Fichiers Migrés

26 fichiers JSON ont été migrés :

| Collection | Items | Description |
|------------|-------|-------------|
| ability-scores | 6 | STR, DEX, CON, INT, WIS, CHA |
| alignments | 9 | Types d'alignement |
| armors | 30 | Types d'armures |
| backgrounds | - | Historiques de personnage |
| classes | 12 | Classes de personnage |
| conditions | 15 | Conditions de statut |
| damage-types | 13 | Types de dégâts |
| equipment | 237 | Équipement général |
| equipment-categories | 39 | Catégories d'équipement |
| feats | - | Dons spéciaux |
| features | 377 | Capacités de classe/race |
| languages | 16 | Langues |
| magic-items | 239 | Objets magiques |
| magic-schools | 8 | Écoles de magie |
| monsters | 332 | Monstres (CR 0-30) |
| proficiencies | 117 | Compétences et outils |
| races | 9 | Races jouables |
| rule-sections | 30 | Sections de règles |
| rules | - | Règles de base |
| skills | 18 | Compétences |
| spells | 319 | Sorts (cantrips à niveau 9) |
| subclasses | 12 | Options de sous-classe |
| subraces | 4 | Variantes raciales |
| traits | 38 | Traits raciaux/historique |
| weapon-properties | 11 | Propriétés d'armes |
| weapons | 65 | Armes simples et martiales |

---

## ✅ Avantages de la Migration

### Pour dnd-5e-core
- ✅ Package complet et autonome
- ✅ Toutes les données D&D 5e centralisées
- ✅ Facilite l'installation et la distribution
- ✅ API cohérente pour accéder aux données

### Pour DnD-5th-Edition-API
- ✅ Peut importer directement de dnd-5e-core
- ✅ Moins de duplication de code
- ✅ Mises à jour automatiques quand dnd-5e-core est mis à jour
- ✅ Code plus maintenable

### Pour les Développeurs
- ✅ Un seul endroit pour gérer les collections
- ✅ Documentation claire et complète
- ✅ Fonctions de convenance pour un usage facile
- ✅ Compatibilité avec l'ancien code

---

## 🚀 Prochaines Étapes

### 1. Mettre à Jour DnD-5th-Edition-API

Modifier `populate_functions.py` pour utiliser dnd-5e-core :

```python
# Option 1: Import direct (recommandé)
from dnd_5e_core.data import populate

# Option 2: Wrapper pour compatibilité
def populate(collection_name: str, key_name: str, with_url=False, collection_path: str = None):
    from dnd_5e_core.data import populate as core_populate
    return core_populate(collection_name, key_name, with_url, collection_path)
```

### 2. Ajouter dnd-5e-core aux Dépendances

Dans `DnD-5th-Edition-API/requirements.txt` :

```
-e ../dnd-5e-core
```

### 3. Tester la Migration

```bash
cd /Users/display/PycharmProjects/dnd-5e-core
python -m dnd_5e_core.data.collections
```

### 4. Mettre à Jour la Documentation

- ✅ README.md dans collections/
- ✅ Module collections.py documenté
- ✅ Ce guide de migration

---

## 🧪 Tests

```python
# Test basique
from dnd_5e_core.data import get_monsters_list, populate

monsters = get_monsters_list()
assert len(monsters) > 0
print(f"✅ {len(monsters)} monstres chargés")

# Test avec populate
spells = populate('spells', 'results')
assert len(spells) > 0
print(f"✅ {len(spells)} sorts chargés")

# Test avec URLs
weapons = populate('weapons', 'results', with_url=True)
assert all(isinstance(w, tuple) and len(w) == 2 for w in weapons)
print(f"✅ {len(weapons)} armes avec URLs chargées")
```

---

## 📖 Documentation

- **README des collections:** `/collections/README.md`
- **Module Python:** `/dnd_5e_core/data/collections.py`
- **Ce guide:** `/docs/COLLECTIONS_MIGRATION.md`

---

## ✅ Checklist de Migration

- [x] Créer le dossier `collections/` dans dnd-5e-core
- [x] Copier tous les fichiers JSON
- [x] Créer `collections/README.md`
- [x] Créer `dnd_5e_core/data/collections.py`
- [x] Mettre à jour `dnd_5e_core/data/__init__.py`
- [x] Créer ce guide de migration
- [ ] Mettre à jour `populate_functions.py` dans DnD-5th-Edition-API
- [ ] Tester l'import dans DnD-5th-Edition-API
- [ ] Mettre à jour CHANGELOG.md

---

## 🔍 Résolution de Problèmes

### Erreur: "Collections directory not found"

**Solution:**
```python
from dnd_5e_core.data import set_collections_directory
set_collections_directory('/path/to/dnd-5e-core/collections')
```

### Import Error

**Solution:**
```bash
# Installer dnd-5e-core en mode développement
cd /Users/display/PycharmProjects/dnd-5e-core
pip install -e .
```

### Les Collections ne se Chargent Pas

**Vérification:**
```python
from dnd_5e_core.data import get_collections_directory
print(get_collections_directory())
```

---

**Status:** ✅ **MIGRATION TERMINÉE**

**Prochaine étape:** Mettre à jour DnD-5th-Edition-API pour utiliser les collections de dnd-5e-core

