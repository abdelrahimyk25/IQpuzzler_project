from __future__ import annotations
import time
from collections import deque
from typing import Any

from pieces import PIECES, generate_catalogue_orient
from plateau import Plateau, HAUTEUR, LARGEUR
from defis import Defi

CATALOGUE = generate_catalogue_orient()

def critere_tri_piece(lettre: str) -> tuple[int, int]:
            taille_piece = PIECES[lettre]["coords"]
            nb_orientations = len(CATALOGUE[lettre])
            return (taille_piece, nb_orientations)

class SolverCSP:
    """
    Moteur de résolution CSP ad hoc (Test & Generate / Backtracking)
    pour le jeu IQ-Puzzler Pro XXL.
    """

    def __init__(self, defi: Defi, activer_ilots_morts: bool = True):
        self.defi = defi
        self.plateau: Plateau = defi.plateau
        self.activer_ilots_morts = activer_ilots_morts

        # Tri heuristique des variables X plus lisible (taille décroissante, puis nombre d'orientations décroissant)
        self.variables_X = sorted(defi.piece_libres, key=critere_tri_piece, reverse=True)

        # Génération des domaines finis D en extension (consistance de nœud)
        self.domaines_D = self._generer_domaines_initiaux()

        # Métriques d'évaluation de l'IA
        self.noeuds_explores: int = 0
        self.backtracks: int = 0
        self.temps_execution_ms: float = 0.0

    def _generer_domaines_initiaux(self) -> dict[str, list[tuple[list[tuple[int, int]], int, int]]]:
        """Construit le domaine D_i de chaque pièce X_i sur le plateau de départ.
        Verifie les 2 contraintes: non-débordement et compatibilité avec les pièces 
        verrouillées du défi)."""
        domaines = {}
        h = len(self.plateau.grille)
        if h > 0:
            w = len(self.plateau.grille[0])
        else:
            w = 0

        """Parcours exhaustif de toutes les positions possibles pour chaque pièce X_i
        et toutes ses orientations (rotation + miroir) sur le plateau."""
        for piece_id in self.variables_X:
            placements_valides = []
            for orientation in CATALOGUE[piece_id]:
                for x in range(w):
                    for y in range(h):
                        if self.plateau.peut_placer(orientation, x, y):
                            placements_valides.append((orientation, x, y))
            domaines[piece_id] = placements_valides
        return domaines

    def _detecter_ilot_mort(self, pieces_restantes: list[str]) -> bool:
        """
        Heuristique ad hoc d'élagage : parcourt les composantes connexes de cases vides (BFS).
        Retourne True s'il existe un îlot vide impossible à combler :
        - Taille strictement inférieure à la plus petite pièce restante (min 3 billes).
        - Taille exactement égale à 3, 4 ou 5 alors qu'aucune pièce de cette taille n'est disponible.
        """
        if not pieces_restantes:
            return False

        # Récuperation de la taille du plus petit ilot vide
        ilots_vides = self.plateau.get_ilots_vides()
        tailles_ilots_vides = [len(ilot) for ilot in ilots_vides]
        smallest_ilot = min(tailles_ilots_vides, default=0)

        # Récuperation de la taille des pieces restantes
        tailles_dispo = []
        for piece_id in pieces_restantes:
            coords_list = PIECES[piece_id]["coords"]
            tailles_dispo.append(len(coords_list))

        # Récuperation de la taille minimale des pieces restantes
        taille_min = min(tailles_dispo)

        # Coupure immédiate si l'îlot est plus petit que la plus petite pièce disponible
        if smallest_ilot < taille_min:
            return True
        # Si l'îlot fait 3, 4 ou 5 cases, il ne peut être rempli que par une seule pièce
        if smallest_ilot < 5 and smallest_ilot not in tailles_dispo:
            return True

        return False

    def resoudre(self) -> tuple[bool, dict[str, Any]]:
        """
        Lance la résolution CSP par Backtracking et retourne (succès, métriques).
        """
        self.noeuds_explores = 0
        self.backtracks = 0
        debut = time.perf_counter()

        succes = self._backtrack(self.variables_X[:])

        self.temps_execution_ms = round((time.perf_counter() - debut) * 1000, 3)
        return succes, self.obtenir_metriques(succes)

    def _backtrack(self, pieces_restantes: list[str]) -> bool:
        """
        Boucle récursive de l'algorithme Test & Generate (Backtracking).
        """
        cible = self.plateau.premiere_case_vide
        
        # Condition d'arrêt : toutes les cases sont remplies (instanciation complète consistante)
        if cible is None:
            return True

        if not pieces_restantes:
            return False

        xc, yc = cible

        # On essaie d'instancier une pièce parmi les variables restantes
        for i, pid in enumerate(pieces_restantes):
            nouvelles_restantes = pieces_restantes[:i] + pieces_restantes[i + 1 :]
            
            for orientation in CATALOGUE[pid]:
                # Pour couvrir la case cible (xc, yc), l'une des billes (dx, dy)
                # de la pièce doit se superposer à (xc, yc) -> ancrage en (xc - dx, yc - dy)
                for dx, dy in orientation:
                    x0, y0 = xc - dx, yc - dy
                    self.noeuds_explores += 1

                    # Test de consistance (Contraintes C : unaire et binaire)
                    if self._peut_placer_strict(orientation, x0, y0):
                        self.plateau.poser_piece(pid, orientation, x0, y0, verrouillee=False)

                        # Filtrage ad hoc : vérification des îlots morts avant de descendre dans l'arbre
                        if not self.activer_ilots_morts or not self._detecter_ilot_mort(nouvelles_restantes):
                            if self._backtrack(nouvelles_restantes):
                                return True

                        # Retour arrière (Backtrack) : annulation de l'instanciation
                        self.plateau.retirer_piece(pid)
                        self.backtracks += 1

        return False

    def obtenir_metriques(self, succes: bool) -> dict[str, Any]:
        """Retourne un dictionnaire récapitulatif des performances de la résolution."""
        return {
            "id_defi": self.defi.id_defi,
            "difficulte": self.defi.difficulte,
            "succes": succes,
            "variables_initiales": len(self.variables_X),
            "noeuds_explores": self.noeuds_explores,
            "backtracks": self.backtracks,
            "temps_ms": self.temps_execution_ms,
        }


