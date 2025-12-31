# 🚀 Plan de Migration - dao_classes.py → dnd-5e-core

## ✅ Progression

Date de début : 23 décembre 2024
Temps estimé total : 11-15 heures

---

## 📊 Phase 1 : Extraction des Classes de Base (COURS)

### ✅ Entities

- [x] **Sprite** → `dnd_5e_core/entities/sprite.py` ✅ FAIT
  - Classe de base pour Monster et Character
  - Code pygame supprimé (draw, draw_effect)
  - Méthodes de base conservées (pos, check_collision, move)

- [ ] **Monster** → `dnd_5e_core/entities/monster.py` 🔄 EN COURS
  - Dépend de : Sprite, Abilities, Proficiency, Action, SpecialAbility, SpellCaster
  - ~150 lignes de code
  - Nettoyer cprint()

- [ ] **Character** → `dnd_5e_core/entities/character.py`
  - Dépend de : Sprite, Race, ClassType, Abilities, Equipment, SpellCaster, Condition
  - ~600 lignes de code
  - Nettoyer cprint()

### 📋 Equipment (Priorité Haute - Beaucoup utilisé)

- [ ] **EquipmentCategory** → `dnd_5e_core/equipment/equipment.py`
- [ ] **Cost** → `dnd_5e_core/equipment/equipment.py`
- [ ] **Equipment** → `dnd_5e_core/equipment/equipment.py`
  - Classe de base pour Weapon, Armor, Potion

- [ ] **Weapon** → `dnd_5e_core/equipment/weapon.py`
  - Dépend de : Equipment, WeaponProperty, DamageType, DamageDice, WeaponRange
  - ~50 lignes
  
- [ ] **Armor** → `dnd_5e_core/equipment/armor.py`
  - Dépend de : Equipment
  - ~30 lignes

- [ ] **Potion** → `dnd_5e_core/equipment/potion.py`
  - HealingPotion, SpeedPotion, StrengthPotion
  - ~100 lignes total

- [ ] **Inventory** → `dnd_5e_core/equipment/inventory.py`

---

## 📊 Phase 2 : Classes Support

### 🧬 Abilities

- [ ] **Abilities** → `dnd_5e_core/abilities/abilities.py`
  - STR, DEX, CON, INT, WIS, CHA
  - ~50 lignes

### 🎲 Mechanics  

- [ ] **DamageDice** → `dnd_5e_core/mechanics/dice.py`
  - Utilisé partout
  - ~30 lignes

### 🏛️ Races

- [ ] **Language** → `dnd_5e_core/races/language.py`
- [ ] **Trait** → `dnd_5e_core/races/trait.py`
- [ ] **SubRace** → `dnd_5e_core/races/subrace.py`
- [ ] **Race** → `dnd_5e_core/races/race.py`

### 🎓 Classes

- [ ] **ProfType** (Enum) → `dnd_5e_core/classes/proficiency.py`
- [ ] **Proficiency** → `dnd_5e_core/classes/proficiency.py`
- [ ] **ClassType** → `dnd_5e_core/classes/class_type.py`
- [ ] **MultiClassing** → `dnd_5e_core/classes/multiclass.py`

---

## 📊 Phase 3 : Combat System

### ⚔️ Combat

- [ ] **ActionType** (Enum) → `dnd_5e_core/combat/action.py`
- [ ] **Damage** → `dnd_5e_core/combat/damage.py`
- [ ] **DamageType** → `dnd_5e_core/combat/damage.py`
- [ ] **Action** → `dnd_5e_core/combat/action.py`
- [ ] **SpecialAbility** → `dnd_5e_core/combat/special_ability.py`
- [ ] **Condition** → `dnd_5e_core/combat/condition.py`

---

## 📊 Phase 4 : Spellcasting System

### ✨ Spells

- [ ] **Spell** → `dnd_5e_core/spells/spell.py`
- [ ] **SpellCaster** → `dnd_5e_core/spells/spellcaster.py`
- [ ] **SpellSlot** → `dnd_5e_core/spells/spell_slots.py`

---

## 📊 Phase 5 : Extraction de populate_functions.py

### 📦 Data Loaders

- [ ] **populate()** → `dnd_5e_core/data/loader.py`
- [ ] **request_monster()** → `dnd_5e_core/data/loader.py`
- [ ] **request_weapon()** → `dnd_5e_core/data/loader.py`
- [ ] **request_armor()** → `dnd_5e_core/data/loader.py`
- [ ] **request_spell()** → `dnd_5e_core/data/loader.py`
- [ ] Toutes les autres fonctions request_*

