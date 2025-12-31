# Guide d'intégration dans populate_functions.py

Ce document explique comment intégrer les nouveaux modules de monstres étendus dans le fichier `populate_functions.py` de DnD-5th-Edition-API.

## Étape 1 : Ajouter les imports

Au début de `populate_functions.py`, ajouter :

```python
# Imports pour les monstres étendus de 5e.tools
from dnd_5e_core.entities import get_extended_monster_loader, get_special_actions_builder

# Initialiser les instances globales
_extended_monster_loader = get_extended_monster_loader()
_special_actions_builder = get_special_actions_builder()
```

## Étape 2 : Créer une fonction helper

Ajouter cette fonction helper pour récupérer les données JSON des monstres :

```python
def get_extended_monster_data(name: str) -> Optional[Dict[str, Any]]:
    """
    Récupère les données JSON d'un monstre étendu de 5e.tools
    
    :param name: Nom du monstre
    :return: Dictionnaire avec les données du monstre ou None
    """
    return _extended_monster_loader.get_monster_by_name(name)
```

## Étape 3 : Vérifier l'implémentation des actions

Modifier la fonction `get_special_monster_actions()` pour vérifier d'abord si le monstre est implémenté :

```python
def get_special_monster_actions(name: str) -> tuple[List[Action], List[SpecialAbility], SpellCaster]:
    """
    Récupère les actions et capacités spéciales pour un monstre de 5e.tools
    
    Note: Cette fonction est maintenant intégrée avec dnd-5e-core
    """
    actions: List[Action] = []
    special_abilities: List[SpecialAbility] = []
    spell_caster: SpellCaster = None
    
    # Vérifier si le monstre est implémenté
    if not _special_actions_builder.is_implemented(name):
        print(f"[WARNING] Monster '{name}' does not have special actions implemented")
        return actions, special_abilities, spell_caster
    
    # Le reste du code existant...
    if name == "Orc Eye of Gruumsh":
        # Code existant...
    elif name == "Ogre Bolt Launcher":
        # Code existant...
    # ... etc.
    
    return actions, special_abilities, spell_caster
```

## Étape 4 : Utiliser les données JSON (optionnel)

Si vous voulez utiliser les données JSON au lieu de les coder en dur, vous pouvez faire :

```python
def create_monster_from_5etools(name: str) -> Optional[Monster]:
    """
    Crée un monstre à partir des données de 5e.tools
    
    :param name: Nom du monstre
    :return: Instance de Monster ou None
    """
    # Récupérer les données JSON
    data = get_extended_monster_data(name)
    if not data:
        return None
    
    # Récupérer les actions spéciales
    actions, special_abilities, spell_caster = get_special_monster_actions(name)
    
    # Extraire les données de base
    cr = data.get('cr', 0)
    if isinstance(cr, dict):
        cr = cr.get('cr', 0)
    if isinstance(cr, str) and '/' in cr:
        num, den = cr.split('/')
        cr = float(num) / float(den)
    else:
        cr = float(cr)
    
    # Construire le monstre
    # Note: Adapter selon votre structure de données
    monster = Monster(
        index=data.get('name', '').lower().replace(' ', '-'),
        name=data['name'],
        abilities=create_abilities_from_data(data),  # À implémenter
        proficiencies=[],  # À extraire des données
        armor_class=extract_ac(data),  # À implémenter
        hit_points=data.get('hp', {}).get('average', 0),
        hit_dice=data.get('hp', {}).get('formula', '1d8'),
        xp=calculate_xp_from_cr(cr),  # À implémenter
        speed=extract_speed(data),  # À implémenter
        challenge_rating=cr,
        actions=actions,
        sc=spell_caster,
        sa=special_abilities
    )
    
    return monster
```

## Étape 5 : Fonctions utilitaires

Ajouter ces fonctions pour extraire les données :

