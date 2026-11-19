import sys
import pygame
from menu_principal import afficher_menu_principal
from selection_mode import afficher_selection_mode
from modes.mode_2d_orthogonal.difficulte.difficulte_2d_orthogonal import afficher_difficulte_2d_orthogonal
from modes.mode_2d_diagonal.difficulte.difficulte_2d_diagonal import afficher_difficulte_2d_diagonal
from modes.mode_3d_pyramidal.difficulte.difficulte_3d_pyramidal import afficher_difficulte_3d_pyramidal

from modes.mode_2d_orthogonal.grilles.starter_orthogonal import afficher_grilles_starter_2d_orthogonal
from modes.mode_2d_orthogonal.grilles.junior_orthogonal import afficher_grilles_junior_2d_orthogonal
from modes.mode_2d_orthogonal.grilles.expert_orthogonal import afficher_grilles_expert_2d_orthogonal
from modes.mode_2d_orthogonal.grilles.master_orthogonal import afficher_grilles_master_2d_orthogonal
from modes.mode_2d_orthogonal.grilles.wizard_orthogonal import afficher_grilles_wizard_2d_orthogonal

from modes.mode_3d_pyramidal.grilles.starter_pyramidal import afficher_grilles_starter_3d_pyramidal
from modes.mode_3d_pyramidal.grilles.junior_pyramidal import afficher_grilles_junior_3d_pyramidal
from modes.mode_3d_pyramidal.grilles.expert_pyramidal import afficher_grilles_expert_3d_pyramidal
from modes.mode_3d_pyramidal.grilles.master_pyramidal import afficher_grilles_master_3d_pyramidal
from modes.mode_3d_pyramidal.grilles.wizard_pyramidal import afficher_grilles_wizard_3d_pyramidal

from modes.mode_2d_diagonal.grilles.starter_diagonal import afficher_grilles_starter_2d_diagonal
from modes.mode_2d_diagonal.grilles.junior_diagonal import afficher_grilles_junior_2d_diagonal
from modes.mode_2d_diagonal.grilles.expert_diagonal import afficher_grilles_expert_2d_diagonal
from modes.mode_2d_diagonal.grilles.master_diagonal import afficher_grilles_master_2d_diagonal
from modes.mode_2d_diagonal.grilles.wizard_diagonal import afficher_grilles_wizard_2d_diagonal

from modes.mode_2d_orthogonal.jeu_2d_orthogonal import afficher_plateau_2d_orthogonal
from modes.mode_2d_diagonal.jeu_2d_diagonal import afficher_plateau_2d_diagonal

# 1. Initialisation globale
pygame.init()
LARGEUR, HAUTEUR = 800, 600
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR), pygame.RESIZABLE)
pygame.display.set_caption("IQ PUZZLER PRO XXL")

liste_plateau_orth = [

["D", "D", "E", "E", "E", "G", "G", "L", "L", None, None],
["K", "D", "D", "C", "E", "E", "G", "L", None, None, None],
["K", "K", "F", "C", None, None, "G", "L", "L",  None, None],
["K", "F", "F", "C", None,None,None,None,None,None,None],
["F", "F", "C", "C", None,None,None,None,None,None,None]

]

