"""
benchmark.py - Banc d'essai et statistiques de performance du solveur (IQ Puzzler Pro).
Rôle : Membre 3 (Banque de défis, Tests & Benchmark).

Fonctionnalités :
- Exécute et évalue le solveur sur les modes RECTANGLE (1-64) ou LOSANGE (65-128).
- Trie par niveau de difficulté : Starter, Junior, Expert, Master, Wizard.
- Calcule et affiche les moyennes (temps de calcul, nœuds explorés, taux de succès).
"""

from __future__ import annotations
import argparse
import json
import time
from pathlib import Path

from defis import Defi
from solver import SolverCSP

FICHIER_DEFIS = Path(__file__).parent / "defis.json"
DIFFICULTES = ["Starter", "Junior", "Expert", "Master", "Wizard"]


def executer_benchmark(mode_cible: str = "losange"):
    """Lance le solveur sur tous les défis du mode choisi et calcule les moyennes par difficulté."""
    with open(FICHIER_DEFIS, "r", encoding="utf-8") as f:
        tous_defis = json.load(f)

    # 1. Regroupement des défis du mode par difficulté
    groupes = {d: [] for d in DIFFICULTES}
    for did, data in tous_defis.items():
        if data.get("mode") == mode_cible:
            diff = data.get("difficulte", "Starter").capitalize()
            if diff in groupes:
                groupes[diff].append(int(did))

    stats_diff = {}

    print("=" * 68)
    print(f"   BANC D'ESSAI AUTOMATISÉ - MODE {mode_cible.upper()} (IQ-PUZZLER PRO)")
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
                # Defi instancie directement le bon plateau (Plateau ou PlateauLosange)
                defi = Defi(did)
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

            print(f"  Défi #{did:03d} | {symbole} | Temps: {t_ms:7.2f} ms | Nœuds: {noeuds:6d}")

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
    print(f"       SYNTHÈSE DES MOYENNES PAR DIFFICULTÉ ({mode_cible.upper()})")
    print("=" * 68)
    print(f"{'Difficulté':<12} | {'Succès':<10} | {'Taux':<8} | {'Temps moyen':<13} | {'Nœuds moy.'}")
    print("-" * 68)

    for diff, s in stats_diff.items():
        print(
            f"{diff:<12} | {s['succes']:>2d}/{s['total']:<2d}      | "
            f"{s['taux']:>5.1f} % | {s['tps_moyen']:>8.2f} ms    | {s['noeuds_moyen']:>9.1f}"
        )
    print("=" * 68)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark IQ-Puzzler Pro")
    parser.add_argument("--mode", choices=["rectangle", "losange"], default="losange", help="Mode de jeu à tester")
    args = parser.parse_args()

    executer_benchmark(mode_cible=args.mode)
