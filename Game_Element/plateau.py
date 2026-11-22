from abc import ABC, abstractmethod
from collections import deque
from .pieces import CATALOGUE


class Plateau(ABC):
    """
    Interface abstraite commune à tous les plateaux (2D et 3D).
    Le solveur CSP ne dialogue qu'avec ces méthodes.
    """

    def __init__(self):
        self.pieces_placees = {}
        self.pieces_verrouillees = set()

    @abstractmethod
    def est_vide(self, case) -> bool:
        """Retourne True si la case (tuple 2D ou 3D) est libre."""
        pass

    @abstractmethod
    def lister_cases_vides(self) -> list:
        """Retourne la liste de toutes les cases actuellement libres."""
        pass

    @abstractmethod
    def obtenir_voisins(self, case) -> list:
        """Retourne la liste des cases voisines valides dans le plateau."""
        pass

    @abstractmethod
    def degre_max(self) -> int:
        """Nombre maximal de voisins d'une case (4 en 2D, 12 en pyramide 3D)."""
        pass

    @abstractmethod
    def nb_orientations(self, piece_id: str) -> int:
        """Retourne le nombre d'orientations possibles de la pièce sur ce plateau."""
        pass

    @abstractmethod
    def generer_placements_valides(self, piece_id: str) -> list[tuple]:
        """
        Retourne tous les placements valides de piece_id sur l'état actuel du plateau.
        Chaque placement est un tuple de coordonnées absolues (cases_absolues).
        """
        pass

    @abstractmethod
    def poser_cases(self, id_piece: str, coords, verrouillee: bool = False) -> bool:
        """Pose directement une pièce à partir de ses coordonnées absolues."""
        pass

    @abstractmethod
    def retirer_piece(self, id_piece: str) -> bool:
        """Retire une pièce non verrouillée du plateau."""
        pass

    @abstractmethod
    def copier(self) -> "Plateau":
        pass

    @abstractmethod
    def afficher(self):
        pass

    def est_complet(self) -> bool:
        return len(self.lister_cases_vides()) == 0


class Plateau2D(Plateau):
    """Base commune pour les plateaux 2D (Rectangle et Losange)."""

    @abstractmethod
    def __init__(self, largeur: int, hauteur: int):
        super().__init__()
        self.largeur = largeur
        self.hauteur = hauteur
        self.grille = [[None] * self.largeur for _ in range(self.hauteur)]

    def dans_plateau(self, x: int, y: int) -> bool:
        return 0 <= x < self.largeur and 0 <= y < self.hauteur

    def _est_vide(self, x: int, y: int) -> bool:
        return self.grille[y][x] in (None, ".")

    # --- Implémentation du contrat générique Plateau ---

    def est_vide(self, case: tuple[int, int]) -> bool:
        x, y = case
        return self.grille[y][x] is None

    def lister_cases_vides(self) -> list[tuple[int, int]]:
        cases_vides = []
        for y in range(self.hauteur):
            for x in range(self.largeur):
                if self.grille[y][x] is None:
                    cases_vides.append((x, y))
        return cases_vides

    def obtenir_voisins(self, case: tuple[int, int]) -> list[tuple[int, int]]:
        x, y = case
        voisins = []
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
        for dx, dy in directions:
            nx = x + dx
            ny = y + dy
            if self.dans_plateau(nx, ny):
                voisins.append((nx, ny))
        return voisins

    def degre_max(self) -> int:
        return 4

    def nb_orientations(self, piece_id: str) -> int:
        return len(CATALOGUE[piece_id])

    def generer_placements_valides(self, piece_id: str) -> list[tuple[tuple[int, int], ...]]:
        placements = []
        for orientation in CATALOGUE[piece_id]:
            for x0 in range(self.largeur):
                for y0 in range(self.hauteur):
                    if self.peut_placer(orientation, x0, y0):
                        cases_absolues = []
                        for dx, dy in orientation:
                            cases_absolues.append((x0 + dx, y0 + dy))
                        placements.append(tuple(cases_absolues))
        return placements

    def poser_cases(self, id_piece: str, coords, verrouillee: bool = False) -> bool:
        if id_piece in self.pieces_placees:
            return False
        for x, y in coords:
            if not self.dans_plateau(x, y) or not self.est_vide((x, y)):
                return False
        coords_liste = list(coords)
        for x, y in coords_liste:
            self.grille[y][x] = id_piece
        self.pieces_placees[id_piece] = coords_liste
        if verrouillee:
            self.pieces_verrouillees.add(id_piece)
        return True

    # --- Méthodes 2D conservées pour compatibilité (defis.py, tests...) ---

    def peut_placer(self, forme, x0: int, y0: int) -> bool:
        for dx, dy in forme:
            x, y = x0 + dx, y0 + dy
            if not self.dans_plateau(x, y) or not self._est_vide(x, y):
                return False
        return True

    def poser_piece(self, id_piece: str, forme, x0: int, y0: int, verrouillee: bool = False) -> bool:
        if id_piece in self.pieces_placees:
            return False
        if not self.peut_placer(forme, x0, y0):
            return False
        coords = [(x0 + dx, y0 + dy) for dx, dy in forme]
        for x, y in coords:
            self.grille[y][x] = id_piece
        self.pieces_placees[id_piece] = coords
        if verrouillee:
            self.pieces_verrouillees.add(id_piece)
        return True

    def retirer_piece(self, id_piece: str) -> bool:
        if id_piece not in self.pieces_placees:
            return False
        if id_piece in self.pieces_verrouillees:
            return False
        for x, y in self.pieces_placees.pop(id_piece):
            self.grille[y][x] = None
        return True

    def premiere_case_vide(self) -> tuple[int, int] | None:
        for x in range(self.largeur):
            for y in range(self.hauteur):
                if self._est_vide(x, y):
                    return (x, y)
        return None

    def get_ilots_vides(self):
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

    def copier(self) -> "Plateau2D":
        p = type(self)()
        p.hauteur = self.hauteur
        p.largeur = self.largeur
        p.grille = [ligne[:] for ligne in self.grille]
        p.pieces_placees = {i: j[:] for i, j in self.pieces_placees.items()}
        p.pieces_verrouillees = set(self.pieces_verrouillees)
        return p

    def afficher(self):
        for ligne in self.grille:
            print(" ".join(c if c else "." for c in ligne))
        print()