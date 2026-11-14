"""Extraction automatisee et validation mathematique des 188 defis et solutions
du livret SmartGames IQ Puzzler Pro XXL vers defis.json.

Sources PDF :
- Pages  4..19  (defis   1..64)  & pages 52..67 (solutions   1..64) : mode "rectangle" (11x5 = 55)
- Pages 20..35  (defis  65..128) & pages 68..83 (solutions  65..128) : mode "losange"   (grille orthogonale 9x9, 55 cases)
- Pages 36..50  (defis 129..188) & pages 84..98 (solutions 129..188) : mode "pyramide"  (5 niveaux 5x5..1x1 = 55)
"""

from __future__ import annotations

import io
import json
import math
import re
import sys
from pathlib import Path

PDF_PATH = (
    PROJECT_ROOT
    / "Aide PDF"
    / "SmartGames_IQ_Puzzler_Pro_XXL_IQ_Puzzler_Pro_XXL_-_Livret_de_défis (1) (1).pdf"
)
JSON_PATH = PROJECT_ROOT / "CSP" / "defis.json"

import pymupdf as fitz
from PIL import Image

PROJECT_ROOT = Path(__file__).parent
PDF_PATH = (
    PROJECT_ROOT
    / "SmartGames_IQ_Puzzler_Pro_XXL_IQ_Puzzler_Pro_XXL_-_Livret_de_défis_(1)_(1).pdf"
)
JSON_PATH = PROJECT_ROOT / "defis.json"

# Palette RGB exacte des 12 pieces officielles (A..L)
PALETTE: dict[str, tuple[int, int, int]] = {
    "A": (255, 222, 0),    # Jaune (5)
    "B": (241, 145, 0),    # Orange (5)
    "C": (228, 6, 21),     # Rouge vif (5)
    "D": (181, 31, 32),    # Bordeaux (4)
    "E": (236, 111, 169),  # Rose (5)
    "F": (132, 30, 130),   # Violet (5)
    "G": (1, 92, 171),     # Bleu fonce (4)
    "H": (0, 159, 225),    # Bleu cyan (5)
    "I": (163, 219, 246),  # Bleu ciel (3)
    "J": (140, 202, 191),  # Turquoise (5)
    "K": (0, 142, 94),     # Vert emeraude (4)
    "L": (152, 192, 34),   # Vert pomme (5)
}

EMPTY_RGB = {
    "rectangle": (87, 81, 83),
    "losange": (227, 227, 227),
    "pyramide": (255, 255, 255),
}

