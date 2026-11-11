import json
from pathlib import Path

FICHIER_DEFIS = Path(__file__).parent / "defis.json"

def charger_tous_les_defis() -> dict:
    with open(FICHIER_DEFIS, "r", encoding="utf-8") as f:
        return json.load(f)

def charger_defi(id_defi: int) -> dict:
    """Signature officielle du contrat de données."""
    defis = charger_tous_les_defis()
    cle = str(id_defi)
    if cle not in defis:
        raise ValueError(f"Défi {id_defi} non trouvé dans {FICHIER_DEFIS}")
    return defis[cle]

def verifier_solution(plateau, id_defi: int) -> bool:
    """Compare le plateau résolu par le solveur avec la vraie solution officielle."""
    defi = charger_defi(id_defi)
    grille_attendue = defi.get("solution_grille")
    if not grille_attendue:
        return True  # Pas de solution pré-enregistrée
    
    for y, ligne in enumerate(grille_attendue):
        symboles = ligne.split()
        for x, lettre in enumerate(symboles):
            if plateau.grille[y][x] != lettre:
                return False
    return True