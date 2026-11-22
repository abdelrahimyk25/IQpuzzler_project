from __future__ import annotations
import time
from collections import deque
from typing import Any

from Game_Element.pieces import PIECES
from CSP.defis import Defi


def construire_tailles_pieces() -> dict[str, int]:
    """Pré-calcule le nombre de billes de chaque pièce."""
    tailles: dict[str, int] = {}
    for lettre, infos in PIECES.items():
        tailles[lettre] = len(infos["coords"])
    return tailles


TAILLE_PIECES = construire_tailles_pieces()


class SolverCSP:
    """
    Moteur de résolution CSP ad hoc (Test & Generate / Backtracking)
    compatible 2D (Rectangle, Losange) et 3D (Pyramide) :
    - Consistance de nœud pré-calculée via le plateau
    - Ordre vertical : MRV (plus petit domaine) départagé par le degré maximum
    - Forward Checking : coupure immédiate si une case vide n'a plus de placement
    - Élagage ad hoc : détection des îlots morts via BFS et sommes de tailles réalisables
    """

    def __init__(self, defi: Defi, activer_ilots_morts: bool = True):
        self.defi = defi
        self.plateau = defi.plateau
        self.activer_ilots_morts = activer_ilots_morts
        self.degre_max = self.plateau.degre_max()

        # Ordre horizontal : grandes pièces rigides en priorité
        self.variables_X: list[str] = sorted(
            defi.pieces_libres,
            key=self._critere_tri_piece,
        )

        # Pré-calculs génériques (fonctionnent en 2D comme en 3D)
        self.cases_vides_initiales = self.plateau.lister_cases_vides()
        self.voisins_par_case = self._precalculer_voisins_vides()
        self.domaines_par_case = self._generer_domaines_initiaux()

        # Métriques de performance
        self.noeuds_explores: int = 0
        self.backtracks: int = 0
        self.temps_execution_ms: float = 0.0

    def _critere_tri_piece(self, lettre: str) -> tuple[int, int]:
        """
        Ordre horizontal des pièces :
        1. Taille décroissante (grandes pièces d'abord)
        2. Nombre d'orientations croissant (pièces les plus rigides d'abord)
        """
        taille_piece = TAILLE_PIECES[lettre]
        nb_orientations = self.plateau.nb_orientations(lettre)
        return (-taille_piece, nb_orientations)

    def _precalculer_voisins_vides(self) -> dict[Any, list[Any]]:
        """
        Pour chaque case vide initiale, liste ses voisins également vides.
        Accélère le calcul du degré et le BFS des îlots morts.
        """
        ensemble_vides = set(self.cases_vides_initiales)
        voisins_par_case = {}

        for case in self.cases_vides_initiales:
            voisins = []
            for voisin in self.plateau.obtenir_voisins(case):
                if voisin in ensemble_vides:
                    voisins.append(voisin)
            voisins_par_case[case] = voisins

        return voisins_par_case

    def _generer_domaines_initiaux(self) -> dict[Any, dict[str, list[tuple]]]:
        """
        Construit les domaines initiaux (consistance de nœud) regroupés
        par case vide puis par pièce. Chaque élément est un tuple de cases absolues.
        """
        domaines = {}
        for case in self.cases_vides_initiales:
            domaines[case] = {}
            for piece_id in self.variables_X:
                domaines[case][piece_id] = []

        for piece_id in self.variables_X:
            placements = self.plateau.generer_placements_valides(piece_id)
            for cases_absolues in placements:
                for case_couverte in cases_absolues:
                    if case_couverte in domaines:
                        domaines[case_couverte][piece_id].append(cases_absolues)

        return domaines

    def _compter_voisins_occupes(self, case: Any) -> int:
        """
        Compte le nombre de directions bloquées autour d'une case
        (bordures du plateau, cases interdites ou pièces déjà posées).
        """
        voisins_libres = 0
        for voisin in self.voisins_par_case[case]:
            if self.plateau.est_vide(voisin):
                voisins_libres += 1
        return self.degre_max - voisins_libres

    def _choisir_case_et_coups(
        self,
        pieces_restantes: set[str],
    ) -> list[tuple[str, tuple]] | None:
        """
        MRV (plus petit domaine) + Degré maximum + Forward Checking :
        - Retourne None si une case vide n'a aucun coup valide (impasse).
        - Retourne [] si toutes les cases sont remplies.
        - Sinon, retourne la liste des coups (piece_id, cases_absolues) de la meilleure case.
        """
        meilleurs_coups = []
        meilleur_score = None
        min_coups = None
        plateau_plein = True

        for case in self.cases_vides_initiales:
            if not self.plateau.est_vide(case):
                continue

            plateau_plein = False
            coups_valides = []
            depasse_minimum = False

            for piece_id in self.variables_X:
                if piece_id not in pieces_restantes:
                    continue

                for cases_absolues in self.domaines_par_case[case][piece_id]:
                    est_libre = True
                    for c in cases_absolues:
                        if not self.plateau.est_vide(c):
                            est_libre = False
                            break

                    if est_libre:
                        coups_valides.append((piece_id, cases_absolues))
                        if min_coups is not None and len(coups_valides) > min_coups:
                            depasse_minimum = True
                            break

                if depasse_minimum:
                    break

            nb_coups = len(coups_valides)

            # Forward Checking : aucune pièce ne peut couvrir cette case
            if nb_coups == 0:
                return None

            voisins_occupes = self._compter_voisins_occupes(case)
            score_case = (nb_coups, -voisins_occupes)

            if meilleur_score is None or score_case < meilleur_score:
                meilleur_score = score_case
                min_coups = nb_coups
                meilleurs_coups = coups_valides

        if plateau_plein:
            return []

        return meilleurs_coups

    def _mesurer_ilot_bfs(self, depart: Any, visitees: set[Any]) -> int:
        """Mesure la taille d'un îlot connexe de cases vides à partir de depart."""
        taille = 0
        file = deque([depart])
        visitees.add(depart)

        while file:
            courante = file.popleft()
            taille += 1
            for voisin in self.voisins_par_case[courante]:
                if voisin not in visitees and self.plateau.est_vide(voisin):
                    visitees.add(voisin)
                    file.append(voisin)

        return taille

    def _detecter_ilot_mort(self, pieces_restantes: set[str]) -> bool:
        """
        Élagage ad hoc : vérifie que chaque îlot vide peut être formé par une somme
        de tailles de pièces restantes, sans dépasser le quota de pièces de taille 3, 4 ou 5.
        """
        if not pieces_restantes:
            return False

        # Sommes de tailles réalisables avec les pièces restantes
        sommes_possibles = {0}
        nb_pieces_petites = {3: 0, 4: 0, 5: 0}

        for piece_id in pieces_restantes:
            taille_piece = TAILLE_PIECES[piece_id]
            if taille_piece in nb_pieces_petites:
                nb_pieces_petites[taille_piece] += 1

            nouvelles_sommes = set()
            for s in sommes_possibles:
                nouvelles_sommes.add(s + taille_piece)
            sommes_possibles = sommes_possibles | nouvelles_sommes

        # Parcours des îlots vides (arrêt immédiat dès qu'un îlot est impossible)
        visitees = set()
        nb_ilots_petits = {3: 0, 4: 0, 5: 0}

        for case in self.cases_vides_initiales:
            if case in visitees or not self.plateau.est_vide(case):
                continue

            taille_ilot = self._mesurer_ilot_bfs(case, visitees)

            if taille_ilot not in sommes_possibles:
                return True

            if taille_ilot in nb_ilots_petits:
                nb_ilots_petits[taille_ilot] += 1
                if nb_ilots_petits[taille_ilot] > nb_pieces_petites[taille_ilot]:
                    return True

        return False

    def resoudre(self) -> tuple[bool, dict[str, Any]]:
        """Lance la résolution CSP par Backtracking et retourne (succès, métriques)."""
        self.noeuds_explores = 0
        self.backtracks = 0
        debut = time.perf_counter()

        pieces_restantes = set(self.variables_X)
        succes = self._backtrack(pieces_restantes)

        self.temps_execution_ms = round((time.perf_counter() - debut) * 1000, 3)
        return succes, self.obtenir_metriques(succes)

    def _backtrack(self, pieces_restantes: set[str]) -> bool:
        """Boucle récursive de l'algorithme Test & Generate (Backtracking)."""
        self.noeuds_explores += 1

        coups_optimaux = self._choisir_case_et_coups(pieces_restantes)

        # Impasse détectée par Forward Checking
        if coups_optimaux is None:
            return False

        # Plateau entièrement rempli
        if len(coups_optimaux) == 0:
            return True

        if not pieces_restantes:
            return False

        for piece_id, cases_absolues in coups_optimaux:
            self.plateau.poser_cases(piece_id, cases_absolues, verrouillee=False)
            pieces_restantes.remove(piece_id)

            if not self.activer_ilots_morts or not self._detecter_ilot_mort(pieces_restantes):
                if self._backtrack(pieces_restantes):
                    return True

            # Retour arrière (Backtrack)
            pieces_restantes.add(piece_id)
            self.plateau.retirer_piece(piece_id)
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