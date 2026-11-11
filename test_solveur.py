"""
Tests du solveur CSP (python -m unittest test_solveur -v).
"""

import unittest

from csp import CATALOGUE, SolveurCSP, generer_domaine, contrainte_binaire, Defi
from defis import DEFI_TEST_3_MANQUANTES
from pieces import PIECES
from plateau import Plateau


class TestCatalogue(unittest.TestCase):
    def test_nombre_orientations_uniques(self):
        attendu = {"A": 8, "B": 8, "C": 8, "D": 4, "E": 8, "F": 4,
                   "G": 8, "H": 4, "I": 4, "J": 8, "K": 4, "L": 4}
        self.assertEqual({l: len(o) for l, o in CATALOGUE.items()}, attendu)

    def test_total_billes(self):
        self.assertEqual(sum(len(p["coords"]) for p in PIECES.values()), 55)


class TestContraintes(unittest.TestCase):
    def test_unaire_domaine_dans_le_plateau(self):
        for lettre in PIECES:
            for p in generer_domaine(lettre):
                self.assertTrue(all(0 <= x <= 10 and 0 <= y <= 4 for x, y in p.cases))

    def test_binaire_chevauchement(self):
        dom = generer_domaine("I")
        a, b = dom[0], dom[0]
        self.assertFalse(contrainte_binaire(a, b))

    def test_ilots_vides(self):
        p = Plateau()
        # On isole la case (0, 0) en remplissant (1, 0) et (0, 1).
        p.plateau[(1, 0)] = "X"
        p.plateau[(0, 1)] = "X"
        self.assertIn(1, p.tailles_ilots_vides())


class TestSolveur(unittest.TestCase):
    def test_defi_unique_solution(self):
        solveur = SolveurCSP(DEFI_TEST_3_MANQUANTES)
        self.assertEqual(sorted(solveur.variables), ["A", "B", "C"])
        solutions = solveur.resoudre(max_solutions=2)
        self.assertEqual(len(solutions), 1)
        pl = solveur.plateau_avec_solution(solutions[0])
        self.assertIsNone(pl.premiere_case_vide())
        # Chaque pièce occupe exactement le bon nombre de cases
        for lettre in PIECES:
            n = sum(1 for v in pl.plateau.values() if v == lettre)
            self.assertEqual(n, len(PIECES[lettre]["coords"]), lettre)

    def test_elagage_ne_change_pas_la_solution(self):
        avec = SolveurCSP(DEFI_TEST_3_MANQUANTES, elagage_ilots=True)
        sans = SolveurCSP(DEFI_TEST_3_MANQUANTES, elagage_ilots=False)
        s1, s2 = avec.resoudre(2), sans.resoudre(2)
        self.assertEqual([{l: p.cases for l, p in s.items()} for s in s1],
                         [{l: p.cases for l, p in s.items()} for s in s2])
        self.assertLessEqual(avec.stats["noeuds"], sans.stats["noeuds"])

    def test_defi_invalide(self):
        with self.assertRaises(ValueError):
            Defi(1, {"I": [(0, 0), (1, 0), (2, 0)]}).valider()  # I est un coude, pas une ligne


if __name__ == "__main__":
    unittest.main()
