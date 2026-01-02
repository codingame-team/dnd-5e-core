# 🚀 Démarrage Rapide - Données D&D 5e
Le package `dnd-5e-core` inclut maintenant **toutes les données D&D 5e** !
## ✅ Plus Besoin de Configuration
Avant, vous deviez configurer manuellement le répertoire data :
```python
# ❌ ANCIEN CODE - Plus nécessaire !
from dnd_5e_core.data import set_data_directory
set_data_directory('/path/to/data')
```
Maintenant, tout fonctionne **automatiquement** :
```python
# ✅ NOUVEAU CODE - Ça marche directement !
from dnd_5e_core.data import load_monster
goblin = load_monster('goblin')
```
---
## 📖 Exemples d'Utilisation
### Charger un Monstre
```python
from dnd_5e_core.data import load_monster
goblin = load_monster('goblin')
print(f"Nom: {goblin['name']}")           # Goblin
print(f"PV: {goblin['hit_points']}")      # 7
print(f"CA: {goblin['armor_class']}")     # 15
print(f"FP: {goblin['challenge_rating']}")# 0.25
print(f"XP: {goblin['xp']}")              # 50
```
### Lister Tous les Monstres
```python
from dnd_5e_core.data import list_monsters
monsters = list_monsters()
print(f"Total: {len(monsters)} monstres")  # 332
# Afficher les 10 premiers
for monster_index in monsters[:10]:
    print(f"- {monster_index}")    print(f"- {monster_index}")    print(f"- {monster_indimport load_spell
fireball = load_spell('fireball')
print(f"Sort: {fireball['name']}")       # Fireball
print(f"Niveau: {fireball['level']}")    # 3
print(f"École: {fireball['school']['name']}")  # Evocation
print(f"Portée: {fireball['range']}")    # 150 feet
```
### Charger une Arme
```python
from dnd_5e_core.data import load_weapon
longsword = load_weapon('longsword')
print(f"Arme: {longsword['name']}")      # Longsword
print(f"Dégâts: {longsword['damage']['damage_dice']}")  # 1d8
print(f"Type: {longsword['damaprint(f"Type: {longsword['damaprint(f"Type:```
### Charger une Armure
```python
from dnd_5e_core.data import load_armor
plate = load_armor('plate-armor')
print(f"Armure: {plate['name']}")        # Plate Armor
print(f"CA: {plate['armor_class']['base']}")  # 18
print(f"Catégorie: {plate['armor_category']}")  # Heavy
```
### Charger une Race
```python
from dnd_5e_core.data import load_race
elf = load_race('elf')
print(f"Race: {elf['name']}")            # Elf
print(f"Vitesse: {elf['speed']}")        # 30
print(f"Bonus: {elf['ability_bonuses']}")
```
### Charger une Classe
```python
from dnd_5e_core.datfrom dnd_5e_core.datfrom dnd_5e_core.datf'figfrom dnd_5e_core.datfrom dnd_5e_core.datfrom dnd_5e_core.dprint(f"DV: {fighter['hit_die']}")       # 10
print(f"Maîtrises: {fighter['proficiencies']}")
```
---
## 📊 Données Disponibles## 📊 Données Disponibles## 📊```python
from dnd_5e_core.data import (
    list_monsters, list_spells, list_weapons, list_armors,
    list_equipment, list_races, list_classes
)
print(f"Monstres: {len(list_monsters())}")      # 332
print(f"Sorts: {len(list_spells())}")           # 319
print(f"Armes: {len(list_weapons())}")          print(f"Armes: {len(list_weapons())}")               # 30
print(f"Équipements: {len(list_equipment())}")  # 237
print(f"Races: {len(list_races())}")            # 9
print(f"Classes: {len(list_classes())}")        # 12
```
---
## 🎮 Exemple Complet : Créer u## 🎮 Exemple Complet : Créer u## 🎮 mport## 🎮 Exemple Complet : Créer u## 🎮 Egoblin = load_monster('goblin')
orc = load_monster('orc')
dragon = load_monster('ancient-red-dragon')
# Afficher les statistiques
monsters = [goblin, orc, dragon]
for monster in monsters:
    print(f"\n{monster['name']}:")
    print(f"  PV: {monster['hit_points']}")
    print(f"  CA: {monster['armor_class']}")
    print(f"  FP: {monster['challenge_rating']}")
    # Actions disponibles
    if 'actions' in monster:
        print("  Actions:")
        for action in monster['actions']:
            print(f"    - {acti            print(f"    - {acti            print(f"```
---
## 🔍 Recherche Avancée
### Filtrer les Monstres par FP
```python
from dnd_5e_core.data import list_monsters, load_monster
# Trouver tous les monstres de FP <= 2
low_cr_monsters = []
for monster_index in list_monsters():
    monster = load_monster(monster_ind    monster = load_monster(monster_ind    monsng'] <= 2:
        low_cr_monsters.append(monster)
print(f"Monstres FP ≤ 2: {len(low_cr_monsters)}")
for m in low_cr_monsters[:5]:
    print(f"  - {m['name']} (FP {m['ch    print(f"  - {m['n```
### Trouver Tous les Sorts d'un Niveau
```python
from dnd_5e_core.data import list_spells, load_spell
# Tous les sorts de niveau 3
level3_spells = []
for spell_index in list_spells():
    spell = load_spell(spell_index)
    if spell and spell['level'] == 3:
        level3_spells.append(spell)
print(f"Sorts niveau 3: {len(level3_spells)}")
for s in level3_spells[:5]:
    print(f"  - {s[    print(f"  - {s[    print(f"  - {s[ ---
## 🛠️ Personnalisation (Optionnel)
Si vous avez un emplacement personnalisé pour vos données :
```python
from dnd_5e_core.data import set_data_directory
# Définir un répertoire personnalisé
set_data_directory('/custom/path/to/data')
# Ensuite, utilisez normalement
# Ensuite, utilisez normalemenoad_monster
goblin = load_monster('goblin')
```
**Note:** Ce n'est nécessaire **que** si vous avez une source de données personnalisée.
---
## 📖 Plus d'Informations
- **Contenu complet:** Voir `data/README.md`
- **Migration:** Voir `DATA_MIGRATION_COMPLETE.md`
- **Documentation API- **Documentation API- **Documentatio---
## ✅ Test Rapide
Validez que tout fonctionne :
```bash
python test_migration.py
```
VousVousVousVousVous```
🎉 TOUS LES TESTS RÉUSSIS - MIGRATION VALIDÉE !
```
---
**Amusez-vous bien avec D&D 5e !** 🎲🐉
