"""
Point d'entrée main.py
Script principal d'exécution et de test du projet.
"""

import sys
from pieces import PIECES, afficher_toutes_les_pieces, translate_piece
from plateau import Plateau
from csp import SolveurCSP
from defis import DEFI_TEST_3_MANQUANTES

def main():
    sys.stdout.reconfigure(encoding='utf-8')

    print("=== TEST 1 : Initialisation des pièces ===")
    afficher_toutes_les_pieces()
    total = sum(len(p["coords"]) for p in PIECES.values())
    print(f"✅ Total des billes des 12 pièces : {total} / 55\n")

    print("=== TEST 2 : Transformations géométriques ===")
    pieces_translates = translate_piece(PIECES["L"]["coords"], 2, 3)
    print("Pièce L (Vert Pomme) après translation de (2, 3) :", pieces_translates)
    print("Nombre de billes après translation :", len(pieces_translates))
    print("Coordonnées des billes après translation :", pieces_translates, "\n")

    print("=== TEST 3 : Placement sur le plateau ===")
    p = Plateau()
    piece_I = PIECES["I"]["coords"]
    
    # On la pose en haut à gauche (0, 0)
    print("Tentative de placement de la pièce I en (0,0)...")
    p.poser_piece(piece_I, 0, 0, "I")
    p.poser_piece(piece_I, 0, 2, "I")
    p.afficher()
    
    # On vérifie la première case vide restante
    print("Prochaine case vide :", p.premiere_case_vide())

    print("\n=== TEST 4 : Résolution CSP (Test & Generate + élagage d'îlots) ===")
    solveur = SolveurCSP(DEFI_TEST_3_MANQUANTES)
    print("Variables X :", solveur.variables)
    print("Tailles des domaines D :", {l: len(d) for l, d in solveur.domaines.items()})
    print("Plateau du défi :")
    solveur.plateau.afficher()
    solutions = solveur.resoudre(max_solutions=2)  # 2 pour vérifier l'unicité
    print(f"Solutions trouvées : {len(solutions)} (unicité : {len(solutions) == 1})")
    print("Statistiques :", solveur.stats)
    if solutions:
        solveur.plateau_avec_solution(solutions[0]).afficher()

if __name__ == "__main__":
    main()