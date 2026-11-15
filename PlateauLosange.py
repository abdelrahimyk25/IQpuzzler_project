from collections import deque
from plateau import Plateau

CASES_INTERDITES = [
    # y = 0 : "####....#"
    (0, 0), (1, 0), (2, 0), (3, 0), (8, 0),
    # y = 1 : "####....."
    (0, 1), (1, 1), (2, 1), (3, 1),
    # y = 2 : "##......."
    (0, 2), (1, 2),
    # y = 3 : "##......."
    (0, 3), (1, 3),
    # y = 4 : "........." (rien)
    # y = 5 : ".......##"
    (7, 5), (8, 5),
    # y = 6 : ".......##"
    (7, 6), (8, 6),
    # y = 7 : ".....####"
    (5, 7), (6, 7), (7, 7), (8, 7),
    # y = 8 : "#....####"
    (0, 8), (5, 8), (6, 8), (7, 8), (8, 8),
]


class PlateauLosange(Plateau):
    """
    Plateau en mode Losange (9x9) pour le jeu IQ-Puzzler Pro XXL.
    Hérite de Plateau et redéfinit les dimensions et méthodes pour la grille 9x9.
    """
    HAUTEUR = 9
    LARGEUR = 9

    def __init__(self):
        super().__init__()
        self.hauteur = 9
        self.largeur = 9
        self.grille = [[None] * self.largeur for _ in range(self.hauteur)]
        self.cases_interdites = set(CASES_INTERDITES)

        # Remplissage des 26 cases hors plateau
        for x, y in self.cases_interdites:
            self.grille[y][x] = "#"

    def dans_plateau(self, x: int, y: int) -> bool:
        """Vérifie si les coordonnées sont dans la grille 9x9."""
        return 0 <= x < self.largeur and 0 <= y < self.hauteur

    def premiere_case_vide(self) -> tuple[int, int] | None:
        """Recherche la première case vide sur l'ensemble de la grille 9x9."""
        for x in range(self.largeur):
            for y in range(self.hauteur):
                if self._est_vide(x, y):
                    return (x, y)
        return None

    def get_ilots_vides(self) -> list[set[tuple[int, int]]]:
        """Détection BFS des îlots de cases vides adaptée aux dimensions 9x9."""
        ilots = []
        visitees = set()
        for y in range(self.hauteur):
            for x in range(self.largeur):
                if self._est_vide(x, y) and (x, y) not in visitees:
                    ilot = set()
                    file = deque([(x, y)])
                    visitees.add((x, y))
                    while file:
                        cx, cy = file.popleft()
                        ilot.add((cx, cy))
                        for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                            if self.dans_plateau(nx, ny) and self._est_vide(nx, ny) and (nx, ny) not in visitees:
                                visitees.add((nx, ny))
                                file.append((nx, ny))
                    ilots.append(ilot)
        return ilots
