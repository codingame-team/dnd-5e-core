#!/usr/bin/env python3
"""
Test de la migration des collections
Vérifie que le module collections.py fonctionne correctement
"""

import sys
from pathlib import Path

# Ajouter le répertoire parent au path pour l'import
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test que tous les imports fonctionnent"""
    print("🧪 Test 1: Imports...")
    try:
        from dnd_5e_core.data import (
            populate,
            load_collection,
            get_collection_count,
            get_collection_item,
            list_all_collections,
            get_monsters_list,
            get_spells_list,
        )
        print("✅ Tous les imports réussis")
        return True
    except Exception as e:
        print(f"❌ Erreur d'import: {e}")
        return False


def test_list_collections():
    """Test de listage des collections"""
    print("\n🧪 Test 2: Lister les collections...")
    try:
        from dnd_5e_core.data import list_all_collections
        collections = list_all_collections()
        print(f"✅ {len(collections)} collections trouvées")
        print(f"   Exemples: {collections[:5]}")
        return len(collections) > 0
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_populate_function():
    """Test de la fonction populate (compatibilité)"""
    print("\n🧪 Test 3: Fonction populate()...")
    try:
        from dnd_5e_core.data import populate

        # Test sans URL
        monsters = populate('monsters', 'results')
        print(f"✅ {len(monsters)} monstres chargés (sans URL)")

        # Test avec URL
        monsters_urls = populate('monsters', 'results', with_url=True)
        print(f"✅ {len(monsters_urls)} monstres chargés (avec URL)")
        print(f"   Exemple: {monsters_urls[0]}")

        return len(monsters) > 0 and len(monsters_urls) > 0
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_convenience_functions():
    """Test des fonctions de convenance"""
    print("\n🧪 Test 4: Fonctions de convenance...")
    try:
        from dnd_5e_core.data import (
            get_monsters_list,
            get_spells_list,
            get_classes_list,
            get_races_list,
        )

        monsters = get_monsters_list()
        spells = get_spells_list()
        classes = get_classes_list()
        races = get_races_list()

        print(f"✅ Monstres: {len(monsters)}")
        print(f"✅ Sorts: {len(spells)}")
        print(f"✅ Classes: {len(classes)}")
        print(f"✅ Races: {len(races)}")

        return all([monsters, spells, classes, races])
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_collection_count():
    """Test du comptage d'items"""
    print("\n🧪 Test 5: Comptage d'items...")
    try:
        from dnd_5e_core.data import get_collection_count

        monster_count = get_collection_count('monsters')
        spell_count = get_collection_count('spells')

        print(f"✅ Monstres: {monster_count} items")
        print(f"✅ Sorts: {spell_count} items")

        return monster_count > 0 and spell_count > 0
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_get_item():
    """Test de récupération d'un item spécifique"""
    print("\n🧪 Test 6: Récupération d'item spécifique...")
    try:
        from dnd_5e_core.data import get_collection_item

        goblin = get_collection_item('monsters', 'goblin')
        fireball = get_collection_item('spells', 'fireball')

        print(f"✅ Goblin: {goblin}")
        print(f"✅ Fireball: {fireball}")

        return goblin is not None and fireball is not None
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_load_full_collection():
    """Test de chargement d'une collection complète"""
    print("\n🧪 Test 7: Chargement collection complète...")
    try:
        from dnd_5e_core.data import load_collection

        monsters_data = load_collection('monsters')

        print(f"✅ Collection chargée")
        print(f"   Count: {monsters_data.get('count', 'N/A')}")
        print(f"   Results: {len(monsters_data.get('results', []))} items")

        return 'count' in monsters_data and 'results' in monsters_data
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def main():
    """Lance tous les tests"""
    print("=" * 60)
    print("🧪 TEST DE LA MIGRATION DES COLLECTIONS")
    print("=" * 60)

    tests = [
        test_imports,
        test_list_collections,
        test_populate_function,
        test_convenience_functions,
        test_collection_count,
        test_get_item,
        test_load_full_collection,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test échoué avec exception: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)

    print("\n" + "=" * 60)
    print("📊 RÉSULTATS")
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    print(f"✅ Tests réussis: {passed}/{total}")

    if passed == total:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS !")
        print("✅ La migration des collections est RÉUSSIE")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) échoué(s)")
        print("❌ Certains tests ont échoué")
        return 1


if __name__ == "__main__":
    exit(main())