# --- Fonction utilitaire directe pour main.py / benchmark.py ---

def resoudre_defi(id_defi: int | str, activer_ilots_morts: bool = True) -> tuple[bool, Plateau, dict[str, Any]]:
    """
    Instancie un objet Defi, l'envoie au SolverCSP et retourne :
    (succes, plateau_resolu, statistiques)
    """
    defi = Defi(id_defi)
    solveur = SolverCSP(defi, activer_ilots_morts=activer_ilots_morts)
    succes, stats = solveur.resoudre()
    return succes, defi.plateau, stats


# --- Test d'exécution ---
if __name__ == "__main__":
    # Test sur un défi Starter (#1), Expert (#25) et Wizard (#64)
    for num_defi in (1, 25, 64):
        print(f"================ DÉFI #{num_defi} ================")
        mon_defi = Defi(num_defi)
        print(f"Difficulté : {mon_defi.difficulte} | Variables X à placer ({len(mon_defi.variables_X)}) : {mon_defi.variables_X}")
        print("\nPlateau initial :")
        mon_defi.plateau.afficher()

        solveur = SolverCSP(mon_defi, activer_ilots_morts=True)
        trouve, metriques = solveur.resoudre()

        if trouve:
            valide = mon_defi.verifier_solution()
            print(f"Solution trouvée en {metriques['temps_ms']} ms "
                  f"({metriques['noeuds_explores']} nœuds, {metriques['backtracks']} backtracks) "
                  f"| Conforme au livret : {valide}")
            mon_defi.plateau.afficher()
        else:
            print("Aucune solution trouvée.")