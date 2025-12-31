"""
Module pour gérer les monstres étendus de 5e.tools

Ce module gère les monstres qui ne sont pas inclus dans l'API officielle D&D 5e,
mais qui sont disponibles sur le site 5e.tools.
Les données proviennent de fichiers JSON avec une structure légèrement différente.
"""
import json
import os
from typing import List, Dict, Optional, Any
from pathlib import Path


class FiveEToolsMonsterLoader:
    """
    Loader pour les monstres du site 5e.tools

    Charge les monstres depuis les fichiers JSON bestiary-sublist-data.json
    """

    def __init__(self, data_folder: Optional[str] = None):
        """
        Initialise le loader

        :param data_folder: Chemin vers le dossier contenant les fichiers JSON
        """
        if data_folder is None:
            # Par défaut, utiliser le dossier data/monsters du package
            module_path = Path(__file__).parent.parent
            data_folder = module_path / "data" / "monsters"

        self.data_folder = Path(data_folder)
        self._monsters_cache: Optional[List[Dict[str, Any]]] = None
        self._all_monsters_cache: Optional[List[Dict[str, Any]]] = None

    def load_implemented_monsters(self) -> List[Dict[str, Any]]:
        """
        Charge la liste des monstres implémentés

        :return: Liste des monstres
        """
        if self._monsters_cache is not None:
            return self._monsters_cache

        file_path = self.data_folder / "bestiary-sublist-data.json"

        if not file_path.exists():
            raise FileNotFoundError(f"Fichier non trouvé: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            self._monsters_cache = json.load(f)

        return self._monsters_cache

    def load_all_monsters(self) -> List[Dict[str, Any]]:
        """
        Charge la liste de tous les monstres disponibles

        :return: Liste de tous les monstres
        """
        if self._all_monsters_cache is not None:
            return self._all_monsters_cache

        file_path = self.data_folder / "bestiary-sublist-data-all-monsters.json"

        if not file_path.exists():
            raise FileNotFoundError(f"Fichier non trouvé: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            self._all_monsters_cache = json.load(f)

        return self._all_monsters_cache

    def get_monster_by_name(self, name: str, use_all: bool = False) -> Optional[Dict[str, Any]]:
        """
        Récupère un monstre par son nom

        :param name: Nom du monstre
        :param use_all: Si True, cherche dans tous les monstres, sinon seulement les implémentés
        :return: Données du monstre ou None si non trouvé
        """
        monsters = self.load_all_monsters() if use_all else self.load_implemented_monsters()

        for monster in monsters:
            if monster.get("name") == name:
                return monster

        return None

    def get_monsters_by_source(self, source: str, use_all: bool = False) -> List[Dict[str, Any]]:
        """
        Récupère tous les monstres d'une source donnée

        :param source: Code de la source (ex: "MM", "VGTM", "MPMM")
        :param use_all: Si True, cherche dans tous les monstres, sinon seulement les implémentés
        :return: Liste des monstres de cette source
        """
        monsters = self.load_all_monsters() if use_all else self.load_implemented_monsters()

        return [
            monster for monster in monsters
            if monster.get("source") == source
        ]

    def get_monsters_by_cr(self, cr: float, use_all: bool = False) -> List[Dict[str, Any]]:
        """
        Récupère tous les monstres d'un CR donné

        :param cr: Challenge Rating
        :param use_all: Si True, cherche dans tous les monstres, sinon seulement les implémentés
        :return: Liste des monstres de ce CR
        """
        monsters = self.load_all_monsters() if use_all else self.load_implemented_monsters()

        result = []
        for monster in monsters:
            monster_cr = monster.get("cr")
            if monster_cr is not None:
                # Le CR peut être un nombre, une fraction (ex: "1/8"), ou un dictionnaire
                try:
                    if isinstance(monster_cr, dict):
                        # Parfois le CR est un dict avec une clé 'cr'
                        monster_cr = monster_cr.get('cr', monster_cr)

                    if isinstance(monster_cr, str) and "/" in monster_cr:
                        num, den = monster_cr.split("/")
                        monster_cr_value = float(num) / float(den)
                    else:
                        monster_cr_value = float(monster_cr)

                    if monster_cr_value == cr:
                        result.append(monster)
                except (ValueError, TypeError):
                    # Ignorer les CR invalides
                    continue

        return result

    def get_monster_names(self, use_all: bool = False) -> List[str]:
        """
        Récupère la liste de tous les noms de monstres

        :param use_all: Si True, retourne tous les monstres, sinon seulement les implémentés
        :return: Liste des noms de monstres
        """
        monsters = self.load_all_monsters() if use_all else self.load_implemented_monsters()
        return [monster.get("name") for monster in monsters if monster.get("name")]

    def search_monsters(self,
                       name_contains: Optional[str] = None,
                       source: Optional[str] = None,
                       min_cr: Optional[float] = None,
                       max_cr: Optional[float] = None,
                       monster_type: Optional[str] = None,
                       use_all: bool = False) -> List[Dict[str, Any]]:
        """
        Recherche de monstres avec plusieurs critères

        :param name_contains: Nom contient cette chaîne (insensible à la casse)
        :param source: Code de la source
        :param min_cr: CR minimum
        :param max_cr: CR maximum
        :param monster_type: Type de créature (ex: "humanoid", "dragon")
        :param use_all: Si True, cherche dans tous les monstres, sinon seulement les implémentés
        :return: Liste des monstres correspondants
        """
        monsters = self.load_all_monsters() if use_all else self.load_implemented_monsters()

        results = []
        for monster in monsters:
            # Filtre par nom
            if name_contains and name_contains.lower() not in monster.get("name", "").lower():
                continue

            # Filtre par source
            if source and monster.get("source") != source:
                continue

            # Filtre par type
            if monster_type:
                m_type = monster.get("type")
                if isinstance(m_type, dict):
                    m_type = m_type.get("type")
                if m_type != monster_type:
                    continue

            # Filtre par CR
            monster_cr = monster.get("cr")
            if monster_cr is not None:
                try:
                    if isinstance(monster_cr, dict):
                        monster_cr = monster_cr.get('cr', monster_cr)

                    if isinstance(monster_cr, str) and "/" in monster_cr:
                        num, den = monster_cr.split("/")
                        monster_cr_value = float(num) / float(den)
                    else:
                        monster_cr_value = float(monster_cr)

                    if min_cr is not None and monster_cr_value < min_cr:
                        continue
                    if max_cr is not None and monster_cr_value > max_cr:
                        continue
                except (ValueError, TypeError):
                    # Ignorer les CR invalides
                    if min_cr is not None or max_cr is not None:
                        continue

            results.append(monster)

        return results

    def get_stats(self, use_all: bool = False) -> Dict[str, Any]:
        """
        Récupère des statistiques sur les monstres chargés

        :param use_all: Si True, utilise tous les monstres, sinon seulement les implémentés
        :return: Dictionnaire de statistiques
        """
        monsters = self.load_all_monsters() if use_all else self.load_implemented_monsters()

        sources = {}
        types = {}
        crs = {}

        for monster in monsters:
            # Compter par source
            source = monster.get("source", "Unknown")
            sources[source] = sources.get(source, 0) + 1

            # Compter par type
            m_type = monster.get("type")
            if isinstance(m_type, dict):
                m_type = m_type.get("type", "Unknown")
            types[m_type] = types.get(m_type, 0) + 1

            # Compter par CR
            cr = monster.get("cr", "Unknown")
            crs[str(cr)] = crs.get(str(cr), 0) + 1

        return {
            "total": len(monsters),
            "by_source": sources,
            "by_type": types,
            "by_cr": crs
        }


# Instance globale pour un accès facile
_loader_instance: Optional[FiveEToolsMonsterLoader] = None


def get_loader() -> FiveEToolsMonsterLoader:
    """
    Récupère l'instance globale du loader

    :return: Instance du loader
    """
    global _loader_instance
    if _loader_instance is None:
        _loader_instance = FiveEToolsMonsterLoader()
    return _loader_instance


if __name__ == "__main__":
    # Test du module
    loader = FiveEToolsMonsterLoader()

    print("=== Statistiques des monstres implémentés ===")
    stats = loader.get_stats()
    print(f"Total: {stats['total']}")
    print(f"\nPar source:")
    for source, count in sorted(stats['by_source'].items()):
        print(f"  {source}: {count}")

    print("\n=== Recherche de monstres orcs ===")
    orcs = loader.search_monsters(name_contains="orc")
    for orc in orcs[:5]:  # Afficher les 5 premiers
        print(f"  - {orc['name']} (CR {orc.get('cr', '?')})")

    print("\n=== Monstre spécifique: Orc Eye of Gruumsh ===")
    eye_of_gruumsh = loader.get_monster_by_name("Orc Eye of Gruumsh")
    if eye_of_gruumsh:
        print(f"  Nom: {eye_of_gruumsh['name']}")
        print(f"  Source: {eye_of_gruumsh['source']}")
        print(f"  CR: {eye_of_gruumsh.get('cr', '?')}")
        print(f"  AC: {eye_of_gruumsh.get('ac', '?')}")
        print(f"  HP: {eye_of_gruumsh.get('hp', {}).get('average', '?')}")

    print("\n=== Monstre spécifique: Doppelganger ===")
    Doppelganger = loader.get_monster_by_name("Doppelganger")
    if Doppelganger:
        print(f"  Nom: {Doppelganger['name']}")
        print(f"  Source: {Doppelganger['source']}")
        print(f"  CR: {Doppelganger.get('cr', '?')}")
        print(f"  AC: {Doppelganger.get('ac', '?')}")
        print(f"  HP: {Doppelganger.get('hp', {}).get('average', '?')}")

    print("\n=== Recherche de monstres Goblin ===")
    goblins = loader.search_monsters(name_contains="goblin")
    for monster in goblins[:5]:  # Afficher les 5 premiers
        print(f"  Nom: {monster['name']}")
        print(f"  Source: {monster['source']}")
        print(f"  CR: {monster.get('cr', '?')}")
        print(f"  AC: {monster.get('ac', '?')}")
        print(f"  HP: {monster.get('hp', {}).get('average', '?')}")