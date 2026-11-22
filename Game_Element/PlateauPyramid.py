from .plateau import Plateau
from .orientation3D import CATALOGUE_3D  # À adapter selon le nom dans orientation3D.py

# Les 12 directions voisines dans un empilement pyramidal compact :
# 4 sur le même étage, 4 sur l'étage au-dessus (z+1), 4 sur l'étage en dessous (z-1)
DIRECTIONS_3D = (
    (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0),
    (0, 0, 1), (-1, 0, 1), (0, -1, 1), (-1, -1, 1),
    (0, 0, -1), (1, 0, -1), (0, 1, -1), (1, 1, -1),
)


class PlateauPyramid(Plateau):
    HAUTEUR = 5  # Étages z = 0 (5x5), 1 (4x4), 2 (3x3), 3 (2x2), 4 (1x1)

    def __init__(self):
        super().__init__()
        # grille[z][y][x] : chaque étage z est une matrice carrée (5 - z) x (5 - z)
        self.grille = []
        for z in range(self.HAUTEUR):
            taille = self.HAUTEUR - z
            etage = [[None] * taille for _ in range(taille)]
            self.grille.append(etage)

    def dans_plateau(self, x: int, y: int, z: int) -> bool:
        if z < 0 or z >= self.HAUTEUR:
            return False
        taille = self.HAUTEUR - z
        return 0 <= x < taille and 0 <= y < taille

    # --- Implémentation du contrat générique Plateau ---

    def est_vide(self, case: tuple[int, int, int]) -> bool:
        x, y, z = case
        return self.grille[z][y][x] is None

    def lister_cases_vides(self) -> list[tuple[int, int, int]]:
        cases_vides = []
        for z in range(self.HAUTEUR):
            taille = self.HAUTEUR - z
            for y in range(taille):
                for x in range(taille):
                    if self.grille[z][y][x] is None:
                        cases_vides.append((x, y, z))
        return cases_vides

    def obtenir_voisins(self, case: tuple[int, int, int]) -> list[tuple[int, int, int]]:
        x, y, z = case
        voisins = []
        for dx, dy, dz in DIRECTIONS_3D:
            nx = x + dx
            ny = y + dy
            nz = z + dz
            if self.dans_plateau(nx, ny, nz):
                voisins.append((nx, ny, nz))
        return voisins

    def degre_max(self) -> int:
        return 12

    def nb_orientations(self, piece_id: str) -> int:
        return len(CATALOGUE_3D[piece_id])

    def peut_placer(self, forme, x0: int, y0: int, z0: int) -> bool:
        for dx, dy, dz in forme:
            x = x0 + dx
            y = y0 + dy
            z = z0 + dz
            if not self.dans_plateau(x, y, z) or self.grille[z][y][x] is not None:
                return False
        return True

    def generer_placements_valides(self, piece_id: str) -> list[tuple[tuple[int, int, int], ...]]:
        placements = []
        deja_vus = set()

        for orientation in CATALOGUE_3D[piece_id]:
            for z0 in range(self.HAUTEUR):
                for y0 in range(self.HAUTEUR):
                    for x0 in range(self.HAUTEUR):
                        if self.peut_placer(orientation, x0, y0, z0):
                            cases_absolues = []
                            for dx, dy, dz in orientation:
                                cases_absolues.append((x0 + dx, y0 + dy, z0 + dz))
                            cle = frozenset(cases_absolues)
                            if cle not in deja_vus:
                                deja_vus.add(cle)
                                placements.append(tuple(cases_absolues))
        return placements

    def poser_cases(self, id_piece: str, coords, verrouillee: bool = False) -> bool:
        if id_piece in self.pieces_placees:
            return False
        for x, y, z in coords:
            if not self.dans_plateau(x, y, z) or self.grille[z][y][x] is not None:
                return False
        coords_liste = list(coords)
        for x, y, z in coords_liste:
            self.grille[z][y][x] = id_piece
        self.pieces_placees[id_piece] = coords_liste
        if verrouillee:
            self.pieces_verrouillees.add(id_piece)
        return True

    def poser_piece(self, id_piece: str, forme, x0: int, y0: int, z0: int, verrouillee: bool = False) -> bool:
        coords = [(x0 + dx, y0 + dy, z0 + dz) for dx, dy, dz in forme]
        return self.poser_cases(id_piece, coords, verrouillee)

    def retirer_piece(self, id_piece: str) -> bool:
        if id_piece not in self.pieces_placees:
            return False
        if id_piece in self.pieces_verrouillees:
            return False
        for x, y, z in self.pieces_placees.pop(id_piece):
            self.grille[z][y][x] = None
        return True

    def copier(self) -> "PlateauPyramid":
        p = PlateauPyramid()
        p.grille = [[ligne[:] for ligne in etage] for etage in self.grille]
        p.pieces_placees = {i: j[:] for i, j in self.pieces_placees.items()}
        p.pieces_verrouillees = set(self.pieces_verrouillees)
        return p

    def afficher(self):
        for z in range(self.HAUTEUR):
            print(f"--- Étage z={z} ---")
            for ligne in self.grille[z]:
                print(" ".join(c if c else "." for c in ligne))
        print()