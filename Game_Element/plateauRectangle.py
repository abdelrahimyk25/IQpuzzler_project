from .plateau import Plateau

# definir les dims (5x11)
HAUTEUR = 5 # 0...4
LARGEUR = 11 # 0....10

class PlateauRectangle(Plateau):
    HAUTEUR = HAUTEUR
    LARGEUR = LARGEUR

    def __init__(self):
        super().__init__(self.LARGEUR, self.HAUTEUR)