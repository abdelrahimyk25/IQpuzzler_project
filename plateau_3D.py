class Plateau3D :
    # Coordonnées valides : 0 <= z <= 4, et pour chaque z : 0 <= x < (5 - z), 0 <= y < (5 - z)
    def __init__(self):
        """Initialise un plateau vide de 5x5x5 cases."""
        self.plateau = {}
        for z in range(5):
            for y in range(5 - z):
                for x in range(5 - z):
                    self.plateau[(x, y, z)] = None
    def peut_placer(self, piece, x, y, z):
            """Vérifie si chaque bille de la pièce rentre dans le plateau sans collision."""
            for bx, by, bz in piece:
                nx = x + bx
                ny = y + by
                nz = z + bz

                # 1. Vérification des bordures du plateau
                if nx < 0 or nx >= 11 or ny < 0 or ny >= 5 or nz < 0 or nz >= 5:
                    return False
    
                # 2. Vérification de collision (la case doit être libre)
                if self.plateau[(nx, ny, nz)] is not None:
                    return False
    
            return True
    
    def poser_piece(self, piece, x, y,z, nom_piece):
            """Place toutes les billes de la pièce sur le plateau."""
            if not self.peut_placer(piece, x, y, z):
                return False
    
            for bx, by, bz in piece:
                self.plateau[(x + bx, y + by, z + bz)] = nom_piece
            return True
    
    def retirer_piece(self, piece, x, y, z):
            """Retire les billes de la pièce (indispensable pour l'IA quand elle fait marche arrière)."""
            for bx, by, bz in piece:
                self.plateau[(x + bx, y + by, z + bz)] = None
    
    def premiere_case_vide(self):
            """Trouve la toute première case vide (de haut en bas, gauche à droite)."""
            for z in range(5):
                for y in range(5 - z):
                    for x in range(5 - z):
                        if self.plateau[(x, y, z)] is None:
                            return (x, y, z)
            return None  # Le plateau est totalement plein !