"""
benchmark.py - Banc d'essai et statistiques de performance du solveur (IQ Puzzler Pro).
Rôle : Membre 3 (Banque de défis, Tests & Benchmark).

Fonctionnalités :
- Exécute les défis du mode RECTANGLE (1 à 64).
- Trie par difficulté : Starter, Junior, Expert, Master, Wizard.
- Calcule et affiche les moyennes (temps de calcul, nœuds explorés, taux de succès).
"""

from __future__ import annotations
import builtins
import json
import time
from pathlib import Path

# Neutralisation de l'éventuel exit() lors de l'import de defis.py
_vrai_exit = builtins.exit
builtins.exit = lambda *a: None
try:
    import defis
    from pieces import PIECES
    from plateau import Plateau
    from solver import SolverCSP
finally:
    builtins.exit = _vrai_exit

FICHIER_DEFIS = Path(__file__).parent / "defis.json"
DIFFICULTES = ["Starter", "Junior", "Expert", "Master", "Wizard"]


def preparer_defi(id_defi: int):
    """Charge le défi et initialise le plateau officiel pour le solveur."""
    defi = defis.Defi(id_defi)
    defi.id_defi = int(defi.id)
    plateau = Plateau()
    poses = set()

    for p in defi.pieces_fixes:
        forme = [tuple(c) for c in p["forme"]]
        plateau.poser_piece(p["id"], forme, p["x"], p["y"], verrouillee=True)
        poses.add(p["id"])

    defi.plateau = plateau
    defi.pieces_libres = sorted(set(PIECES.keys()) - poses)
    return defi


def executer_benchmark():
    """Lance le solveur sur tous les défis Rectangle et calcule les moyennes par difficulté."""
    with open(FICHIER_DEFIS, "r", encoding="utf-8") as f:
        tous_defis = json.load(f)

    # 1. Regroupement des défis Rectangle par difficulté
    groupes = {d: [] for d in DIFFICULTES}
    for did, data in tous_defis.items():
        if data.get("mode") == "rectangle":
            diff = data.get("difficulte", "Starter").capitalize()
            if diff in groupes:
                groupes[diff].append(int(did))

    stats_diff = {}

    print("=" * 68)
    print("   BANC D'ESSAI AUTOMATISÉ - MODE RECTANGLE (IQ-PUZZLER PRO)")
    print("=" * 68)

    # 2. Exécution niveau par niveau
    for diff in DIFFICULTES:
        ids = sorted(groupes[diff])
        if not ids:
            continue

        print(f"\n▶ [{diff.upper()}] ({len(ids)} défis)")
        print("-" * 68)

        temps_liste = []
        noeuds_liste = []
        succes_count = 0

        for did in ids:
            try:
                defi = preparer_defi(did)
                t0 = time.perf_counter()
                solver = SolverCSP(defi)
                ok, metriques = solver.resoudre()
                t_ms = (time.perf_counter() - t0) * 1000.0
                noeuds = metriques.get("noeuds_explores", 0)
            except Exception:
                ok, t_ms, noeuds = False, 0.0, 0

            if ok:
                succes_count += 1
                temps_liste.append(t_ms)
                noeuds_liste.append(noeuds)
                symbole = "✅ SUCCÈS"
            else:
                symbole = "❌ ÉCHEC "

            print(f"  Défi #{did:03d} | {symbole} | Temps: {t_ms:6.2f} ms | Nœuds: {noeuds:5d}")

        # Calcul des moyennes pour la difficulté
        nb_ok = len(temps_liste)
        stats_diff[diff] = {
            "total": len(ids),
            "succes": succes_count,
            "taux": (succes_count / len(ids)) * 100.0,
            "tps_moyen": sum(temps_liste) / nb_ok if nb_ok else 0.0,
            "noeuds_moyen": sum(noeuds_liste) / nb_ok if nb_ok else 0.0,
        }

    # 3. Tableau de synthèse final
    print("\n" + "=" * 68)
    print("           SYNTHÈSE DES MOYENNES PAR DIFFICULTÉ")
    print("=" * 68)
    print(f"{'Difficulté':<12} | {'Succès':<10} | {'Taux':<8} | {'Temps moyen':<13} | {'Nœuds moy.'}")
    print("-" * 68)

    for diff, s in stats_diff.items():
        print(
            f"{diff:<12} | {s['succes']:>2d}/{s['total']:<2d}      | "
            f"{s['taux']:>5.1f} % | {s['tps_moyen']:>8.2f} ms    | {s['noeuds_moyen']:>8.1f}"
        )
    print("=" * 68)


if __name__ == "__main__":
    executer_benchmark()
