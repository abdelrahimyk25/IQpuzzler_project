"""
defis.py - Gestionnaire de défis 2D pour le solveur (IQ Puzzler Pro)
Classe Defi compacte et épurée pour alimenter directement le solveur :
- Initialise le Plateau depuis main.py avec les pièces fixes déjà posées
- Isole les pièces libres restantes à placer
- Fournit la solution officielle et les données prêtes à être extraites
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from main import Plateau, PIECES

FICHIER_DEFIS = Path(__file__).parent / "defis.json"


class Defi:
    """
    Modélise un défi du jeu et prépare le problème pour le solveur.

    Attributs accessibles par le solveur :
    - id : int (numéro du défi)
    - difficulte : str ("Starter", "Junior", etc.)
    - mode : str ("rectangle", etc.)
    - plateau : Plateau (instance de main.py avec les pièces fixes déjà posées)
    - pieces_fixes : list[dict] (pièces initiales imposées avec id, x, y, forme)
    - pieces_libres : list[str] (liste des identifiants des pièces restant à placer, ex: ['C', 'F', 'L'])
    - pieces_a_placer : dict[str, list[tuple[int, int]]] (formes de base des pièces libres depuis PIECES)
    - solution : list[str] (grille de la solution officielle du défi)
    """

    def __init__(self, id_defi: int | str, fichier_json: str | Path = FICHIER_DEFIS):
        self.id = int(id_defi)

        # 1. Chargement des données du défi json 
        with open(fichier_json, "r", encoding="utf-8") as f:
            tous_defis = json.load(f)

        cle = str(id_defi)
        if cle not in tous_defis:
            raise ValueError(f"Défi #{id_defi} non trouvé dans {fichier_json}")

        donnees = tous_defis[cle]
        self.mode = donnees.get("mode", "rectangle")
        self.difficulte = donnees.get("difficulte", "Inconnue")
        self.pieces_fixes = donnees.get("pieces_initiales", [])
        self.solution = donnees.get("solution_grille", [])

        # 2. Initialisation du plateau avec pose des pièces fixes de départ
        self.plateau = Plateau()
        ids_fixes = set()

        for p in self.pieces_fixes:
            pid = p["id"]
            x0, y0 = p["x"], p["y"]
            forme = [tuple(coord) for coord in p["forme"]]
            self.plateau.poser_piece(pid, forme, x0, y0, True)
            ids_fixes.add(pid)

        # 3. Détermination des pièces libres restantes à placer par le solveur
        self.pieces_libres = sorted(set(PIECES.keys()) - ids_fixes)
        self.pieces_a_placer = {pid: PIECES[pid]["coords"] for pid in self.pieces_libres}

    def get_donnees(self) -> dict[str, Any]:
        """Retourne un dictionnaire clé en main contenant tout ce dont le solveur a besoin."""
        return {
            "id": self.id,
            "plateau": self.plateau,
            "pieces_libres": self.pieces_libres,
            "pieces_a_placer": self.pieces_a_placer,
            "pieces_fixes": self.pieces_fixes,
            "solution": self.solution,
            "premiere_case_vide": self.plateau.premiere_case_vide(),
        }

    def __repr__(self) -> str:
        return (
            f"Defi(id={self.id}, difficulte='{self.difficulte}', "
            f"fixes={len(self.pieces_fixes)}, libres={len(self.pieces_libres)})"
        )


if __name__ == "__main__":
    # Test d'extraction des données pour le défi 1
    defi = Defi(1)
    print("=" * 45)
    print(f"Extraction du {defi}")
    print("Pièces libres restantes à placer :", defi.pieces_libres)
    print("Première case vide :", defi.plateau.premiere_case_vide())
    print("\nPlateau avec pièces fixes posées :")
    defi.plateau.afficher()
    print("Solution attendue :")
    for ligne in defi.solution:
        print(" ", ligne)
    print("=" * 45)
from defis import Defi

defi = Defi(1)
print("Pièces libres :", defi.pieces_libres)
defi.plateau.afficher()
exit()