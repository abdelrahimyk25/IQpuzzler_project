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
    HAUTEUR = 9
    LARGEUR = 9

    def __init__(self):
        super().__init__()
        self.hauteur = 9
        self.largeur = 9
        self.grille = [[None] *self.hauteur for _ in range(self.largeur)]
        self.cases_interdit = set(CASES_INTERDITES)

        for x,y in self.cases_interdites:
            self.grille[y][x] = "#"