```python
def extract_ac(data: Dict[str, Any]) -> int:
    """Extrait l'AC depuis les données 5e.tools"""
    ac_data = data.get('ac', [])
    if isinstance(ac_data, list) and len(ac_data) > 0:
        ac_entry = ac_data[0]
        if isinstance(ac_entry, dict):
            return ac_entry.get('ac', 10)
        return ac_entry
    return 10

def extract_speed(data: Dict[str, Any]) -> int:
    """Extrait la vitesse depuis les données 5e.tools"""
    speed_data = data.get('speed', {})
    if isinstance(speed_data, dict):
        walk = speed_data.get('walk', 30)
        if isinstance(walk, dict):
            return walk.get('number', 30)
        return walk
    return 30

def create_abilities_from_data(data: Dict[str, Any]) -> Abilities:
    """Crée un objet Abilities depuis les données 5e.tools"""
    return Abilities(
        strength=data.get('str', 10),
        dexterity=data.get('dex', 10),
        constitution=data.get('con', 10),
        intelligence=data.get('int', 10),
        wisdom=data.get('wis', 10),
        charisma=data.get('cha', 10)
    )

def calculate_xp_from_cr(cr: float) -> int:
    """Calcule l'XP à partir du CR"""
    xp_by_cr = {
        0: 10, 0.125: 25, 0.25: 50, 0.5: 100,
        1: 200, 2: 450, 3: 700, 4: 1100, 5: 1800,
        6: 2300, 7: 2900, 8: 3900, 9: 5000, 10: 5900,
        # ... compléter selon la table D&D 5e
    }
    return xp_by_cr.get(cr, int(cr * 1000))
```

## Étape 6 : Exemple d'utilisation complète

```python
# Dans votre code principal
from populate_functions import create_monster_from_5etools

# Créer un monstre étendu
orc_eye = create_monster_from_5etools("Orc Eye of Gruumsh")
if orc_eye:
    print(f"Created {orc_eye.name} with {len(orc_eye.actions)} actions")
    
# Lister tous les monstres implémentés
from dnd_5e_core.entities import get_special_actions_builder

builder = get_special_actions_builder()
implemented = builder.get_implemented_monsters()
print(f"Total monsters with actions: {len(implemented)}")
```

## Étape 7 : Télécharger les tokens

Ajouter une fonction pour télécharger les tokens des monstres utilisés :

```python
from dnd_5e_core.utils import download_monster_token

def download_monster_tokens(monster_names: List[str], output_folder: str = "./images/monsters/tokens"):
    """
    Télécharge les tokens pour une liste de monstres
    
    :param monster_names: Liste des noms de monstres
    :param output_folder: Dossier de destination
    """
    from dnd_5e_core.entities import get_extended_monster_loader
    
    loader = get_extended_monster_loader()
    monster_list = []
    
    for name in monster_names:
        data = loader.get_monster_by_name(name)
        if data:
            source = data.get('source', 'MM')
            monster_list.append((name, source))
    
    if monster_list:
        from dnd_5e_core.utils import download_tokens_batch
        results = download_tokens_batch(monster_list, output_folder)
        return results
    
    return {}
```

## Notes importantes

1. **Dépendances** : Assurez-vous que `dnd-5e-core` est installé :
   ```bash
   pip install -e /path/to/dnd-5e-core
   ```

2. **Compatibilité** : Le code existant continue de fonctionner, on ajoute juste des fonctionnalités

3. **Performance** : Le loader met en cache les données JSON après le premier chargement

4. **Tests** : Tester chaque monstre après migration pour vérifier que les actions sont correctes

## Checklist de migration

- [ ] Ajouter les imports en haut de `populate_functions.py`
- [ ] Créer les fonctions helper
- [ ] Tester avec un monstre (ex: "Orc Eye of Gruumsh")
- [ ] Migrer progressivement les autres monstres
- [ ] Télécharger les tokens nécessaires
- [ ] Nettoyer les anciens fichiers JSON
- [ ] Mettre à jour la documentation du projet
- [ ] Exécuter les tests

## Support

Pour toute question :
- Consulter `docs/EXTENDED_MONSTERS_MIGRATION.md`
- Voir les exemples dans `test_extended_monsters.py`
- Vérifier le code de `dnd_5e_core/entities/extended_monsters.py`