---

## 📊 Phase 6 : Mise à Jour des Imports

### Fichiers à Modifier (15+)

#### Jeux
- [ ] `main.py`
- [ ] `main_ncurses.py`
- [ ] `dungeon_pygame.py`
- [ ] `dungeon_menu_pygame.py`
- [ ] `boltac_tp_pygame.py`
- [ ] `pyQTApp/wizardry.py`
- [ ] `pyQTApp/common.py`
- [ ] `pyQTApp/Castle/Boltac_module.py`
- [ ] `pyQTApp/Castle/Cant_module.py`
- [ ] `pyQTApp/Castle/Inn_module.py`
- [ ] `pyQTApp/EdgeOfTown/Combat_module.py`

#### Support
- [ ] `populate_functions.py`
- [ ] `populate_rpg_functions.py`

---

## 📊 Phase 7 : Tests et Validation

- [ ] Tests unitaires pour Sprite
- [ ] Tests unitaires pour Monster
- [ ] Tests unitaires pour Character
- [ ] Tests unitaires pour Weapon/Armor
- [ ] Tests unitaires pour Combat system
- [ ] Tests unitaires pour Spell system
- [ ] Tests d'intégration main.py
- [ ] Tests d'intégration main_ncurses.py
- [ ] Tests d'intégration dungeon_pygame.py
- [ ] Tests d'intégration pyQTApp/wizardry.py

---

## 🎯 Statut Actuel

**Date** : 23 décembre 2024, 17:30

### ✅ Fait
1. Structure dnd-5e-core créée ✅
2. Sprite extrait et nettoyé ✅

### 🔄 En Cours
3. Création du plan de migration (ce document)

### 📋 À Faire
4. Extraire les classes de base (Equipment, DamageDice, Abilities)
5. Extraire Monster
6. Extraire Character
7. Extraire les autres classes
8. Mettre à jour les imports
9. Tester

---

## 📝 Notes

### Classes Prioritaires (Les Plus Utilisées)

D'après DEPENDENCY_MAP.md :

1. **Character** - 8+ utilisations
2. **Weapon** - 6+ utilisations
3. **Armor** - 6+ utilisations
4. **Monster** - 5+ utilisations
5. **Equipment** - 4+ utilisations
6. **HealingPotion** - 4+ utilisations

### Stratégie

1. ✅ Commencer par Sprite (classe de base)
2. Extraire Equipment, Weapon, Armor, Potion (très utilisés, relativement simples)
3. Extraire DamageDice, Abilities (dépendances de Monster/Character)
4. Extraire Monster (complexe mais essentiel)
5. Extraire Character (le plus complexe)
6. Extraire le reste (Races, Classes, Spells, Combat)
7. Extraire populate_functions.py
8. Mettre à jour tous les imports
9. Tester chaque jeu

---

## 🚧 Problèmes Potentiels

### Dépendances Circulaires

- Monster importe Character (pour attack)
- Character importe Monster (pour kills list)
- Solution : Utiliser `from __future__ import annotations` et quotes pour les types

### Code UI Mélangé

- cprint() partout
- color.RED, color.END
- pygame.mixer.Sound
- Solution : Supprimer ou commenter, retourner seulement des données

### Imports Relatifs

- from tools.common import cprint
- Solution : Supprimer les imports UI, garder seulement les imports data

---

## ⏱️ Estimation de Temps Révisée

| Phase | Estimation Initiale | Temps Réel | Statut |
|-------|---------------------|------------|--------|
| Phase 1 : Classes de base | 3-4h | ? | 🔄 |
| Phase 2 : Classes support | 2h | ? | ⏸️ |
| Phase 3 : Combat system | 2h | ? | ⏸️ |
| Phase 4 : Spell system | 2h | ? | ⏸️ |
| Phase 5 : Data loaders | 2h | ? | ⏸️ |
| Phase 6 : Mise à jour imports | 2-3h | ? | ⏸️ |
| Phase 7 : Tests | 2-3h | ? | ⏸️ |
| **TOTAL** | **15-17h** | **?** | 🔄 |

---

## 📞 Prochaine Action

✅ Continuer l'extraction des classes dans cet ordre :

1. Equipment (base class)
2. DamageDice
3. Weapon
4. Armor
5. Potion (Healing, Speed, Strength)
6. Abilities
7. Monster
8. Character

Chaque classe sera nettoyée (suppression code UI) et documentée.

