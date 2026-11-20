from .pieces import PIECES
from itertools import permutations, product


def normaliser3D(forme):
    if not forme :
        # verifier que la piece n'est pas vide
        raise ValueError("une piéce de peut pas etre vide") 
    # trouver la plus petit valeur de chaque coordoné : mini_x, mini_y, mini_z
    mini = [min(point[i] for point in forme)for i in range(3)]
    #retourne ce tuple trié
    return tuple (sorted((x-mini[0],y-mini[1],z-mini[2]) for x,y,z in forme))

# verifie que la permutation est even ou odd , car le rearrangement des axes peut soit sortir une rotation valid ou une reflection donc faut
# faire la distinction
def _parite(perm):
    inversions = sum(perm[i] > perm[j] for i in range(3) for j in range (i+1,3))
    return (-1) ** inversions # ça retourne +1 pour une rotation et -1 pour une reflection


# fonction pour generer des orientations des pieces 3d
def generate_orientations3d(coords2d, autoriser_miroir=True):
    base = [(x,y,0) for x,y in coords2d] # convertir une piece 2d au 3d
    resultats = set()
    #si on peut avoir un reflextion on examine la piece original et ca reflection
    for miroir in ((False,True) if autoriser_miroir else (False,)):
        # si on un miroir, le cordoné de x devient -x , sinon il reste le meme
        points = [(-x if miroir else x,y,z) for x,y,z in base]
        # ça generer des permutation de les axes de coordonné car une pieces dans XY peut etre orienté ver XZ ou YZ
        for perm in permutations(range(3)):
            # ça genere tout les combinations des signes pour les trois coordonnés : 3 coords donc 2^3 = 8 combinations possible
            for signes in product((-1,1), repeat=3):

                # pour filterer des transformations
                if _parite(perm) * signes[0] * signes[1] * signes[2] != 1:
                    continue
                resultat = [tuple(signes[i] * p[perm[i]] for i in range(3)) for p in points]
                resultats.add(normaliser3D(resultat))

    return sorted(resultats)



def generer_catalogue3d(autoriser_miroir = True):
    return {identifiant: generate_orientations3d(data['coords'], autoriser_miroir)
            for identifiant, data in PIECES.items()}




CATALOGUE_3D = generer_catalogue3d()