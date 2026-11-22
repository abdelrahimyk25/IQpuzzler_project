from .plateau import Plateau2D

HAUTEUR = 5   # 0...4
LARGEUR = 11  # 0...10


class PlateauRectangle(Plateau2D):
    HAUTEUR = HAUTEUR
    LARGEUR = LARGEUR

    def __init__(self):
        super().__init__(largeur=self.LARGEUR, hauteur=self.HAUTEUR)