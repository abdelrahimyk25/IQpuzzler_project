
#chaque pieces est representé par un nom, color, et les cordonnés des balls avec (x,y) : x for cols, y for rows

PIECES = { 
# A - Jaune (5 billes)
# . . ● . 
# ● ● ● ●
 "A" :{"nom" : "Jaune", "color" : "#F1C40F", "coords" : [(2,0),(0,1),(1,1),(2,1),(3,1)],},

# B - Orange (5 billes)
# . . ●
# ● ● ●
# . ● .
 "B":{"nom": "Orange","color":"#E67E22", "coords":[(2,0),(0,1),(1,1),(2,1),(1,2)]},

# C - Rouge vif (5 billes)
# ● ● ● ●
# . . . ●
 "C":{"nom": "Rouge", "color":"#E74C3C", "coords":[(0,0),(1,0),(2,0),(3,0),(3,1)]},

# D - Rouge bordeaux (4 billes)
# . ●
# ● ●
# ● .
  "D":{"nom":"Bordeaux","color":"#922B21","coords":[(1,0),(0,1),(1,1),(0,2)]},

# E - Rose (5 billes)
# ● .
# ● .
# ● ●
# . ●
  "E":{"nom" : "Rose","color": "#E84393", "coords":[(0,0),(0,1),(0,2),(1,2),(1,3)]},

# F - Violet foncé (5 billes)
# . . ●
# . ● ●
# ● ● .

 "F":{"nom" :"Violet","color":"#8E44AD","coords":[(2,0),(1,1),(2,1),(0,2),(1,2)]},

 # G - Bleu foncé (4 billes)
 # . ● ● ●
 # ● . . .
 "G":{"nom":"Bluef","color":"#1B1464","coords":[(1,0),(2,0),(3,0),(0,1)]},

 # H - Bleu cyan (5 billes en grand L)
 # . . ●
 # . . ●
 # ● ● ●

  "H":{"nom":"Cyan","color":"#00CEC9","coords":[(2,0),(2,1),(0,2),(1,2),(2,2)]},

 # I - Bleu ciel (3 billes en petit coin)
 # ● ●
 # . ●
  "I":{"nom":"ciel","color":"#74B9FF","coords":[(0,0),(1,0),(1,1)]},

 # J - Turquoise pâle (5 billes : anneau carré de 4 + 1 au-dessus)
 # ● .
 # ● ●
 # ● ●
  "J":{"nom":"Turquoise","color":"#55E6C1","coords":[(0,0),(0,1),(1,1),(0,2),(1,2)]},

 # K - Vert émeraude (4 billes en T)
 # ● ● ●
 # . ● .

   "K":{"nom":"Vertém","color":"#27AE60","coords":[(0,0),(1,0),(2,0),(1,1)]},

 # L - Vert pomme (5 billes en U vertical)
 # ● ●
 # . ●
 # ● ●

   "L":{"nom":"Vertpom","color":"#A8E6CF","coords":[(0,0),(1,0),(1,1),(0,2),(1,2)]},
}

#bibliothéque pour les couleurs des pieces 
Colorpieces = { 
    id_pieces : piece["color"]
    for id_pieces, piece in PIECES.items()
            }

#Fonction normaliser() pour eviter des coordonnés negatives au point de rotation or reflection
# le fait de normaliser est fait par une soustraction des coordonné par les x et y plus petit
def normaliser(piece):

    min_x = min(x for x,y in piece)

    min_y = min(y for x,y in piece)

    resultat = []

    for x,y in piece :
        new_x = x - min_x
        new_y = y - min_y
        resultat.append((new_x,new_y))

    return tuple(sorted(resultat)) #on utilise tuple et sorted pour eliminer des doublons ainsi que garder le meme ordre pour les boules


#Fonction pour la rotation des pieces
#le principe : un rotation de 90 deg est equivalent a : (x,y) -> (-y,x) + normaliser()

def rotation(piece):

    resultat = []
    for x,y in piece :
        new_y = x
        new_x = -y
        resultat.append((new_x,new_y))

    return normaliser(resultat)        


#fonction miroir : le principe est simple : (x,y) -> (-x,y)

def miroir(piece):
    resultat = []
    for x,y in piece :
        new_x = -x
        resultat.append((new_x,y))


    return normaliser(resultat)


#Fonction pour generer des orientations des pieces avec des rotations de 0,90,180,270 de la piece original et ça reflection

def generate_orientations(piece):
    listorientation = set() # pour eliminer des doublons

    for reflet in (False, True):
        if reflet :
            forme = miroir(piece)
        else:
            forme = normaliser(piece)

        for i in range(4):
            listorientation.add(forme)
            forme = rotation(forme)

    return sorted(listorientation)


#Fonction pour generer le catalogue de tout les orientations possible pour les 12 pieces


def generate_catalogue_orient():
    catalogue = {}

    for id_piece, piece in PIECES.items() :
        catalogue[id_piece] = generate_orientations(piece["coords"])

    return catalogue