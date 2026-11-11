"""
Module plateau.py
Gestion de la grille de jeu, des placements et des vérifications de collisions.
"""

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

    def tailles_ilots_vides(self):
        """
        Parcours (DFS itératif) des cases vides : retourne la liste des tailles des zones
        vides contiguës (4-connexité). Sert à détecter les îlots morts.
        """
        vus = set()
        tailles = []
        for depart, val in self.plateau.items():
            if val is not None or depart in vus:
                continue
            vus.add(depart)
            file = [depart]
            taille = 0
            while file:
                cx, cy = file.pop()
                taille += 1
                for v in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if v in self.plateau and self.plateau[v] is None and v not in vus:
                        vus.add(v)
                        file.append(v)
            tailles.append(taille)
        return tailles
