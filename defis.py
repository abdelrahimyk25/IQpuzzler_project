"""
Module defis.py
Bibliothèque de défis : pièces pré-posées en coordonnées absolues (x, y).
"""

from csp import Defi

# Défi de test avec 3 pièces manquantes (A, B, C) et solution unique.
# NB : il a été généré à partir d'une solution du plateau vide puis vérifié
# (unicité) par le solveur ; ce n'est PAS le défi officiel #179/#180 du livret,
# dont l'énoncé n'est pas fourni. Pour saisir un défi officiel, il suffit de
# lister les cases (x, y) de chaque pièce posée : voir `Defi`.
DEFI_TEST_3_MANQUANTES = Defi(
    numero=0,
    pieces_fixes={
        "D": [(6, 0), (7, 0), (7, 1), (8, 1)],
        "H": [(8, 0), (9, 0), (10, 0), (10, 1), (10, 2)],
        "E": [(3, 2), (3, 3), (3, 4), (4, 1), (4, 2)],
        "G": [(6, 1), (7, 2), (7, 3), (7, 4)],
        "K": [(8, 2), (9, 1), (9, 2), (9, 3)],
        "F": [(4, 3), (4, 4), (5, 2), (5, 3), (6, 2)],
        "J": [(0, 4), (1, 3), (1, 4), (2, 3), (2, 4)],
        "I": [(5, 4), (6, 3), (6, 4)],
        "L": [(8, 3), (8, 4), (9, 4), (10, 3), (10, 4)],
    },
)
