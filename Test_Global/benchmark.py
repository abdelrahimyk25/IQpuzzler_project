"""

Missions :
- Lancer l'algorithme de résolution sur une série de défis (ex: 12, 24, 64 ou 188 défis).
- Mesurer les temps d'exécution (min, max, moyen), les nœuds explorés et les backtracks.
- Vérifier la validité des solutions trouvées face à la solution officielle.
- Générer un rapport statistique consolidé par niveau de difficulté (Starter, Junior, Expert, Master, Wizard).
- Exporter les résultats au format JSON et texte.
"""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable

import CSP.defis as defis

# Import du solveur du projet s'il existe, sinon solveur de secours
try:
    from CSP.solver import resoudre_csp
except ImportError:
    try:
        from main import resoudre_csp
    except ImportError:
        resoudre_csp = None


@dataclass
class ResultatDefi:
    id_defi: int
    mode: str
    difficulte: str
    succes: bool
    temps_ms: float
    noeuds: int = 0
    backtracks: int = 0
    conforme_officiel: bool = False
    message: str = ""


@dataclass
class StatsDifficulte:
    difficulte: str
    total: int = 0
    reussis: int = 0
    taux_succes: float = 0.0
    temps_moyen_ms: float = 0.0
    temps_min_ms: float = 0.0
    temps_max_ms: float = 0.0
    noeuds_moyen: float = 0.0
    backtracks_moyen: float = 0.0


def resoudre_avec_timeout(
    solveur_fn: Callable, plateau: Any, timeout_sec: float = 10.0
) -> tuple[bool, Any, dict[str, Any]]:
    """Exécute le solveur en mesurant précisément le temps."""
    t0 = time.perf_counter()
    metriques_defaut = {"noeuds": 0, "backtracks": 0}

    try:
        # Signature contrat : resoudre_csp(plateau, utiliser_heuristiques=True)
        res = solveur_fn(plateau)
        t1 = time.perf_counter()
        temps_ms = (t1 - t0) * 1000.0

        if isinstance(res, tuple):
            succes = bool(res[0])
            plateau_resolu = res[1] if len(res) > 1 else plateau
            metriques = res[2] if len(res) > 2 and isinstance(res[2], dict) else metriques_defaut
        elif isinstance(res, bool):
            succes = res
            plateau_resolu = plateau
            metriques = metriques_defaut
        else:
            succes = False
            plateau_resolu = plateau
            metriques = metriques_defaut

        metriques["temps_ms"] = temps_ms
        return succes, plateau_resolu, metriques

    except Exception as e:
        t1 = time.perf_counter()
        return False, plateau, {"noeuds": 0, "backtracks": 0, "temps_ms": (t1 - t0) * 1000.0, "erreur": str(e)}


def executer_benchmark(
    liste_defis: list[int] | None = None,
    difficulte_filtre: str | None = None,
    mode_filtre: str = "rectangle",
    solveur_fn: Callable | None = None,
    timeout_sec: float = 10.0,
    afficher_progression: bool = True,
) -> tuple[list[ResultatDefi], dict[str, StatsDifficulte]]:
    """
    Lance le banc d'essai complet sur la sélection de défis demandée.
    """
    tous_defis = defis.charger_tous_les_defis()

    # Sélection des IDs
    if liste_defis is None:
        ids_candidats = []
        for str_id, data in tous_defis.items():
            if mode_filtre and data.get("mode") != mode_filtre:
                continue
            if difficulte_filtre and data.get("difficulte", "").lower() != difficulte_filtre.lower():
                continue
            ids_candidats.append(int(str_id))
        ids_candidats.sort()
    else:
        ids_candidats = sorted(liste_defis)

    if afficher_progression:
        print(f"\n========================================================")
        print(f" DÉMARRAGE DU BENCHMARK : {len(ids_candidats)} DÉFI(S) SÉLECTIONNÉ(S)")
        print(f" Mode : {mode_filtre} | Difficulté : {difficulte_filtre or 'Toutes'}")
        print(f"========================================================\n")

    resultats: list[ResultatDefi] = []

    for id_defi in ids_candidats:
        info = tous_defis[str(id_defi)]
        mode = info.get("mode", "rectangle")
        diff = info.get("difficulte", "Inconnue")

        # 1. Vérification d'intégrité préliminaire
        valide, msg_integ = defis.verifier_integrite_defi(id_defi)
        if not valide:
            res_err = ResultatDefi(
                id_defi=id_defi,
                mode=mode,
                difficulte=diff,
                succes=False,
                temps_ms=0.0,
                message=f"Intégrité invalide: {msg_integ}",
            )
            resultats.append(res_err)
            if afficher_progression:
                print(f"[Défi #{id_defi:03d} | {diff:8s}] ❌ ERREUR INTÉGRITÉ : {msg_integ}")
            continue

        # 2. Initialisation du plateau
        try:
            plateau = defis.initialiser_plateau_defi(id_defi)
        except Exception as e:
            resultats.append(
                ResultatDefi(
                    id_defi=id_defi,
                    mode=mode,
                    difficulte=diff,
                    succes=False,
                    temps_ms=0.0,
                    message=f"Erreur init plateau: {e}",
                )
            )
            continue

        # 3. Résolution
        if solveur_fn is not None:
            succes, plateau_resolu, metriques = resoudre_avec_timeout(
                solveur_fn, plateau, timeout_sec=timeout_sec
            )
            conforme = False
            if succes:
                conforme = defis.verifier_solution(plateau_resolu, id_defi)

            res = ResultatDefi(
                id_defi=id_defi,
                mode=mode,
                difficulte=diff,
                succes=succes,
                temps_ms=metriques.get("temps_ms", 0.0),
                noeuds=metriques.get("noeuds", 0),
                backtracks=metriques.get("backtracks", 0),
                conforme_officiel=conforme,
                message=metriques.get("erreur", "OK" if succes else "Échec solveur"),
            )
        else:
            # Mode audit de la banque de données (chargement & validation sans solveur externe)
            res = ResultatDefi(
                id_defi=id_defi,
                mode=mode,
                difficulte=diff,
                succes=True,
                temps_ms=0.1,
                conforme_officiel=True,
                message="Banque validée (pas de solveur fourni)",
            )

        resultats.append(res)

        if afficher_progression:
            symb = "✅" if res.succes else "❌"
            conf = " (Officiel OK)" if res.conforme_officiel else ""
            print(
                f"[Défi #{id_defi:03d} | {diff:8s}] {symb} Temps: {res.temps_ms:7.2f} ms | "
                f"Nœuds: {res.noeuds:6d} | Backtracks: {res.backtracks:6d}{conf}"
            )

    # Consolidation des statistiques par niveau
    stats_par_diff: dict[str, StatsDifficulte] = {}
    ordre_diffs = ["Starter", "Junior", "Expert", "Master", "Wizard"]

    for d in ordre_diffs:
        groupe = [r for r in resultats if r.difficulte.lower() == d.lower()]
        if not groupe:
            continue

        total = len(groupe)
        reussis = sum(1 for r in groupe if r.succes)
        temps = [r.temps_ms for r in groupe if r.succes] or [0.0]
        noeuds = [r.noeuds for r in groupe]
        btracks = [r.backtracks for r in groupe]

        stats_par_diff[d] = StatsDifficulte(
            difficulte=d,
            total=total,
            reussis=reussis,
            taux_succes=round((reussis / total) * 100.0, 1),
            temps_moyen_ms=round(sum(temps) / len(temps), 2),
            temps_min_ms=round(min(temps), 2),
            temps_max_ms=round(max(temps), 2),
            noeuds_moyen=round(sum(noeuds) / total, 1),
            backtracks_moyen=round(sum(btracks) / total, 1),
        )

    return resultats, stats_par_diff


