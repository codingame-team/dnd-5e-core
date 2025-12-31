#!/usr/bin/env python3
"""
Script utilitaire pour télécharger les tokens de tous les monstres implémentés de 5e.tools

Usage:
    python download_all_tokens.py [--output FOLDER]

Options:
    --output FOLDER    Dossier de destination pour les tokens (défaut: ./tokens)
    --help            Afficher cette aide
"""
import sys
import argparse
from pathlib import Path

# Ajouter le répertoire parent au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

from dnd_5e_core.entities import get_extended_monster_loader
from dnd_5e_core.utils import download_tokens_batch


def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description="Télécharge les tokens de tous les monstres implémentés de 5e.tools"
    )
    parser.add_argument(
        '--output', '-o',
        default='./tokens',
        help='Dossier de destination pour les tokens (défaut: ./tokens)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Afficher les monstres qui seraient téléchargés sans les télécharger'
    )

    args = parser.parse_args()

    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "TÉLÉCHARGEMENT DES TOKENS 5E.TOOLS" + " " * 19 + "║")
    print("╚" + "═" * 68 + "╝")
    print()

    # Charger les monstres
    print("[1] Chargement de la liste des monstres...")
    loader = get_extended_monster_loader()
    monsters = loader.load_implemented_monsters()

    print(f"    ✓ {len(monsters)} monstres trouvés")
    print()

    # Créer la liste des tuples (nom, source)
    monster_list = []
    for monster in monsters:
        name = monster.get('name')
        source = monster.get('source', 'MM')
        if name:
            monster_list.append((name, source))

    print(f"[2] Préparation du téléchargement de {len(monster_list)} tokens...")
    print(f"    Destination: {args.output}")
    print()

    if args.dry_run:
        print("[DRY RUN] Monstres qui seraient téléchargés:")
        print("-" * 70)
        for i, (name, source) in enumerate(monster_list, 1):
            print(f"  {i:3d}. {name:40s} [{source}]")
        print("-" * 70)
        print(f"\nTotal: {len(monster_list)} tokens")
        print("\nPour télécharger réellement, relancer sans --dry-run")
        return

    # Télécharger les tokens
    print("[3] Téléchargement en cours...")
    print("-" * 70)

    results = download_tokens_batch(monster_list, save_folder=args.output)

    print("-" * 70)
    print()

    # Afficher les échecs
    failed = [(name, code) for name, code in results.items() if code != 200]
    if failed:
        print("[4] Échecs de téléchargement:")
        for name, code in failed:
            print(f"    ✗ {name} (HTTP {code})")
        print()

    print("✓ Téléchargement terminé!")
    print(f"  Tokens sauvegardés dans: {args.output}")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Téléchargement interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

