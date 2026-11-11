import sys
import pygame
from menu_principal import afficher_menu_principal
from selection_mode import afficher_selection_mode
from modes.mode_2d_orthogonal.difficulte.difficulte_2d_orthogonal import afficher_difficulte_2d_orthogonal
from modes.mode_2d_diagonal.difficulte.difficulte_2d_diagonal import afficher_difficulte_2d_diagonal
from modes.mode_3d_pyramidal.difficulte.difficulte_3d_pyramidal import afficher_difficulte_3d_pyramidal

from modes.mode_2d_orthogonal.grilles.starter_orthogonal import afficher_grilles_starter_2d_orthogonal

# 1. Initialisation globale
pygame.init()
LARGEUR, HAUTEUR = 800, 600
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR), pygame.RESIZABLE)
pygame.display.set_caption("Mon Projet Jeu")

# 2. État initial au lancement
etat_actuel = "menu"

# 3. Boucle centrale d'orchestration
while etat_actuel != "quitter":

  for event in pygame.event.get(pygame.VIDEORESIZE):
    fenetre = pygame.display.set_mode(
        (event.w, event.h), pygame.RESIZABLE
  )

  if etat_actuel == "menu":
    # On passe le contrôle au menu principal
    etat_actuel = afficher_menu_principal(fenetre)

  elif etat_actuel == "selection_mode":
    # On passe le contrôle à la sélection du mode
    etat_actuel = afficher_selection_mode(fenetre)

  elif etat_actuel == "difficulte_2d_orthogonal":
      # On passe le contrôle à la sélection du mode
      print("choix_difficulte_2d_orthogonal")
      etat_actuel = afficher_difficulte_2d_orthogonal(fenetre)

  elif etat_actuel == "difficulte_2d_diagonal":
        # On passe le contrôle à la sélection du mode
        print("choix_difficulte_2d_diagonal")
        etat_actuel = afficher_difficulte_2d_diagonal(fenetre)

  elif etat_actuel == "difficulte_3d_pyramidal":
        # On passe le contrôle à la sélection du mode
        print("difficulte_3d_pyramidal")
        etat_actuel = afficher_difficulte_3d_pyramidal(fenetre)

  elif etat_actuel == "starter_orthogonal":
          # On passe le contrôle à la sélection du mode
          print("starter_orthogonal")
          etat_actuel = afficher_grilles_starter_2d_orthogonal(fenetre)

  elif etat_actuel == "jeu":
    # Exemple pour plus tard : etat_actuel = lancer_jeu(fenetre)
    pass

# 4. Nettoyage de fin
pygame.quit()
sys.exit()