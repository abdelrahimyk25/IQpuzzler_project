"""
visualiseur_3d.py - Visualiseur interactif 3D pour la Pyramide IQ-Puzzler Pro XXL.
Technologies : Pygame + PyOpenGL (sphères 3D avec ombrage et lumière).

Contrôles :
- Clic gauche + glisser la souris : Faire pivoter la pyramide à 360°
- Molette de la souris : Zoomer / Dézoomer
- Touche ESPACE : Basculer entre Défi (pièces imposées) et Solution complète
- Flèches GAUCHE / DROITE : Changer de défi (129 à 188)
- ÉCHAP : Quitter
"""

import json
import math
import sys
from pathlib import Path

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Palette de couleurs officielles SmartGames (normalisées entre 0.0 et 1.0 pour OpenGL)
COULEURS_RGB = {
    "A": (255 / 255, 222 / 255,   0 / 255),  # Jaune
    "B": (241 / 255, 145 / 255,   0 / 255),  # Orange
    "C": (228 / 255,   6 / 255,  21 / 255),  # Rouge vif
    "D": (181 / 255,  31 / 255,  32 / 255),  # Bordeaux
    "E": (236 / 255, 111 / 255, 169 / 255),  # Rose
    "F": (132 / 255,  30 / 255, 130 / 255),  # Violet
    "G": (  1 / 255,  92 / 255, 171 / 255),  # Bleu foncé
    "H": (  0 / 255, 159 / 255, 225 / 255),  # Bleu cyan
    "I": (163 / 255, 219 / 255, 246 / 255),  # Bleu ciel
    "J": (140 / 255, 202 / 255, 191 / 255),  # Turquoise
    "K": (  0 / 255, 142 / 255,  94 / 255),  # Vert émeraude
    "L": (152 / 255, 192 / 255,  34 / 255),  # Vert pomme
    ".": (220 / 255, 220 / 255, 220 / 255),  # Emplacement vide (gris très clair translucide)
}

FICHIER_DEFIS = Path(__file__).parent / "defis.json"


def charger_donnees():
    if not FICHIER_DEFIS.is_file():
        raise FileNotFoundError(f"Fichier {FICHIER_DEFIS} introuvable.")
    with open(FICHIER_DEFIS, "r", encoding="utf-8") as f:
        return json.load(f)


def coordonnees_spatiales(x: int, y: int, z: int) -> tuple[float, float, float]:
    """
    Convertit la coordonnée de grille discrète (x, y, z) en position spatiale continue (X, Y, Z).
    Empilement compact de sphères :
    - Étage z décalé de z * 0.5 vers le centre
    - Altitude verticale = z * sqrt(2)/2 * rayon_bille
    """
    PAS_BILLE = 1.0
    HAUTEUR_ETAGE = PAS_BILLE * (math.sqrt(2.0) / 2.0)

    # Centrage autour de l'origine (0, 0, 0)
    # À la base (z=0), x et y vont de 0 à 4 (centre à 2.0)
    X = (x + 0.5 * z - 2.0) * PAS_BILLE
    Y = (z - 2.0) * HAUTEUR_ETAGE
    Z = (y + 0.5 * z - 2.0) * PAS_BILLE

    return X, Y, Z


def dessiner_sphere(x: float, y: float, z: float, rayon: float, couleur: tuple[float, float, float], alpha: float = 1.0):
    """Dessine une sphère 3D avec éclairage à la position spatiale donnée."""
    glPushMatrix()
    glTranslatef(x, y, z)

    # Matériau et couleur
    mat_color = list(couleur) + [alpha]
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, mat_color)
    glMaterialfv(GL_FRONT, GL_SPECULAR, (0.8, 0.8, 0.8, alpha))
    glMaterialf(GL_FRONT, GL_SHININESS, 50.0)

    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, rayon, 24, 24)
    gluDeleteQuadric(quad)

    glPopMatrix()


