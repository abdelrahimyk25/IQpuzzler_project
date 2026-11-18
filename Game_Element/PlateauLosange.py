from .plateau import Plateau

INTERDIT = "#"
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
        super().__init__(largeur=self.LARGEUR, hauteur=self.HAUTEUR)
        # mettre des case inutilisable pour la losange
        self.cases_interdites = set(CASES_INTERDITES)

        for x, y in self.cases_interdites:
            self.grille[y][x] = INTERDIT

    def dans_plateau(self, x, y):
        # Une case fait partie du losange si elle est dans la grille 9x9 ET non interdite
        return super().dans_plateau(x, y) and (x, y) not in self.cases_interdites

    def copier(self) -> "PlateauLosange":
        p = super().copier()
        p.cases_interdites = set(self.cases_interdites)
        return p