"""
defis.py - Gestionnaire de défis 2D pour le solveur (IQ Puzzler Pro)
Classe Defi compacte et épurée pour alimenter directement le solveur :
- Initialise le Plateau (Rectangle ou Losange) avec les pièces fixes déjà posées
- Isole les pièces libres restantes à placer
- Fournit la solution officielle et les données prêtes à être extraites
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any

from pieces import PIECES
from plateau import Plateau
from PlateauLosange import PlateauLosange

# Si Plateau n'avait pas encore get_ilots_vides, on lui partage celle définie dans PlateauLosange
if not hasattr(Plateau, "get_ilots_vides"):
    Plateau.get_ilots_vides = PlateauLosange.get_ilots_vides

FICHIER_DEFIS = Path(__file__).parent / "defis.json"


class Defi:
    """
    Modélise un défi du jeu et prépare le problème pour le solveur.

    Attributs accessibles par le solveur :
    - id : int (numéro du défi)
    - id_defi : int (alias normalisé pour le solveur)
    - difficulte : str ("Starter", "Junior", "Expert", "Master", "Wizard")
    - mode : str ("rectangle" ou "losange")
    - plateau : Plateau | PlateauLosange (avec les pièces fixes posées et verrouillées)
    - pieces_fixes : list[dict] (pièces initiales imposées avec id, x, y, forme)
    - pieces_libres : list[str] (liste des pièces restant à placer, ex: ['C', 'F', 'L'])
    - solution : list[str] (grille de la solution officielle du livret)
    """

    def __init__(self, id_defi: int | str, fichier_json: str | Path = FICHIER_DEFIS):
        self.id = int(id_defi)
        self.id_defi = self.id

        # 1. Chargement des données depuis defis.json
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

        # 2. Instanciation directe du bon plateau selon le mode
        self.plateau = PlateauLosange() if self.mode == "losange" else Plateau()
        ids_fixes = set()

        for p in self.pieces_fixes:
            pid = p["id"]
            x0, y0 = p["x"], p["y"]
            forme = [tuple(coord) for coord in p["forme"]]
            self.plateau.poser_piece(pid, forme, x0, y0, verrouillee=True)
            ids_fixes.add(pid)

        # 3. Détermination des pièces libres restantes
        self.pieces_libres = sorted(set(PIECES.keys()) - ids_fixes)
        self.pieces_a_placer = {pid: PIECES[pid]["coords"] for pid in self.pieces_libres}

    def get_donnees_solver(self) -> dict[str, Any]:
        """Retourne un dictionnaire clé en main contenant tout ce dont le solveur a besoin."""
        return {
            "id": self.id,
            "mode": self.mode,
            "difficulte": self.difficulte,
            "plateau": self.plateau,
            "pieces_libres": self.pieces_libres,
            "pieces_fixes": self.pieces_fixes,
            "solution": self.solution,
            "premiere_case_vide": self.plateau.premiere_case_vide(),
        }

    def __repr__(self) -> str:
        return (
            f"Defi(id={self.id}, mode='{self.mode}', difficulte='{self.difficulte}', "
            f"fixes={len(self.pieces_fixes)}, libres={len(self.pieces_libres)})"
        )


if __name__ == "__main__":
    d1 = Defi(1)
    print("Défi #1 (Rectangle) :", d1)
    print("Pièces libres #1    :", d1.pieces_libres)

    d65 = Defi(65)
    print("Défi #65 (Losange)  :", d65)
    print("Type plateau #65    :", type(d65.plateau).__name__)
    print("Pièces libres #65   :", d65.pieces_libres)