def configurer_opengl(largeur: int, hauteur: int):
    """Initialise le contexte 3D, la perspective et les lumières."""
    glViewport(0, 0, largeur, hauteur)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(largeur) / float(hauteur), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Activation des tampons de profondeur (Z-buffer) et de l'éclairage
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    # Position de la source de lumière (en haut à droite, légèrement devant)
    glLightfv(GL_LIGHT0, GL_POSITION, (5.0, 10.0, 8.0, 1.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.35, 0.35, 0.35, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.85, 0.85, 0.85, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))

    # Transparence pour les billes vides
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Fond gris foncé doux
    glClearColor(0.12, 0.14, 0.18, 1.0)


def main():
    pygame.init()
    largeur, hauteur = 1000, 750
    pygame.display.set_mode((largeur, hauteur), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("IQ-Puzzler Pro XXL - Visualiseur 3D Pyramide")

    configurer_opengl(largeur, hauteur)
    tous_defis = charger_donnees()

    id_defi_actuel = 129
    mode_solution = False  # False = Défi imposé, True = Solution complète

    # Paramètres de caméra
    rot_x = 25.0
    rot_y = -35.0
    zoom = -9.0
    clic_en_cours = False
    dernier_x, dernier_y = 0, 0

    horloge = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_SPACE:
                    mode_solution = not mode_solution
                elif event.key == K_RIGHT:
                    if id_defi_actuel < 188:
                        id_defi_actuel += 1
                elif event.key == K_LEFT:
                    if id_defi_actuel > 129:
                        id_defi_actuel -= 1

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    clic_en_cours = True
                    dernier_x, dernier_y = event.pos
                elif event.button == 4:  # Molette vers le haut (Zoom avant)
                    zoom += 0.5
                elif event.button == 5:  # Molette vers le bas (Zoom arrière)
                    zoom -= 0.5

            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    clic_en_cours = False

            elif event.type == MOUSEMOTION:
                if clic_en_cours:
                    dx = event.pos[0] - dernier_x
                    dy = event.pos[1] - dernier_y
                    rot_y += dx * 0.4
                    rot_x += dy * 0.4
                    dernier_x, dernier_y = event.pos

        # Effacer l'écran
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Matrice caméra
        glLoadIdentity()
        glTranslatef(0.0, 0.0, zoom)
        glRotatef(rot_x, 1.0, 0.0, 0.0)
        glRotatef(rot_y, 0.0, 1.0, 0.0)

        # Préparation des billes de la pyramide
        defi = tous_defis[str(id_defi_actuel)]
        billes: dict[tuple[int, int, int], str] = {}

        if mode_solution:
            # Affichage de la solution officielle complète
            for z, niveau in enumerate(defi["solution_grille"]):
                for y, ligne in enumerate(niveau):
                    for x, piece_id in enumerate(ligne.split()):
                        billes[(x, y, z)] = piece_id
        else:
            # Affichage du défi initial (pièces imposées)
            for z in range(5):
                taille = 5 - z
                for y in range(taille):
                    for x in range(taille):
                        billes[(x, y, z)] = "."

            for p in defi["pieces_initiales"]:
                for x, y, z in p["positions"]:
                    billes[(x, y, z)] = p["id"]

        # Dessin des 55 billes
        for (x, y, z), piece_id in billes.items():
            spat_x, spat_y, spat_z = coordonnees_spatiales(x, y, z)
            if piece_id == ".":
                # Emplacement vide : petite sphère translucide
                dessiner_sphere(spat_x, spat_y, spat_z, rayon=0.25, couleur=COULEURS_RGB["."], alpha=0.35)
            else:
                couleur = COULEURS_RGB.get(piece_id, (1.0, 1.0, 1.0))
                # Vraie bille colorée
                dessiner_sphere(spat_x, spat_y, spat_z, rayon=0.46, couleur=couleur, alpha=1.0)

        # Mise à jour du titre avec le mode et les touches
        titre_mode = "SOLUTION OFFICIELLE" if mode_solution else "DÉFI EN COURS"
        pygame.display.set_caption(
            f"Pyramide 3D - Défi #{id_defi_actuel} ({defi['difficulte']}) [{titre_mode}] - ESPACE pour basculer, Souris pour tourner"
        )

        pygame.display.flip()
        horloge.tick(60)


if __name__ == "__main__":
    main()
