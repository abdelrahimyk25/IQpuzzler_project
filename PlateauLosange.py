from plateau import Plateau
from collections import deque
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
    HAUTEUR = 9
    LARGEUR = 9

    def __init__(self):
        super().__init__()
        self.hauteur = 9
        self.largeur = 9
        self.grille = [[None] *self.largeur for _ in range(self.hauteur)]
        self.cases_interdites = set(CASES_INTERDITES)

        for x,y in self.cases_interdites:
            self.grille[y][x] = "#"

    def get_ilots_vides(self):
        # BFS : renvoie la liste des zones de cases vides connexes (4 voisins)
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
                        for nx, ny in ((cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)):
                            if self.dans_plateau(nx, ny) and self._est_vide(nx, ny) and (nx, ny) not in visitees:
                                visitees.add((nx, ny))
                                file.append((nx, ny))
                    ilots.append(ilot)
        return ilots

