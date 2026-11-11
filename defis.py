"""


Fournit les fonctions d'interface :
- charger_defi(id_defi) -> dict
- initialiser_plateau_defi(id_defi) -> Plateau
- verifier_integrite_defi(id_defi) -> tuple[bool, str]
- sauvegarder_solution(id_defi, plateau, chemin_fichier) -> None
- verifier_solution(plateau, id_defi) -> bool
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# Import de la classe Plateau
try:
    from plateau import Plateau
except ImportError:
    from main import Plateau

FICHIER_DEFIS = Path(__file__).parent / "defis.json"


def charger_tous_les_defis() -> dict[str, Any]:
    """Charge l'intégralité du fichier defis.json."""
    if not FICHIER_DEFIS.is_file():
        raise FileNotFoundError(f"Fichier de défis introuvable : {FICHIER_DEFIS}")
    with open(FICHIER_DEFIS, "r", encoding="utf-8") as f:
        return json.load(f)


def charger_defi(id_defi: int | str) -> dict[str, Any]:
    """
    Signature officielle du contrat d'interface.
    Retourne le dictionnaire correspondant au défi (mode, difficulte, pieces_initiales, solution_grille).
    """
    defis = charger_tous_les_defis()
    cle = str(id_defi)
    if cle not in defis:
        raise ValueError(f"Défi #{id_defi} non trouvé dans {FICHIER_DEFIS}")
    return defis[cle]


def verifier_integrite_defi(id_defi: int | str) -> tuple[bool, str]:
    """
    Vérifie qu'un défi n'a pas d'incohérence dès le départ :
    - Pas de superposition entre pièces imposées
    - Respect des limites du plateau selon le mode (rectangle: 11x5, losange: 9x9, pyramide: z=0..4)
    - Pièces connues et non vides
    Retourne (True, "OK") ou (False, message_erreur).
    """
    defi = charger_defi(id_defi)
    mode = defi.get("mode", "rectangle")
    pieces_init = defi.get("pieces_initiales", [])

    if mode in ("rectangle", "losange"):
        max_x = 11 if mode == "rectangle" else 9
        max_y = 5 if mode == "rectangle" else 9
        cases_occupees: dict[tuple[int, int], str] = {}

        for p in pieces_init:
            pid = p.get("id", "?")
            x0 = p.get("x", 0)
            y0 = p.get("y", 0)
            forme = p.get("forme", [])

            if not forme:
                return False, f"Défi #{id_defi} : la pièce {pid} n'a aucune coordonnée dans 'forme'."

            for dx, dy in forme:
                cx, cy = x0 + dx, y0 + dy
                # Dépassement de grille
                if not (0 <= cx < max_x and 0 <= cy < max_y):
                    return False, f"Défi #{id_defi} : la pièce {pid} déborde de la grille en ({cx}, {cy})."
                # Superposition
                if (cx, cy) in cases_occupees:
                    autre = cases_occupees[(cx, cy)]
                    return (
                        False,
                        f"Défi #{id_defi} : superposition en ({cx}, {cy}) entre {autre} et {pid}.",
                    )
                cases_occupees[(cx, cy)] = pid

        return True, f"Intégrité OK ({len(pieces_init)} pièces initiales, {len(cases_occupees)} billes placées)."

    elif mode == "pyramide":
        cases_3d: dict[tuple[int, int, int], str] = {}
        for p in pieces_init:
            pid = p.get("id", "?")
            positions = p.get("positions", [])
            for x, y, z in positions:
                if not (0 <= z <= 4 and 0 <= x < (5 - z) and 0 <= y < (5 - z)):
                    return False, f"Défi #{id_defi} : position 3D invalide ({x}, {y}, {z}) pour {pid}."
                if (x, y, z) in cases_3d:
                    autre = cases_3d[(x, y, z)]
                    return (
                        False,
                        f"Défi #{id_defi} : superposition 3D en ({x}, {y}, {z}) entre {autre} et {pid}.",
                    )
                cases_3d[(x, y, z)] = pid

        return True, f"Intégrité 3D OK ({len(pieces_init)} pièces, {len(cases_3d)} billes)."

    return False, f"Mode inconnu : {mode}"


