from pieces import PIECES, generer_orientations, normalize_piece
from plateau import Plateau

LARGEUR = 11
HAUTEUR = 5


# 1. Catalogue des formes possibles pour chaque pièce (sans symétries)
def construire_catalogue():
    catalogue = {}
    for lettre, infos in PIECES.items():
        catalogue[lettre] = generer_orientations(infos["coords"])
    return catalogue

CATALOGUE = construire_catalogue()


# 2. Génération du domaine D_i d'une pièce (tous les placements dans la grille)
def generer_domaine(lettre):
    """
    Retourne la liste de tous les placements (orientation, x, y) qui ne
    débordent pas du plateau (Consistance de noeud / contrainte unaire).
    """
    plateau_vide = Plateau()
    domaine = []
    
    for orientation in CATALOGUE[lettre]:
        for y in range(HAUTEUR):
            for x in range(LARGEUR):
                if plateau_vide.peut_placer(orientation, x, y):
                    domaine.append((orientation, x, y))
    return domaine


# 3. Définition d'un défi de départ
class Defi:
    def __init__(self, numero, pieces_fixes):
        self.numero = numero
        self.pieces_fixes = pieces_fixes  # dict {lettre: [(x, y), ...]}

    def valider(self):
        """Vérifie que les pièces de départ sont valides et dans la grille."""
        cases_occupees = set()
        for lettre, cases in self.pieces_fixes.items():
            if lettre not in PIECES:
                raise ValueError(f"Pièce inconnue : {lettre}")
            if sorted(normalize_piece(cases)) not in CATALOGUE[lettre]:
                raise ValueError(f"Forme invalide pour la pièce {lettre}")
            for x, y in cases:
                if not (0 <= x < LARGEUR and 0 <= y < HAUTEUR):
                    raise ValueError(f"La pièce {lettre} sort du plateau")
                if (x, y) in cases_occupees:
                    raise ValueError(f"Chevauchement sur la pièce {lettre}")
                cases_occupees.add((x, y))


# 4. Solveur CSP : P = (X, D, C) résolu par Backtracking (Test & Generate)
class SolveurCSP:
    def __init__(self, defi, elagage_ilots=True):
        defi.valider()
        self.defi = defi
        self.elagage_ilots = elagage_ilots

        # Initialisation du plateau avec les pièces déjà posées du défi
        self.plateau = Plateau()
        for lettre, cases in defi.pieces_fixes.items():
            for x, y in cases:
                self.plateau.plateau[(x, y)] = lettre

        # X : Les variables sont les pièces qu'il reste à placer
        self.variables = [l for l in PIECES if l not in defi.pieces_fixes]
        self.tailles_pieces = {l: len(PIECES[l]["coords"]) for l in PIECES}

        # D : Les domaines filtrés (on garde les placements qui ne touchent pas les pièces fixes)
        self.domaines = {}
        for lettre in self.variables:
            self.domaines[lettre] = [
                (orient, x, y)
                for (orient, x, y) in generer_domaine(lettre)
                if self.plateau.peut_placer(orient, x, y)
            ]

        self.stats = {"noeuds": 0, "backtracks": 0, "ilots_elagues": 0}
        self.solutions = []

    def ilot_mort(self, pieces_restantes):
        """Retourne True s'il y a un trou vide plus petit que la plus petite pièce restante."""
        if not pieces_restantes:
            return False
        plus_petite = min(self.tailles_pieces[l] for l in pieces_restantes)
        for taille_trou in self.plateau.tailles_ilots_vides():
            if taille_trou < plus_petite:
                return True
        return False

    def resoudre(self, max_solutions=1):
        self.stats = {"noeuds": 0, "backtracks": 0, "ilots_elagues": 0}
        self.solutions = []
        self.choix_actuels = {}

        if self.elagage_ilots and self.ilot_mort(self.variables):
            return []

        self.backtrack(self.variables, max_solutions)
        return self.solutions

    def backtrack(self, pieces_restantes, max_solutions):
        self.stats["noeuds"] += 1

        # 1. On cherche la première case vide en haut à gauche
        case_cible = self.plateau.premiere_case_vide()
        if case_cible is None:
            # Plus aucune case vide : toutes les pièces sont posées, c'est gagné !
            self.solutions.append(dict(self.choix_actuels))
            return len(self.solutions) >= max_solutions

        cible_x, cible_y = case_cible

        # 2. On essaie de couvrir cette case vide avec une des pièces restantes
        for lettre in pieces_restantes:
            for orientation in CATALOGUE[lettre]:
                # Comme le plateau est rempli de haut en bas et de gauche à droite,
                # la 1re bille de la pièce (en y puis x) doit tomber sur (cible_x, cible_y)
                premiere_bille = min(orientation, key=lambda b: (b[1], b[0]))
                x = cible_x - premiere_bille[0]
                y = cible_y - premiere_bille[1]

                # TEST : La pièce rentre-t-elle sans déborder ni chevaucher ?
                if not self.plateau.peut_placer(orientation, x, y):
                    continue

                # GENERATE : On pose la pièce sur le plateau
                self.plateau.poser_piece(orientation, x, y, lettre)
                self.choix_actuels[lettre] = (orientation, x, y)
                nouvelles_restantes = [l for l in pieces_restantes if l != lettre]

                # Vérification des îlots morts avant de continuer à descendre l'arbre
                if self.elagage_ilots and self.ilot_mort(nouvelles_restantes):
                    self.stats["ilots_elagues"] += 1
                    doit_arreter = False
                else:
                    doit_arreter = self.backtrack(nouvelles_restantes, max_solutions)

                # BACKTRACK : On retire la pièce pour tester les autres possibilités
                self.plateau.retirer_piece(orientation, x, y)
                del self.choix_actuels[lettre]
                self.stats["backtracks"] += 1

                if doit_arreter:
                    return True

        return False

    def plateau_avec_solution(self, solution):
        """Crée une copie du plateau contenant le défi résolu pour l'afficher."""
        pl = Plateau()
        pl.plateau.update(self.plateau.plateau)
        for lettre, (orientation, x, y) in solution.items():
            pl.poser_piece(orientation, x, y, lettre)
        return pl