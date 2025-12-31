"""
Module pour télécharger les tokens d'images de monstres depuis 5e.tools
"""
import os
from typing import List, Optional
from urllib.parse import quote

import requests


def download_image(url: str, save_folder: str, monster_name: str, filename: Optional[str] = None) -> int:
    """
    Télécharge une image depuis une URL et la sauvegarde dans le dossier spécifié.

    :param url: URL de l'image
    :param save_folder: Dossier de destination
    :param monster_name: Nom du monstre (pour les messages de log)
    :param filename: Nom de fichier optionnel (sinon extrait de l'URL)
    :return: Code de statut HTTP
    """
    # S'assurer que le dossier de destination existe
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Extraire le nom de fichier de l'URL si non fourni
    if not filename:
        filename = os.path.basename(url)

    # Définir le chemin complet de sauvegarde
    save_path = os.path.join(save_folder, filename)

    # Envoyer une requête HTTP à l'URL
    try:
        response = requests.get(url, timeout=10)

        # Vérifier si la requête a réussi
        if response.status_code == 200:
            # Écrire le contenu dans un fichier
            with open(save_path, 'wb') as file:
                file.write(response.content)
            # print(f"Image téléchargée avec succès: {save_path}")
        else:
            print(f"{monster_name} -> Échec du téléchargement. Code HTTP: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"{monster_name} -> Erreur de requête: {e}")
        return 0

    return response.status_code


def download_monster_token(monster_name: str, source: str = "MM", save_folder: str = "tokens") -> int:
    """
    Télécharge le token d'un monstre depuis 5e.tools

    :param monster_name: Nom du monstre
    :param source: Source du monstre (MM par défaut)
    :param save_folder: Dossier de destination
    :return: Code de statut HTTP
    """
    # Construire l'URL pour le token du monstre
    image_url = f"https://5e.tools/img/bestiary/tokens/{source}/{quote(monster_name, safe='')}.webp"
    filename = f"{monster_name.replace('/', '_')}.webp"

    return download_image(image_url, save_folder, monster_name, filename)


def download_tokens_batch(monster_list: List[tuple[str, str]], save_folder: str = "tokens") -> dict:
    """
    Télécharge les tokens pour une liste de monstres

    :param monster_list: Liste de tuples (nom_monstre, source)
    :param save_folder: Dossier de destination
    :return: Dictionnaire avec les résultats {nom: status_code}
    """
    results = {}

    for monster_name, source in monster_list:
        status = download_monster_token(monster_name, source, save_folder)
        results[monster_name] = status

    # Résumé
    successful = sum(1 for status in results.values() if status == 200)
    failed = len(results) - successful

    print(f"\nRésumé du téléchargement:")
    print(f"  Réussis: {successful}")
    print(f"  Échoués: {failed}")

    return results


if __name__ == "__main__":
    # Exemple d'utilisation
    test_monsters = [
        ("Cult Fanatic", "MM"),
        ("Orc Eye of Gruumsh", "MM"),
        ("Goblin Boss", "MM"),
    ]

    download_tokens_batch(test_monsters, "../../../images/monsters/tokens")

