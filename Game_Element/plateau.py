from abc import ABC, abstractmethod
from collections import deque
from .pieces import CATALOGUE

class Plateau(ABC):
    # Un grid[y][x] : 
    @abstractmethod
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
       
        self.grille = [[None] * self.largeur for _ in range(self.hauteur)]
        # Listes des pieces placees et verrouillees
        self.pieces_placees = {} 
        self.pieces_verrouillees = set() # set pour pas permettre de bougé les pieces intialisé au debut

    def dans_plateau(self, x, y): # une fonction pour checker si une piece est dans le plateau ou pas
        return 0 <= x < self.largeur and 0 <= y < self.hauteur

    # Fonction pour verifier si une pieces peut etre placé ou pas
    # forme ici est une orientation normalisée
    # x0, y0 sont la position du coin haut-gauche de la forme sur le plateau
    def peut_placer(self, forme, x0, y0):
        for dx, dy in forme:
            # coordonnée réelle de la bille sur le plateau
            x, y = x0 + dx, y0 + dy
            # echec si on sort de plateau ou la case est déja occupée
            if not self.dans_plateau(x, y) or not self._est_vide(x, y):
                return False
        return True

    def poser_piece(self, id_piece, forme, x0, y0, verrouillee=False) -> bool:
        # verification que la piece est placée une seule fois
        if id_piece in self.pieces_placees:
            return False
        # verif avant d'ecrire
        if not self.peut_placer(forme, x0, y0):
            return False
        # calcul des coords absolues de chauqe bille
        coords = [(x0 + dx, y0 + dy) for dx, dy in forme]
        for x, y in coords:
            self.grille[y][x] = id_piece

        # on les memoris pour pouvoir retirer plutard
        self.pieces_placees[id_piece] = coords
        # piece de défi initial interdit de la retirer ensuite
        if verrouillee:
            self.pieces_verrouillees.add(id_piece)
        return True

    def retirer_piece(self, id_piece) -> bool:
        # pas possible de retirer un truc qui n'est pas sur le plateau Mdrr
        if id_piece not in self.pieces_placees:
            return False
        # eviter de retirer un piece de defi initial
        if id_piece in self.pieces_verrouillees:
            return False
        # retire l'entree du catalogue avec pop() et envoie ses coords
        for x, y in self.pieces_placees.pop(id_piece):
            self.grille[y][x] = None # on vide les cases
        return True

    def premiere_case_vide(self) -> tuple[int, int]:
        # on parcours col par col et de ligne haut a ligne bas jusqu'a quand on trouve la case
        for x in range(self.largeur):
            for y in range(self.hauteur):
                if self._est_vide(x, y):
                    return (x, y)
        return None

    def case_la_plus_contrainte(self) -> tuple[int, int]:
        """
        Retourne la case vide avec le moins de voisins vides adjacents (MRV géométrique).
        Ultra-rapide à calculer et cible naturellement les goulots d'étranglement.
        """
        case_min = None
        min_voisins = float('inf')

        for x in range(self.largeur):
            for y in range(self.hauteur):
                if self._est_vide(x, y):
                    voisins_vides = 0
                    
                    # Vérification des 4 directions : Haut, Bas, Gauche, Droite
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        # Vérifie si le voisin est dans les limites du plateau et s'il est vide
                        if self.dans_plateau(nx, ny) and self._est_vide(nx, ny):
                            voisins_vides += 1
                    
                    # Coupure instantanée : si une case a 0 voisin libre, c'est un trou isolé d'une case.
                    # On la retourne immédiatement pour que le solveur back-track tout de suite.
                    if voisins_vides == 0:
                        return (x, y)

                    if voisins_vides < min_voisins:
                        min_voisins = voisins_vides
                        case_min = (x, y)

        return case_min

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

    # fonction pour la fin de jeu quand le plateau est complet
    def est_complet(self) -> bool: 
        return self.premiere_case_vide() is None

    # fonction pour verifier si le plateau est vide ou pas 
    def _est_vide(self, x, y): 
        return self.grille[y][x] is None

    # constructeur pour copier un plateau
    def copier(self) -> "Plateau":
        p = type(self)()
        p.hauteur = self.hauteur
        p.largeur = self.largeur
        p.grille = [ligne[:] for ligne in self.grille]
        p.pieces_placees = {i: j[:] for i, j in self.pieces_placees.items()}
        p.pieces_verrouillees = set(self.pieces_verrouillees)
        return p

    # fonction pour afficher le plateau
    def afficher(self):
        for ligne in self.grille:
            print(" ".join(c if c else "." for c in ligne))
        print()