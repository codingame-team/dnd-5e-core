#!/usr/bin/env python3
"""
Test de validation de la migration du dossier data
Vérifie que toutes les données sont accessibles depuis dnd-5e-core
"""

import sys
from pathlib import Path

# Add dnd-5e-core to path
sys.path.insert(0, str(Path(__file__).parent))

def test_data_migration():
    """Test complet de la migration des données"""

    print("="*70)
    print("🎮 DND-5E-CORE - VALIDATION DE LA MIGRATION DES DONNÉES")
    print("="*70)
    print()

    # Test 1: Auto-détection du répertoire
    print("📍 Test 1: Auto-détection du répertoire data")
    try:
        from dnd_5e_core.data import get_data_directory
        data_dir = get_data_directory()
        print(f"   ✅ Répertoire trouvé: {data_dir}")
        print(f"   ✅ Existe: {data_dir.exists()}")
        assert data_dir.exists(), "Le répertoire data n'existe pas"
        assert "dnd-5e-core" in str(data_dir), "Le répertoire n'est pas dans dnd-5e-core"
    except Exception as e:
        print(f"   ❌ ERREUR: {e}")
        return False
    print()

    # Test 2: Chargement des listes
    print("📋 Test 2: Chargement des listes de données")
    try:
        from dnd_5e_core.data import (
            list_monsters, list_spells, list_weapons, list_armors,
            list_equipment, list_races, list_classes
        )

        counts = {
            'Monsters': len(list_monsters()),
            'Spells': len(list_spells()),
            'Weapons': len(list_weapons()),
            'Armors': len(list_armors()),
            'Equipment': len(list_equipment()),
            'Races': len(list_races()),
            'Classes': len(list_classes()),
        }

        for category, count in counts.items():
            status = "✅" if count > 0 else "❌"
            print(f"   {status} {category}: {count}")
            assert count > 0, f"Aucun {category} trouvé"

    except Exception as e:
        print(f"   ❌ ERREUR: {e}")
        return False
    print()

    # Test 3: Chargement d'objets spécifiques
    print("🔍 Test 3: Chargement d'objets spécifiques")
    try:
        from dnd_5e_core.data import load_monster, load_spell, load_weapon, load_armor, load_race, load_class

        tests = [
            ('Monster', load_monster('goblin'), 'Goblin'),
            ('Spell', load_spell('fireball'), 'Fireball'),
            ('Weapon', load_weapon('longsword'), 'Longsword'),
            ('Armor', load_armor('plate-armor'), 'Plate Armor'),
            ('Race', load_race('elf'), 'Elf'),
            ('Class', load_class('fighter'), 'Fighter'),
        ]

        for category, data, expected_name in tests:
            if data and data.get('name') == expected_name:
                print(f"   ✅ {category}: {data['name']} chargé avec succès")
            else:
                print(f"   ❌ {category}: Échec du chargement")
                return False

    except Exception as e:
        print(f"   ❌ ERREUR: {e}")
        return False
    print()

    # Test 4: Vérification des données détaillées
    print("🔬 Test 4: Vérification des données détaillées")
    try:
        goblin = load_monster('goblin')

        required_fields = ['name', 'hit_points', 'armor_class', 'challenge_rating', 'xp']
        for field in required_fields:
            if field in goblin:
                print(f"   ✅ {field}: {goblin[field]}")
            else:
                print(f"   ❌ Champ manquant: {field}")
                return False

    except Exception as e:
        print(f"   ❌ ERREUR: {e}")
        return False
    print()

    # Test 5: Test de compatibilité (pas de set_data_directory requis)
    print("🔄 Test 5: Compatibilité (pas de configuration requise)")
    try:
        # Réinitialiser et retester
        from dnd_5e_core.data import loader
        loader._DATA_DIR = None  # Reset

        # Devrait toujours fonctionner
        test_dir = get_data_directory()
        print(f"   ✅ Auto-détection fonctionne après reset: {test_dir}")

    except Exception as e:
        print(f"   ❌ ERREUR: {e}")
        return False
    print()

    # Résultat final
    print("="*70)
    print("🎉 TOUS LES TESTS RÉUSSIS - MIGRATION VALIDÉE !")
    print("="*70)
    print()
    print("📊 Résumé:")
    print(f"   • Répertoire data: {data_dir}")
    print(f"   • Monstres: {counts['Monsters']}")
    print(f"   • Sorts: {counts['Spells']}")
    print(f"   • Armes: {counts['Weapons']}")
    print(f"   • Armures: {counts['Armors']}")
    print(f"   • Équipements: {counts['Equipment']}")
    print(f"   • Races: {counts['Races']}")
    print(f"   • Classes: {counts['Classes']}")
    print()
    print("✅ Le package dnd-5e-core est PRÊT à être utilisé !")
    print()

    return True


if __name__ == "__main__":
    success = test_data_migration()
    sys.exit(0 if success else 1)