liste_plateau_diag = [
    ["#", "#", "#", "#", "A", "A", "A", "A", "#"],
    ["#", "#", "#", "#", "E", "E", "A", "J", "J"],
    ["#", "#", "E", "E", "E", "C", "J", "J", "J"],
    ["#", "#", "D", "D", "K", "C", "C", "C", "C"],
    ["I", "D", "D", "K", "K", "K", "H", "H", "H"],
    ["I", "I", "B", "G", "G", "G", "H", "#", "#"],
    ["F", "B", "B", "L", "L", "G", "H", "#", "#"],
    ["F", "F", "B", "B", "L", "#", "#", "#", "#"],
    ["#", "F", "F", "L", "L", "#", "#", "#", "#"],
]

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
    #etat_actuel = afficher_plateau_2d_diagonal(fenetre, liste_plateau_diag)##------------------a modifier

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

  elif etat_actuel == "junior_orthogonal":
            # On passe le contrôle à la sélection du mode
            print("junior_orthogonal")
            etat_actuel = afficher_grilles_junior_2d_orthogonal(fenetre)

  elif etat_actuel == "expert_orthogonal":
              # On passe le contrôle à la sélection du mode
              print("expert_orthogonal")
              etat_actuel = afficher_grilles_expert_2d_orthogonal(fenetre)

  elif etat_actuel == "master_orthogonal":
                # On passe le contrôle à la sélection du mode
                print("master_orthogonal")
                etat_actuel = afficher_grilles_master_2d_orthogonal(fenetre)

  elif etat_actuel == "wizard_orthogonal":
                  # On passe le contrôle à la sélection du mode
                  print("wizard_orthogonal")
                  etat_actuel = afficher_grilles_wizard_2d_orthogonal(fenetre)

  elif etat_actuel == "starter_diagonal":
            # On passe le contrôle à la sélection du mode
            print("starter_diagonal")
            etat_actuel = afficher_grilles_starter_2d_diagonal(fenetre)
  
  elif etat_actuel == "junior_diagonal":
            # On passe le contrôle à la sélection du mode
            print("junior_diagonal")
            etat_actuel = afficher_grilles_junior_2d_diagonal(fenetre)

  elif etat_actuel == "expert_diagonal":
              # On passe le contrôle à la sélection du mode
              print("expert_diagonal")
              etat_actuel = afficher_grilles_expert_2d_diagonal(fenetre)

  elif etat_actuel == "master_diagonal":
                # On passe le contrôle à la sélection du mode
                print("master_diagonal")
                etat_actuel = afficher_grilles_master_2d_diagonal(fenetre)

  elif etat_actuel == "wizard_diagonal":
                  # On passe le contrôle à la sélection du mode
                  print("wizard_diagonal")
                  etat_actuel = afficher_grilles_wizard_2d_diagonal(fenetre)

  elif etat_actuel == "starter_pyramidal":
              # On passe le contrôle à la sélection du mode
              print("starter_pyramidal")
              etat_actuel = afficher_grilles_starter_3d_pyramidal(fenetre)
    
  elif etat_actuel == "junior_pyramidal":
            # On passe le contrôle à la sélection du mode
            print("junior_pyramidal")
            etat_actuel = afficher_grilles_junior_3d_pyramidal(fenetre)

  elif etat_actuel == "expert_pyramidal":
              # On passe le contrôle à la sélection du mode
              print("expert_pyramidal")
              etat_actuel = afficher_grilles_expert_3d_pyramidal(fenetre)

  elif etat_actuel == "master_pyramidal":
                # On passe le contrôle à la sélection du mode
                print("master_pyramidal")
                etat_actuel = afficher_grilles_master_3d_pyramidal(fenetre)

  elif etat_actuel == "wizard_pyramidal":
                  # On passe le contrôle à la sélection du mode
                  print("wizard_pyramidal")
                  etat_actuel = afficher_grilles_wizard_3d_pyramidal(fenetre)

  elif etat_actuel == "jeu_2d_orthogonal":
                    # On passe le contrôle à la sélection du mode
                    print("afichage plateau")
                    etat_actuel = afficher_plateau_2d_orthogonal(fenetre, liste_plateau_orth)

  elif etat_actuel == "jeu_2d_diagonal":
                      # On passe le contrôle à la sélection du mode
                      print("afichage plateau")
                      etat_actuel = afficher_plateau_2d_diagonal(fenetre, liste_plateau_diag)

  elif etat_actuel == "jeu":
    # Exemple pour plus tard : etat_actuel = lancer_jeu(fenetre)
    pass

# 4. Nettoyage de fin
pygame.quit()
sys.exit()