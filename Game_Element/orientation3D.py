from .pieces import CATALOGUE

# Les 3 plans orthogonaux valides dans la pyramide 3D :
# 1 plan horizontal + 2 plans verticaux diagonaux (pièces inclinées à 45°)
PLANS_PYRAMIDE = (
    ((1, 0, 0), (0, 1, 0)),       # Horizontal (même étage z)
    ((0, 0, 1), (-1, -1, 1)),     # Diagonal vertical 1
    ((-1, 0, 1), (0, -1, 1)),     # Diagonal vertical 2
)


def normaliser3D(forme):
    if not forme:
        raise ValueError("Une pièce ne peut pas être vide")
    mini_x = min(p[0] for p in forme)
    mini_y = min(p[1] for p in forme)
    mini_z = min(p[2] for p in forme)
    return tuple(sorted((x - mini_x, y - mini_y, z - mini_z) for x, y, z in forme))


def generate_orientations3d(orientations_2d):
    resultats = set()
    for (ux, uy, uz), (vx, vy, vz) in PLANS_PYRAMIDE:
        for forme_2d in orientations_2d:
            forme_3d = []
            for x, y in forme_2d:
                forme_3d.append((x * ux + y * vx, x * uy + y * vy, x * uz + y * vz))
            resultats.add(normaliser3D(forme_3d))
    return sorted(resultats)


def generer_catalogue3d():
    catalogue = {}
    for identifiant, orientations_2d in CATALOGUE.items():
        catalogue[identifiant] = generate_orientations3d(orientations_2d)
    return catalogue


CATALOGUE_3D = generer_catalogue3d()