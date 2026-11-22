from .plateau import Plateau2D

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

class PlateauLosange(Plateau2D):
    HAUTEUR = 9
    LARGEUR = 9

    def __init__(self):
        super().__init__(largeur=self.LARGEUR, hauteur=self.HAUTEUR)
        self.cases_interdites = set(CASES_INTERDITES)

        for x, y in self.cases_interdites:
            assert super().dans_plateau(x, y), f"case interdite hors grille : {(x, y)}"
            self.grille[y][x] = INTERDIT

    def dans_plateau(self, x: int, y: int) -> bool:
        return super().dans_plateau(x, y) and (x, y) not in self.cases_interdites

    def copier(self) -> "PlateauLosange":
        p = super().copier()
        p.cases_interdites = set(self.cases_interdites)
        return p