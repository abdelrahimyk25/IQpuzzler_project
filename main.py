"""
pieces.py - Les 12 pièces officielles vérifiées de l'IQ Puzzler Pro XXL
Total = 55 billes 3EME VERIF (verif que le main est bien lier au projet github)
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

PIECES = {
    # A - Jaune (5 billes)
    # . . ● .
    # ● ● ● ●
    "A": {
        "nom": "Jaune",
        "couleur": "#F1C40F",
        "coords": [(0, 1), (1, 1), (2, 1), (3, 1), (2, 0)],
    },
    # B - Orange (5 billes)
    # . . ●
    # ● ● ●
    # . ● .
    "B": {
        "nom": "Orange",
        "couleur": "#E67E22",
        "coords": [(2, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    },
    # C - Rouge vif (5 billes)
    # ● ● ● ●
    # . . . ●
    "C": {
        "nom": "Rouge",
        "couleur": "#E74C3C",
        "coords": [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)],
    },
    # D - Rouge bordeaux (4 billes)
    # . ●
    # ● ●
    # ● .
    "D": {
        "nom": "Bordeaux",
        "couleur": "#922B21",
        "coords": [(1, 0), (0, 1), (1, 1), (0, 2)],
    },
    # E - Rose (5 billes)
    # ● .
    # ● .
    # ● ●
    # . ●
    "E": {
        "nom": "Rose",
        "couleur": "#E84393",
        "coords": [(0, 0), (0, 1), (0, 2), (1, 2), (1, 3)],
    },
    # F - Violet foncé (5 billes)
    # . . ●
    # . ● ●
    # ● ● .
    "F": {
        "nom": "Violet",
        "couleur": "#8E44AD",
        "coords": [(2, 0), (1, 1), (2, 1), (0, 2), (1, 2)],
    },
    # G - Bleu foncé (4 billes)
    # . ● ● ●
    # ● . . .
    "G": {
        "nom": "Bleu Fonce",
        "couleur": "#1B1464",
        "coords": [(0, 0), (1, 0), (2, 0), (0, 1)],
    },
    # H - Bleu cyan (5 billes en grand L)
    # . . ●
    # . . ●
    # ● ● ●
    "H": {
        "nom": "Bleu Cyan",
        "couleur": "#00CEC9",
        "coords": [(2, 0), (2, 1), (0, 2), (1, 2), (2, 2)],
    },
    # I - Bleu ciel (3 billes en petit coin)
    # ● ●
    # . ●
    "I": {
        "nom": "Bleu Ciel",
        "couleur": "#74B9FF",
        "coords": [(0, 0), (1, 0), (1, 1)],
    },
    # J - Turquoise pâle (5 billes : anneau carré de 4 + 1 au-dessus)
    # ● .
    # ● ●
    # ● ●
    "J": {
        "nom": "Turquoise",
        "couleur": "#55E6C1",
        "coords": [(0, 0), (0, 1), (1, 1), (0, 2), (1, 2)],
    },
    # K - Vert émeraude (4 billes en T)
    # ● ● ●
    # . ● .
    "K": {
        "nom": "Vert Emeraude",
        "couleur": "#27AE60",
        "coords": [(0, 0), (1, 0), (2, 0), (1, 1)],
    },
    # L - Vert pomme (5 billes en U vertical)
    # ● ●
    # . ●
    # ● ●
    "L": {
        "nom": "Vert Pomme",
        "couleur": "#A8E6CF",
        "coords": [(0, 0), (1, 0), (1, 1), (0, 2), (1, 2)],
    },
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


if __name__ == "__main__":
    afficher_toutes_les_pieces()
    total = sum(len(p["coords"]) for p in PIECES.values())
    print(f"✅ Total des billes des 12 pièces : {total} / 55")


def translate_piece(piece, dx, dy):
    nouvelle_piece = []
    for x, y in piece:
        nouvelle_piece.append((x + dx, y + dy))
    return nouvelle_piece

pieces_translates=translate_piece(PIECES["L"]["coords"], 2, 3)
print("Pièce Bleu Clair après translation de (2, 3) :", pieces_translates)
print("Nombre de billes après translation :", len(pieces_translates))
print("Coordonnées des billes après translation :", pieces_translates)

def rotate_piece90(piece):
    nouvelle_piece = []
    for x,y in piece:
        nouvelle_piece.append((-y, x))
    return nouvelle_piece
def miroir_piece(piece):
    nouvelle_piece = []
    for x,y in piece:
        
        nouvelle_piece.append((-x, y))
    return nouvelle_piece
def min_x_y(piece):
    min_x = min(x for x,y in piece)
    min_y = min(y for x,y in piece)
    return (min_x, min_y)
def normalize_piece(piece):
    min_x, min_y = min_x_y(piece)
    return translate_piece(piece, -min_x, -min_y)

def generer_orientations(piece):
    orientations= [] 
    for i in range(4):
        normalized = normalize_piece(piece)
        if normalized not in orientations:
            orientations.append(normalized)
    miroir = miroir_piece(piece)
    for i in range(4):
        normalized = normalize_piece(miroir)
        if normalized not in orientations:
            orientations.append(normalized)
    return orientations

class Plateau:
    def __init__(self):
        """Initialise un plateau vide de 11 colonnes (x) et 5 lignes (y) -> 55 cases."""
        self.plateau = {}
        for y in range(5):
            for x in range(11):
                self.plateau[(x, y)] = None

    def peut_placer(self, piece, x, y):
        """Vérifie si chaque bille de la pièce rentre dans le plateau sans collision."""
        for bx, by in piece:
            nx = x + bx
            ny = y + by

            # 1. Vérification des bordures du plateau
            if nx < 0 or nx >= 11 or ny < 0 or ny >= 5:
                return False

            # 2. Vérification de collision (la case doit être libre)
            if self.plateau[(nx, ny)] is not None:
                return False

        return True

    def poser_piece(self, piece, x, y, nom_piece):
        """Place toutes les billes de la pièce sur le plateau."""
        if not self.peut_placer(piece, x, y):
            return False

        for bx, by in piece:
            self.plateau[(x + bx, y + by)] = nom_piece
        return True

    def retirer_piece(self, piece, x, y):
        """Retire les billes de la pièce (indispensable pour l'IA quand elle fait marche arrière)."""
        for bx, by in piece:
            self.plateau[(x + bx, y + by)] = None

    def premiere_case_vide(self):
        """Trouve la toute première case vide (de haut en bas, gauche à droite)."""
        for y in range(5):
            for x in range(11):
                if self.plateau[(x, y)] is None:
                    return (x, y)
        return None  # Le plateau est totalement plein !

    def afficher(self):
        """Affiche le plateau visuellement dans le terminal."""
        print("-" * 25)
        for y in range(5):
            ligne = []
            for x in range(11):
                val = self.plateau[(x, y)]
                ligne.append(val if val is not None else ".")
            print(" ".join(ligne))
        print("-" * 25)

p = Plateau()

# Pièce I (petit coin de 3 billes)
piece_I = [(0, 0), (1, 0), (1, 1)]

# On la pose en haut à gauche (0, 0)
p.poser_piece(piece_I, 0, 0, "I")
p.afficher()

# On vérifie la première case vide restante
print("Prochaine case vide :", p.premiere_case_vide())