# Formes de reference exactes (G corrigee par rapport a la coquille de main.py)
BASE_PIECES: dict[str, list[tuple[int, int]]] = {
    "A": [(0, 1), (1, 1), (2, 1), (3, 1), (2, 0)],
    "B": [(2, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    "C": [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)],
    "D": [(1, 0), (0, 1), (1, 1), (0, 2)],
    "E": [(0, 0), (0, 1), (0, 2), (1, 2), (1, 3)],
    "F": [(2, 0), (1, 1), (2, 1), (0, 2), (1, 2)],
    "G": [(0, 0), (1, 0), (2, 0), (0, 1)],
    "H": [(2, 0), (2, 1), (0, 2), (1, 2), (2, 2)],
    "I": [(0, 0), (1, 0), (1, 1)],
    "J": [(0, 0), (0, 1), (1, 1), (0, 2), (1, 2)],
    "K": [(0, 0), (1, 0), (2, 0), (1, 1)],
    "L": [(0, 0), (1, 0), (1, 1), (0, 2), (1, 2)],
}

# Cellules visuelles du plateau losange : (ligne_visuelle, colonnes_paires/impaires)
LOSANGE_CELLS: list[tuple[int, list[int]]] = [
    (0, [3, 7, 11]),
    (1, [2, 4, 6, 8, 10, 12]),
    (2, [1, 3, 5, 7, 9, 11, 13]),
    (3, [0, 2, 4, 6, 8, 10, 12, 14]),
    (4, [1, 3, 5, 7, 9, 11, 13]),
    (5, [0, 2, 4, 6, 8, 10, 12, 14]),
    (6, [1, 3, 5, 7, 9, 11, 13]),
    (7, [2, 4, 6, 8, 10, 12]),
    (8, [3, 7, 11]),
]

# Geometrie perspective de la pyramide par niveau z (0=base 5x5 .. 4=sommet 1x1)
PYRAMIDE_GEOM: dict[int, list[tuple[float, float]]] = {
    4: [(0.0, 0.0)],
    3: [(70.5, 34.0), (93.0, 36.0)],
    2: [(139.0, 33.3), (162.5, 35.8), (186.5, 37.9)],
    1: [(230.0, 34.2), (252.0, 36.2), (275.0, 37.6), (300.0, 39.7)],
    0: [(345.0, 34.1), (368.0, 36.0), (391.0, 37.6), (416.5, 39.7), (444.5, 41.9)],
}


def normalize_2d(pts: list[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
    mx = min(x for x, _ in pts)
    my = min(y for _, y in pts)
    return tuple(sorted((x - mx, y - my) for x, y in pts))


def all_2d_orientations(pts: list[tuple[int, int]]) -> set[tuple[tuple[int, int], ...]]:
    orientations: set[tuple[tuple[int, int], ...]] = set()
    for mirror in (False, True):
        cur = [(-x if mirror else x, y) for x, y in pts]
        for _ in range(4):
            orientations.add(normalize_2d(cur))
            cur = [(-y, x) for x, y in cur]
    return orientations


VALID_SHAPES_2D = {k: all_2d_orientations(v) for k, v in BASE_PIECES.items()}

# Orientations 3D valides sur reseau FCC (horizontal + plans inclines a 45 degres)
_FCC_STEPS = [
    (2, 0, 0), (-2, 0, 0), (0, 2, 0), (0, -2, 0),
    (1, 1, 1), (1, -1, 1), (-1, 1, 1), (-1, -1, 1),
    (1, 1, -1), (1, -1, -1), (-1, 1, -1), (-1, -1, -1),
]
_FCC_BASES = [
    (e1, e2)
    for e1 in _FCC_STEPS
    for e2 in _FCC_STEPS
    if e1[0] * e2[0] + e1[1] * e2[1] + 2 * e1[2] * e2[2] == 0
]


def _all_3d_orientations(pts2d: list[tuple[int, int]]) -> set[tuple[tuple[int, int, int], ...]]:
    signatures: set[tuple[tuple[int, int, int], ...]] = set()
    for shape2d in all_2d_orientations(pts2d):
        for e1, e2 in _FCC_BASES:
            placed = [
                (p * e1[0] + q * e2[0], p * e1[1] + q * e2[1], p * e1[2] + q * e2[2])
                for p, q in shape2d
            ]
            ax, ay, az = min(placed)
            signatures.add(tuple(sorted((x - ax, y - ay, z - az) for x, y, z in placed)))
    return signatures


VALID_SHAPES_3D = {k: _all_3d_orientations(v) for k, v in BASE_PIECES.items()}


def signature_3d(xyz_list: list[tuple[int, int, int]]) -> tuple[tuple[int, int, int], ...]:
    fcc = sorted((2 * x + z, 2 * y + z, z) for x, y, z in xyz_list)
    ax, ay, az = min(fcc)
    return tuple(sorted((fx - ax, fy - ay, fz - az) for fx, fy, fz in fcc))


def load_page_pixels(doc: fitz.Document, page_1based: int):
    page = doc[page_1based - 1]
    images = page.get_images(full=True)
    if not images:
        raise RuntimeError(f"Aucune image trouvee sur la page {page_1based}")
    xref = images[0][0]
    img_bytes = doc.extract_image(xref)["image"]
    return Image.open(io.BytesIO(img_bytes)).convert("RGB").load()


def extract_difficulty(doc: fitz.Document, page_1based: int) -> str:
    compact = re.sub(r"\s+", "", doc[page_1based - 1].get_text("text").upper())
    for level in ("STARTER", "JUNIOR", "EXPERT", "MASTER", "WIZARD"):
        if level in compact:
            return level.capitalize()
    raise RuntimeError(f"Difficulte introuvable sur la page {page_1based}")


def median_rgb(px, cx: int, cy: int, rad: int = 2) -> tuple[int, int, int]:
    rs, gs, bs = [], [], []
    for dy in range(-rad, rad + 1):
        for dx in range(-rad, rad + 1):
            r, g, b = px[cx + dx, cy + dy]
            rs.append(r)
            gs.append(g)
            bs.append(b)
    rs.sort()
    gs.sort()
    bs.sort()
    mid = len(rs) // 2
    return (rs[mid], gs[mid], bs[mid])


def classify_rgb(
    r: int, g: int, b: int, empty_rgb: tuple[int, int, int] | None = None
) -> tuple[str, float]:
    best_k, best_d2 = "", 10**9
    for k, (pr, pg, pb) in PALETTE.items():
        d2 = (r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2
        if d2 < best_d2:
            best_d2 = d2
            best_k = k
    if empty_rgb is not None:
        er, eg, eb = empty_rgb
        de2 = (r - er) ** 2 + (g - eg) ** 2 + (b - eb) ** 2
        if de2 < best_d2:
            return ".", math.sqrt(de2)
    return best_k, math.sqrt(best_d2)


def find_rectangle_boxes(px) -> list[tuple[int, int, int, int]]:
    quads = [
        (40, 515, 70, 380),
        (520, 1000, 70, 380),
        (40, 515, 380, 670),
        (520, 1000, 380, 670),
    ]
    boxes = []
    for qx0, qx1, qy0, qy1 in quads:
        ys = [
            y
            for y in range(qy0, qy1)
            if sum(1 for x in range(qx0, qx1) if sum(px[x, y]) < 75) > 250
        ]
        xs = [
            x
            for x in range(qx0, qx1)
            if sum(1 for y in range(qy0, qy1) if sum(px[x, y]) < 75) > 120
        ]
        if not ys or not xs:
            raise RuntimeError(f"Cadre rectangle introuvable dans quadrant {(qx0, qx1, qy0, qy1)}")
        boxes.append((min(xs), min(ys), max(xs), max(ys)))
    return boxes


def read_rectangle_board(
    px, box: tuple[int, int, int, int], empty_rgb: tuple[int, int, int] | None
) -> tuple[dict[tuple[int, int], str], float]:
    x0, y0, x1, y1 = box
    cells: dict[tuple[int, int], str] = {}
    max_d = 0.0
    for y in range(5):
        cy = int(y0 + 14 + (y + 0.5) * (y1 - y0 - 28) / 5.0)
        for x in range(11):
            cx = int(x0 + 14 + (x + 0.5) * (x1 - x0 - 28) / 11.0)
            k, d = classify_rgb(*median_rgb(px, cx, cy), empty_rgb=empty_rgb)
            max_d = max(max_d, d)
            cells[(x, y)] = k
    return cells, max_d


def find_losange_boxes(px) -> list[tuple[int, int, int, int]]:
    quads = [
        (55, 502, 70, 385),
        (530, 980, 70, 385),
        (55, 502, 385, 680),
        (530, 980, 385, 680),
    ]
    boxes = []
    for qx0, qx1, qy0, qy1 in quads:
        ys = [
            y
            for y in range(qy0, qy1)
            if sum(
                1
                for x in range(qx0 + 40, qx1 - 40)
                if abs(px[x, y][0] - px[x, y][1]) < 15 and 100 <= px[x, y][0] <= 175
            )
            > 250
        ]
        if not ys:
            raise RuntimeError(f"Cadre losange introuvable dans quadrant {(qx0, qx1, qy0, qy1)}")
        top_y = min(ys)
        boxes.append((qx0 + 4, top_y, qx1 - 4, top_y + 256))
    return boxes


def read_losange_board(
    px, box: tuple[int, int, int, int], empty_rgb: tuple[int, int, int] | None
) -> tuple[dict[tuple[int, int], str], float]:
    x0, y0, _, _ = box
    cells: dict[tuple[int, int], str] = {}
    max_d = 0.0
    for r, cols in LOSANGE_CELLS:
        cy = round(y0 + 19 + r * 27.125)
        for c in cols:
            cx = round((x0 + 37) + c * 26.0)
            k, d = classify_rgb(*median_rgb(px, cx, cy), empty_rgb=empty_rgb)
            max_d = max(max_d, d)
            u = (c + r - 3) // 2
            v = (r - c + 11) // 2
            cells[(u, v)] = k
    return cells, max_d


def find_pyramid_tops(px) -> list[tuple[float, float]]:
    tops = []
    for x0 in (90, 330, 570, 810):
        pts = [
            (x, y)
            for y in range(135, 205)
            for x in range(x0, x0 + 160)
            if max(px[x, y]) < 95
        ]
        if not pts:
            raise RuntimeError(f"Sommet pyramide introuvable dans colonne x={x0}")
        ys_sorted = sorted({y for _, y in pts})
        max_top_y = ys_sorted[0]
        prev_y = ys_sorted[0]
        for y in ys_sorted[1:]:
            if y - prev_y >= 6:
                break
            max_top_y = y
            prev_y = y
        top_pts = [(x, y) for x, y in pts if y <= max_top_y]
        cx = (min(x for x, _ in top_pts) + max(x for x, _ in top_pts)) / 2.0
        cy = (min(y for _, y in top_pts) + max(y for _, y in top_pts)) / 2.0
        tops.append((cx, cy))
    return tops


def read_pyramid_board(
    px, top_cx: float, top_cy: float, empty_rgb: tuple[int, int, int] | None
) -> tuple[dict[tuple[int, int, int], str], float]:
    cells: dict[tuple[int, int, int], str] = {}
    max_d = 0.0
    for z, rows in PYRAMIDE_GEOM.items():
        n = 5 - z
        for r, (dy, step_x) in enumerate(rows):
            cy = round(top_cy + dy)
            for c in range(n):
                cx = round(top_cx + (c - (n - 1) / 2.0) * step_x)
                k, d = classify_rgb(*median_rgb(px, cx, cy), empty_rgb=empty_rgb)
                max_d = max(max_d, d)
                cells[(c, r, z)] = k
    return cells, max_d


def build_2d_pieces_list(cells: dict[tuple[int, int], str]) -> list[dict]:
    by_id: dict[str, list[tuple[int, int]]] = {}
    for (x, y), k in cells.items():
        if k != ".":
            by_id.setdefault(k, []).append((x, y))
    pieces = []
    for k in sorted(by_id):
        pts = by_id[k]
        mx = min(x for x, _ in pts)
        my = min(y for _, y in pts)
        forme = [[x - mx, y - my] for x, y in sorted(pts)]
        pieces.append({"id": k, "x": mx, "y": my, "forme": forme})
    return pieces


def validate_2d_pair(
    defi_id: int,
    scells: dict[tuple[int, int], str],
    ccells: dict[tuple[int, int], str],
) -> None:
    if len(scells) != 55 or len(ccells) != 55:
        raise ValueError(f"Defi {defi_id}: nombre de cases invalide ({len(scells)}, {len(ccells)})")

    s_by_id: dict[str, list[tuple[int, int]]] = {k: [] for k in BASE_PIECES}
    for xy, k in scells.items():
        if k not in BASE_PIECES:
            raise ValueError(f"Defi {defi_id} solution: piece invalide {k!r} en {xy}")
        s_by_id[k].append(xy)

    for k, pts in s_by_id.items():
        if len(pts) != len(BASE_PIECES[k]):
            raise ValueError(f"Defi {defi_id} solution {k}: taille {len(pts)} != {len(BASE_PIECES[k])}")
        if normalize_2d(pts) not in VALID_SHAPES_2D[k]:
            raise ValueError(f"Defi {defi_id} solution {k}: forme invalide {pts}")

    c_by_id: dict[str, list[tuple[int, int]]] = {}
    for xy, ck in ccells.items():
        if ck != ".":
            if scells[xy] != ck:
                raise ValueError(f"Defi {defi_id}: discordance en {xy} (defi={ck}, sol={scells[xy]})")
            c_by_id.setdefault(ck, []).append(xy)

    for k, pts in c_by_id.items():
        if len(pts) != len(BASE_PIECES[k]):
            raise ValueError(f"Defi {defi_id} initial {k}: piece incomplete ({len(pts)})")


def validate_3d_pair(
    defi_id: int,
    scells: dict[tuple[int, int, int], str],
    ccells: dict[tuple[int, int, int], str],
) -> None:
    if len(scells) != 55 or len(ccells) != 55:
        raise ValueError(f"Defi {defi_id}: nombre de cases 3D invalide ({len(scells)}, {len(ccells)})")

    s_by_id: dict[str, list[tuple[int, int, int]]] = {k: [] for k in BASE_PIECES}
    for xyz, k in scells.items():
        if k not in BASE_PIECES:
            raise ValueError(f"Defi {defi_id} solution 3D: piece invalide {k!r} en {xyz}")
        s_by_id[k].append(xyz)

    for k, xyzs in s_by_id.items():
        if len(xyzs) != len(BASE_PIECES[k]):
            raise ValueError(f"Defi {defi_id} solution 3D {k}: taille {len(xyzs)} != {len(BASE_PIECES[k])}")
        if signature_3d(xyzs) not in VALID_SHAPES_3D[k]:
            raise ValueError(f"Defi {defi_id} solution 3D {k}: forme 3D invalide {xyzs}")

    c_by_id: dict[str, list[tuple[int, int, int]]] = {}
    for xyz, ck in ccells.items():
        if ck != ".":
            if scells[xyz] != ck:
                raise ValueError(f"Defi {defi_id}: discordance 3D en {xyz} (defi={ck}, sol={scells[xyz]})")
            c_by_id.setdefault(ck, []).append(xyz)

    for k, xyzs in c_by_id.items():
        if len(xyzs) != len(BASE_PIECES[k]):
            raise ValueError(f"Defi {defi_id} initial 3D {k}: piece incomplete ({len(xyzs)})")


def extract_all() -> dict[str, dict]:
    if not PDF_PATH.is_file():
        print(f"ERREUR: PDF introuvable: {PDF_PATH}")
        sys.exit(1)

    doc = fitz.open(str(PDF_PATH))
    result: dict[str, dict] = {}
    stats = {"rectangle": 0.0, "losange": 0.0, "pyramide": 0.0}

    # 1. Mode rectangle : defis 1..64 (pp. 4..19, sol pp. 52..67)
    for idx in range(16):
        ch_pg, sol_pg = 4 + idx, 52 + idx
        difficulte = extract_difficulty(doc, ch_pg)
        px_ch = load_page_pixels(doc, ch_pg)
        px_sol = load_page_pixels(doc, sol_pg)
        b_ch = find_rectangle_boxes(px_ch)
        b_sol = find_rectangle_boxes(px_sol)
        for q in range(4):
            defi_id = 1 + idx * 4 + q
            scells, sd = read_rectangle_board(px_sol, b_sol[q], None)
            ccells, cd = read_rectangle_board(px_ch, b_ch[q], EMPTY_RGB["rectangle"])
            stats["rectangle"] = max(stats["rectangle"], sd, cd)
            validate_2d_pair(defi_id, scells, ccells)
            solution_grille = [
                " ".join(scells[(x, y)] for x in range(11))
                for y in range(5)
            ]
            result[str(defi_id)] = {
                "mode": "rectangle",
                "difficulte": difficulte,
                "pieces_initiales": build_2d_pieces_list(ccells),
                "solution_grille": solution_grille,
            }

    # 2. Mode losange : defis 65..128 (pp. 20..35, sol pp. 68..83)
    for idx in range(16):
        ch_pg, sol_pg = 20 + idx, 68 + idx
        difficulte = extract_difficulty(doc, ch_pg)
        px_ch = load_page_pixels(doc, ch_pg)
        px_sol = load_page_pixels(doc, sol_pg)
        b_ch = find_losange_boxes(px_ch)
        b_sol = find_losange_boxes(px_sol)
        for q in range(4):
            defi_id = 65 + idx * 4 + q
            scells, sd = read_losange_board(px_sol, b_sol[q], None)
            ccells, cd = read_losange_board(px_ch, b_ch[q], EMPTY_RGB["losange"])
            stats["losange"] = max(stats["losange"], sd, cd)
            validate_2d_pair(defi_id, scells, ccells)
            solution_grille = [
                " ".join(scells.get((u, v), ".") for u in range(9))
                for v in range(9)
            ]
            result[str(defi_id)] = {
                "mode": "losange",
                "difficulte": difficulte,
                "pieces_initiales": build_2d_pieces_list(ccells),
                "solution_grille": solution_grille,
            }

    # 3. Mode pyramide : defis 129..188 (pp. 36..50, sol pp. 84..98)
    for idx in range(15):
        ch_pg, sol_pg = 36 + idx, 84 + idx
        difficulte = extract_difficulty(doc, ch_pg)
        px_ch = load_page_pixels(doc, ch_pg)
        px_sol = load_page_pixels(doc, sol_pg)
        t_ch = find_pyramid_tops(px_ch)
        t_sol = find_pyramid_tops(px_sol)
        for q in range(4):
            defi_id = 129 + idx * 4 + q
            scells, sd = read_pyramid_board(px_sol, *t_sol[q], None)
            ccells, cd = read_pyramid_board(px_ch, *t_ch[q], EMPTY_RGB["pyramide"])
            stats["pyramide"] = max(stats["pyramide"], sd, cd)
            validate_3d_pair(defi_id, scells, ccells)

            by_id: dict[str, list[list[int]]] = {}
            for (x, y, z), k in sorted(ccells.items(), key=lambda item: (item[0][2], item[0][1], item[0][0])):
                if k != ".":
                    by_id.setdefault(k, []).append([x, y, z])
            pieces_init = [
                {"id": k, "positions": by_id[k]}
                for k in sorted(by_id)
            ]
            solution_grille = [
                [
                    " ".join(scells[(x, y, z)] for x in range(5 - z))
                    for y in range(5 - z)
                ]
                for z in range(5)
            ]
            result[str(defi_id)] = {
                "mode": "pyramide",
                "difficulte": difficulte,
                "pieces_initiales": pieces_init,
                "solution_grille": solution_grille,
            }

    doc.close()
    print(
        f"Extraction et validation reussies: {len(result)}/188 defis | "
        f"ecart RGB max = { {k: round(v, 2) for k, v in stats.items()} }"
    )
    return result


def _format_list_block(items: list, indent: str = "    ") -> list[str]:
    """Formate une liste JSON avec un element compact par ligne."""
    if not items:
        return ["[]"]
    lines = ["["]
    for idx, item in enumerate(items):
        comma = "," if idx < len(items) - 1 else ""
        lines.append(f"{indent}  {json.dumps(item, ensure_ascii=False)}{comma}")
    lines.append(f"{indent}]")
    return lines


def format_defis_json(defis: dict[str, dict]) -> str:
    """Genere un JSON lisible : une ligne par piece initiale et une ligne par rangee/niveau."""
    out = ["{"]
    keys = list(defis.keys())
    for k_idx, defi_id in enumerate(keys):
        entry = defis[defi_id]
        pieces_lines = _format_list_block(entry["pieces_initiales"])
        sol_lines = _format_list_block(entry["solution_grille"])

        out.append(f'  {json.dumps(defi_id)}: {{')
        out.append(f'    "mode": {json.dumps(entry["mode"], ensure_ascii=False)},')
        out.append(f'    "difficulte": {json.dumps(entry["difficulte"], ensure_ascii=False)},')
        if len(pieces_lines) == 1:
            out.append(f'    "pieces_initiales": {pieces_lines[0]},')
        else:
            out.append(f'    "pieces_initiales": {pieces_lines[0]}')
            out.extend(pieces_lines[1:-1])
            out.append(f'{pieces_lines[-1]},')
        out.append(f'    "solution_grille": {sol_lines[0]}')
        out.extend(sol_lines[1:])
        trailing = "," if k_idx < len(keys) - 1 else ""
        out.append(f"  }}{trailing}")
    out.append("}")
    return "\n".join(out) + "\n"


def main() -> None:
    defis = extract_all()
    JSON_PATH.write_text(format_defis_json(defis), encoding="utf-8")
    print(f"Fichier ecrit : {JSON_PATH}")


if __name__ == "__main__":
    main()