def initialiser_plateau_defi(id_defi: int | str) -> Plateau:
    """
    Signature officielle du contrat d'interface.
    Charge le défi et instancie un Plateau avec les pièces verrouillées de départ.
    """
    defi = charger_defi(id_defi)
    mode = defi.get("mode", "rectangle")
    plateau = Plateau()

    # Mémoriser le mode et l'id du défi sur l'instance pour faciliter le travail du solveur
    plateau.mode = mode
    plateau.id_defi = int(id_defi)

    if not hasattr(plateau, "pieces_verrouillees"):
        plateau.pieces_verrouillees = set()

    # Assurer la compatibilité entre self.grille (contrat) et self.plateau (main.py)
    if hasattr(plateau, "plateau") and not hasattr(plateau, "grille"):
        plateau.grille = plateau.plateau

    for p in defi.get("pieces_initiales", []):
        pid = p["id"]
        forme = [tuple(coord) for coord in p["forme"]] if "forme" in p else []
        x0 = p.get("x", 0)
        y0 = p.get("y", 0)

        # Pose de la pièce initiale sur le plateau
        # Supporte à la fois poser_piece(id_piece, forme, x, y, verrouillee=True)
        # et poser_piece(forme, x, y, id_piece)
        try:
            plateau.poser_piece(pid, forme, x0, y0, verrouillee=True)
        except TypeError:
            try:
                plateau.poser_piece(forme, x0, y0, pid)
            except Exception as e:
                raise RuntimeError(
                    f"Impossible de poser la pièce {pid} en ({x0}, {y0}) : {e}"
                )

        plateau.pieces_verrouillees.add(pid)

    return plateau


def verifier_solution(plateau: Any, id_defi: int | str) -> bool:
    """
    Compare l'état du plateau résolu avec la solution officielle du livret.
    Gère les grilles stockées sous forme de liste de listes ou de dictionnaire.
    """
    defi = charger_defi(id_defi)
    grille_attendue = defi.get("solution_grille")
    if not grille_attendue:
        return True

    mode = defi.get("mode", "rectangle")

    if mode in ("rectangle", "losange"):
        for y, ligne in enumerate(grille_attendue):
            symboles = ligne.split()
            for x, lettre in enumerate(symboles):
                if lettre == ".":
                    continue
                # Lecture de la case sur le plateau (supporte dict (x, y) ou grille[y][x])
                valeur_case = None
                if hasattr(plateau, "grille"):
                    if isinstance(plateau.grille, dict):
                        valeur_case = plateau.grille.get((x, y))
                    elif isinstance(plateau.grille, list):
                        valeur_case = plateau.grille[y][x]
                elif callable(getattr(plateau, "get_case", None)):
                    valeur_case = plateau.get_case(x, y)

                if valeur_case != lettre:
                    return False
        return True

    elif mode == "pyramide":
        # Grille 3D : liste de niveaux z=0..4
        for z, niveau in enumerate(grille_attendue):
            for y, ligne in enumerate(niveau):
                for x, lettre in enumerate(ligne.split()):
                    valeur_case = None
                    if hasattr(plateau, "grille"):
                        if isinstance(plateau.grille, dict):
                            valeur_case = plateau.grille.get((x, y, z))
                        elif isinstance(plateau.grille, list):
                            valeur_case = plateau.grille[z][y][x]
                    if valeur_case != lettre:
                        return False
        return True

    return True


def sauvegarder_solution(
    id_defi: int | str,
    plateau: Any,
    chemin_fichier: str | Path,
    format_export: str = "json",
) -> None:
    """
    Exporte la solution trouvée par le solveur au format JSON ou texte lisible.
    """
    chemin = Path(chemin_fichier)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    defi = charger_defi(id_defi)
    mode = defi.get("mode", "rectangle")

    # Reconstruction de la grille sous forme de liste de chaînes
    grille_export = []
    if mode == "rectangle":
        for y in range(5):
            ligne = []
            for x in range(11):
                val = (
                    plateau.grille.get((x, y), ".")
                    if isinstance(plateau.grille, dict)
                    else plateau.grille[y][x]
                )
                ligne.append(val if val is not None else ".")
            grille_export.append(" ".join(ligne))
    elif mode == "losange":
        for y in range(9):
            ligne = []
            for x in range(9):
                val = (
                    plateau.grille.get((x, y), ".")
                    if isinstance(plateau.grille, dict)
                    else plateau.grille[y][x]
                )
                ligne.append(val if val is not None else ".")
            grille_export.append(" ".join(ligne))

    donnees = {
        "id_defi": int(id_defi),
        "mode": mode,
        "difficulte": defi.get("difficulte", "Inconnue"),
        "solution_trouvee": grille_export,
        "pieces_placees": getattr(plateau, "pieces_placees", {}),
    }

    if format_export.lower() == "json" or chemin.suffix.lower() == ".json":
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump(donnees, f, indent=2, ensure_ascii=False)
    else:
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(f"=== Défi #{id_defi} ({mode} - {donnees['difficulte']}) ===\n\n")
            f.write("Solution :\n")
            for ligne in grille_export:
                f.write(f"  {ligne}\n")
