"""
Module pieces.py
Définition des pièces officielles et fonctions de transformations géométriques.
"""

PIECES = {
    "A": {"nom": "Jaune", "couleur": "#F1C40F", "coords": [(0, 1), (1, 1), (2, 1), (3, 1), (2, 0)]},
    "B": {"nom": "Orange", "couleur": "#E67E22", "coords": [(2, 0), (0, 1), (1, 1), (2, 1), (1, 2)]},
    "C": {"nom": "Rouge", "couleur": "#E74C3C", "coords": [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)]},
    "D": {"nom": "Bordeaux", "couleur": "#922B21", "coords": [(1, 0), (0, 1), (1, 1), (0, 2)]},
    "E": {"nom": "Rose", "couleur": "#E84393", "coords": [(0, 0), (0, 1), (0, 2), (1, 2), (1, 3)]},
    "F": {"nom": "Violet", "couleur": "#8E44AD", "coords": [(2, 0), (1, 1), (2, 1), (0, 2), (1, 2)]},
    "G": {"nom": "Bleu Fonce", "couleur": "#1B1464", "coords": [(1, 0), (2, 0), (3, 0), (0, 1)]},
    "H": {"nom": "Bleu Cyan", "couleur": "#00CEC9", "coords": [(2, 0), (2, 1), (0, 2), (1, 2), (2, 2)]},
    "I": {"nom": "Bleu Ciel", "couleur": "#74B9FF", "coords": [(0, 0), (1, 0), (1, 1)]},
    "J": {"nom": "Turquoise", "couleur": "#55E6C1", "coords": [(0, 0), (0, 1), (1, 1), (0, 2), (1, 2)]},
    "K": {"nom": "Vert Emeraude", "couleur": "#27AE60", "coords": [(0, 0), (1, 0), (2, 0), (1, 1)]},
    "L": {"nom": "Vert Pomme", "couleur": "#A8E6CF", "coords": [(0, 0), (1, 0), (1, 1), (0, 2), (1, 2)]},
}

def afficher_toutes_les_pieces():
    """Dessine chaque pièce dans la console pour vérifier visuellement."""
    for lettre, p in PIECES.items():
        coords = p["coords"]
        max_x = max(c[0] for c in coords) + 1
        max_y = max(c[1] for c in coords) + 1
        print(f"--- Pièce {lettre} ({p['nom']} - {len(coords)} billes) ---")
        for y in range(max_y):
            ligne = ""
            for x in range(max_x):
                ligne += "● " if (x, y) in coords else "  "
            print(ligne)
        print()

def translate_piece(piece, dx, dy):
    nouvelle_piece = []
    for x, y in piece:
        nouvelle_piece.append((x + dx, y + dy))
    return nouvelle_piece

def rotate_piece90(piece):
    nouvelle_piece = []
    for x, y in piece:
        nouvelle_piece.append((-y, x))
    return nouvelle_piece

def miroir_piece(piece):
    nouvelle_piece = []
    for x, y in piece:
        nouvelle_piece.append((-x, y))
    return nouvelle_piece

def min_x_y(piece):
    min_x = min(x for x, y in piece)
    min_y = min(y for x, y in piece)
    return (min_x, min_y)

def normalize_piece(piece):
    min_x, min_y = min_x_y(piece)
    # Tri canonique : deux orientations identiques doivent donner la même liste,
    # sinon la détection des symétries (comparaison de listes) échoue.
    return sorted(translate_piece(piece, -min_x, -min_y))

def generer_orientations(piece):
    orientations = [] 
    for i in range(4):
        piece = rotate_piece90(piece)
        normalized = normalize_piece(piece)
        if normalized not in orientations:
            orientations.append(normalized)
    miroir = miroir_piece(piece)
    for i in range(4):
        miroir = rotate_piece90(miroir)
        normalized = normalize_piece(miroir)
        if normalized not in orientations:
            orientations.append(normalized)
    return orientations