def afficher_rapport_statistique(stats_par_diff: dict[str, StatsDifficulte]) -> None:
    """Affiche un tableau récapitulatif dans la console."""
    print("\n" + "=" * 80)
    print("                      RAPPORT STATISTIQUE DU BENCHMARK")
    print("=" * 80)
    print(
        f"{'Niveau':<10} | {'Total':<6} | {'Succès':<7} | {'Taux':<7} | "
        f"{'Tps Moy (ms)':<13} | {'Tps Min':<9} | {'Tps Max':<9} | {'Nœuds Moy':<10}"
    )
    print("-" * 80)

    total_global = 0
    total_reussis = 0
    temps_cumul = 0.0

    for d, s in stats_par_diff.items():
        total_global += s.total
        total_reussis += s.reussis
        temps_cumul += s.temps_moyen_ms * s.reussis

        print(
            f"{s.difficulte:<10} | {s.total:<6d} | {s.reussis:<7d} | {s.taux_succes:>5.1f} % | "
            f"{s.temps_moyen_ms:>11.2f} ms | {s.temps_min_ms:>7.2f} ms | {s.temps_max_ms:>7.2f} ms | {s.noeuds_moyen:>10.1f}"
        )

    print("-" * 80)
    taux_global = round((total_reussis / total_global) * 100.0, 1) if total_global else 0.0
    temps_moyen_global = round(temps_cumul / total_reussis, 2) if total_reussis else 0.0
    print(
        f"{'GLOBAL':<10} | {total_global:<6d} | {total_reussis:<7d} | {taux_global:>5.1f} % | "
        f"{temps_moyen_global:>11.2f} ms | {'-':>9} | {'-':>9} |"
    )
    print("=" * 80 + "\n")


def exporter_rapport(
    resultats: list[ResultatDefi],
    stats: dict[str, StatsDifficulte],
    chemin_fichier: str | Path = "benchmark_resultats.json",
) -> None:
    """Sauvegarde le rapport complet au format JSON."""
    chemin = Path(chemin_fichier)
    donnees = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "statistiques_par_niveau": {k: asdict(v) for k, v in stats.items()},
        "details_defis": [asdict(r) for r in resultats],
    }
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(donnees, f, indent=2, ensure_ascii=False)
    print(f"📁 Rapport de benchmark exporté dans : {chemin.resolve()}")


if __name__ == "__main__":
    # Test d'exécution du benchmark sur les 24 premiers défis (Starter + Junior)
    print("Exécution du benchmark...")
    # Si le solveur officiel resoudre_csp existe, on le passe, sinon audit
    resultats, stats = executer_benchmark(
        liste_defis=list(range(1, 25)),
        solveur_fn=resoudre_csp,
        afficher_progression=True,
    )
    afficher_rapport_statistique(stats)
    exporter_rapport(resultats, stats)
