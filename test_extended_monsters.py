"""
Script de test pour les fonctionnalités des monstres étendus de 5e.tools
"""
import sys
from pathlib import Path

# Ajouter le répertoire parent au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

from dnd_5e_core.entities.extended_monsters import get_loader
from dnd_5e_core.entities.special_monster_actions import get_builder


def test_monster_loader():
    """Test du chargement des monstres"""
    print("=" * 70)
    print("TEST: Chargement des monstres de 5e.tools")
    print("=" * 70)

    loader = get_loader()

    # Test 1: Statistiques générales
    print("\n[1] Statistiques des monstres implémentés")
    stats = loader.get_stats()
    print(f"   Total de monstres: {stats['total']}")
    print(f"   Sources représentées: {len(stats['by_source'])}")
    print(f"   Types de créatures: {len(stats['by_type'])}")

    # Test 2: Récupération d'un monstre spécifique
    print("\n[2] Récupération d'un monstre: Orc Eye of Gruumsh")
    monster = loader.get_monster_by_name("Orc Eye of Gruumsh")
    if monster:
        print(f"   ✓ Monstre trouvé")
        print(f"     - Nom: {monster['name']}")
        print(f"     - Source: {monster['source']}")
        print(f"     - CR: {monster.get('cr', '?')}")
        print(f"     - AC: {monster.get('ac', '?')}")
        print(f"     - HP moyen: {monster.get('hp', {}).get('average', '?')}")
    else:
        print("   ✗ Monstre non trouvé")

    # Test 3: Recherche de monstres
    print("\n[3] Recherche de monstres contenant 'goblin'")
    goblins = loader.search_monsters(name_contains="goblin")
    print(f"   Trouvé {len(goblins)} monstre(s)")
    for goblin in goblins[:5]:
        print(f"     - {goblin['name']} (CR {goblin.get('cr', '?')})")

    # Test 4: Filtrage par CR
    print("\n[4] Monstres de CR 2")
    cr2_monsters = loader.get_monsters_by_cr(2.0)
    print(f"   Trouvé {len(cr2_monsters)} monstre(s)")
    for monster in cr2_monsters[:5]:
        print(f"     - {monster['name']}")

    # Test 5: Filtrage par source
    print("\n[5] Monstres de la source MM (Monster Manual)")
    mm_monsters = loader.get_monsters_by_source("MM")
    print(f"   Trouvé {len(mm_monsters)} monstre(s)")

    print("\n✓ Test du loader terminé avec succès")


def test_special_actions_builder():
    """Test du builder d'actions spéciales"""
    print("\n" + "=" * 70)
    print("TEST: Builder d'actions spéciales")
    print("=" * 70)

    builder = get_builder()

    # Test 1: Liste des monstres implémentés
    print("\n[1] Monstres avec actions implémentées")
    implemented = builder.get_implemented_monsters()
    print(f"   Total: {len(implemented)} monstres")
    print(f"   Premiers monstres:")
    for monster in sorted(implemented)[:10]:
        print(f"     - {monster}")

    # Test 2: Vérification d'implémentation
    print("\n[2] Vérification d'implémentation")
    test_monsters = [
        "Orc Eye of Gruumsh",
        "Goblin Boss",
        "Ancient Red Dragon",  # Non implémenté
    ]
    for monster_name in test_monsters:
        is_impl = builder.is_implemented(monster_name)
        status = "✓ Implémenté" if is_impl else "✗ Non implémenté"
        print(f"   {status}: {monster_name}")

    print("\n✓ Test du builder terminé avec succès")


def test_integration():
    """Test d'intégration: combiner loader et builder"""
    print("\n" + "=" * 70)
    print("TEST: Intégration loader + builder")
    print("=" * 70)

    loader = get_loader()
    builder = get_builder()

    # Charger les monstres implémentés
    print("\n[1] Vérification de la cohérence entre loader et builder")
    implemented_actions = set(builder.get_implemented_monsters())

    # Vérifier que tous les monstres avec actions sont dans le JSON
    monsters_in_json = set(loader.get_monster_names())

    # Trouver les monstres avec actions mais pas dans le JSON
    missing_in_json = implemented_actions - monsters_in_json
    if missing_in_json:
        print(f"   ⚠ Monstres avec actions mais absents du JSON:")
        for monster in sorted(missing_in_json):
            print(f"     - {monster}")
    else:
        print(f"   ✓ Tous les monstres avec actions sont dans le JSON")

    # Trouver les monstres dans le JSON mais sans actions
    missing_actions = monsters_in_json - implemented_actions
    if missing_actions:
        print(f"\n   ℹ Monstres dans le JSON sans actions implémentées: {len(missing_actions)}")
        print(f"     Exemples:")
        for monster in sorted(missing_actions)[:5]:
            print(f"       - {monster}")

    print("\n✓ Test d'intégration terminé")


def main():
    """Fonction principale"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "TESTS DES MONSTRES ÉTENDUS 5E.TOOLS" + " " * 17 + "║")
    print("╚" + "═" * 68 + "╝")

    try:
        test_monster_loader()
        test_special_actions_builder()
        test_integration()

        print("\n" + "=" * 70)
        print("RÉSUMÉ: Tous les tests ont réussi ✓")
        print("=" * 70)
        print()

    except Exception as e:
        print(f"\n✗ ERREUR lors des tests: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

