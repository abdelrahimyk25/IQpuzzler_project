import sys
import pygame

from ui import Image, Boule

# 1. Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS_CLAIR = (200, 200, 200)
BLEU = (50, 150, 250)
ROUGE = (255, 0, 0)


def afficher_plateau_3d_pyramidal(fenetre, liste_plateau):
    horloge = pygame.time.Clock()

    # Polices
    police_titre = pygame.font.Font(None, 48)
    police_bouton = pygame.font.Font(None, 32)
    police_info = pygame.font.Font(None, 24)

    # image plateau
    plateau = Image(0, 0, 216, 471, "IQpuzzler_project/interface/src/assets/plateau_3d_pyramidal.png")

    
    
    
    
    
    #coordonnées:

    """
    
    """

   

    #couleurs:

    couleurs = {
        "A" : (252,222,23),
        "B" : (240,144,11),
        "C" : (225,10,25),
        "D" : (181,30,33),
        "E" : (234,112,166),
        "F" : (129,33,128),
        "G" : (23,94,169),
        "H" : (25,157,218),
        "I" : (163,215,240),
        "J" : (140,201,190),
        "K" : (18,142,94),
        "L" : (151,191,34)
    }

    #Boules:

    boules = {}

    
    A = (252,222,23)
    B = (240,144,11)
    C = (225,10,25)
    D = (181,30,33)
    E = (234,112,166)
    F = (129,33,128)
    G = (23,94,169)
    H = (25,157,218)
    I = (163,215,240)
    J = (140,201,190)
    K = (18,142,94)
    L = (151,191,34)

    #coordonnées:

    coord = {



    }
    

    
    

    
    #Création et ancrage de la boule directement sur la surface du plateau

    #ETAGE 0:------------------------------------------------------------------------------------------
    
    #ligne 1--------------------------
    boule1 = Boule(46, 343, A)
    boule1.dessiner(plateau.image_base)

    boule2 = Boule(59, 75, B)
    boule2.dessiner(plateau.image_base)

    boule3 = Boule(50, 115, C)
    boule3.dessiner(plateau.image_base)

    boule4 = Boule(61, 156, D)
    boule4.dessiner(plateau.image_base)

    boule5 = Boule(48, 75, E)
    boule5.dessiner(plateau.image_base)
    """
    #ligne 2--------------------------
    boule6 = Boule(499, 115, F)
    boule6.dessiner(plateau.image_base)

    boule7 = Boule(540, 156, G)
    boule7.dessiner(plateau.image_base)

    boule8 = Boule(581, 196, H)
    boule8.dessiner(plateau.image_base)

    boule9 = Boule(621, 236, I)
    boule9.dessiner(plateau.image_base)

    boule10 = Boule(336, 34, J)
    boule10.dessiner(plateau.image_base)

    #ligne 3---------------------------
    boule11 = Boule(377, 75, K)
    boule11.dessiner(plateau.image_base)
    
    boule12 = Boule(417, 115, L)
    boule12.dessiner(plateau.image_base)

    boule13 = Boule(458, 156, A)
    boule13.dessiner(plateau.image_base)

    boule14 = Boule(499, 196, B)
    boule14.dessiner(plateau.image_base)

    boule15 = Boule(540, 236, C)
    boule15.dessiner(plateau.image_base)

    #ligne 4---------------------------
    boule16 = Boule(580, 277, D)
    boule16.dessiner(plateau.image_base)

    boule17 = Boule(296, 75, C)
    boule17.dessiner(plateau.image_base)

    boule18 = Boule(336, 115, D)
    boule18.dessiner(plateau.image_base)

    boule19 = Boule(377, 156, E)
    boule19.dessiner(plateau.image_base)

    boule20 = Boule(417, 196, F)
    boule20.dessiner(plateau.image_base)

    #ligne 5---------------------------
    boule21 = Boule(458, 236, G)
    boule21.dessiner(plateau.image_base)

    boule22 = Boule(499, 277, H)
    boule22.dessiner(plateau.image_base)

    boule23 = Boule(540, 318, I)
    boule23.dessiner(plateau.image_base)

    boule24 = Boule(174, 34, J)
    boule24.dessiner(plateau.image_base)

    boule25 = Boule(214, 75, K)
    boule25.dessiner(plateau.image_base)

    #ETAGE 1:-------------------------------------------------------------------------------------

    #ligne 1---------------------------
    boule26 = Boule(255, 115, L)
    boule26.dessiner(plateau.image_base)

    boule27 = Boule(296, 156, A)
    boule27.dessiner(plateau.image_base)

    boule28 = Boule(336, 196, B)
    boule28.dessiner(plateau.image_base)

    boule29 = Boule(377, 236, C)
    boule29.dessiner(plateau.image_base)

    #ligne 2---------------------------
    boule30 = Boule(417, 277, D)
    boule30.dessiner(plateau.image_base)

    boule31 = Boule(458, 318, E)
    boule31.dessiner(plateau.image_base)

    boule32 = Boule(499, 358, F)
    boule32.dessiner(plateau.image_base)

    boule33 = Boule(133, 75, G)
    boule33.dessiner(plateau.image_base)

    #ligne 3---------------------------
    boule34 = Boule(174, 115, H)
    boule34.dessiner(plateau.image_base)

    boule35 = Boule(214, 156, I)
    boule35.dessiner(plateau.image_base)

    boule36 = Boule(255, 196, J)
    boule36.dessiner(plateau.image_base)

    boule37 = Boule(296, 236, K)
    boule37.dessiner(plateau.image_base)

    #ligne 4----------------------------
    boule38 = Boule(336, 277, L)
    boule38.dessiner(plateau.image_base)

    boule39 = Boule(377, 318, A)
    boule39.dessiner(plateau.image_base)

    boule40 = Boule(92, 115, B)
    boule40.dessiner(plateau.image_base)

    boule41 = Boule(133, 156, C)
    boule41.dessiner(plateau.image_base)

    #ETAGE 2:--------------------------------------------------------------------------------------------------

    #ligne 1----------------------------
    boule42 = Boule(174, 196, D)
    boule42.dessiner(plateau.image_base)

    boule43 = Boule(214, 236, E)
    boule43.dessiner(plateau.image_base)

    boule44 = Boule(255, 277, F)
    boule44.dessiner(plateau.image_base)

    #ligne 2----------------------------
    boule45 = Boule(296, 318, G)
    boule45.dessiner(plateau.image_base)

    boule46 = Boule(336, 358, H)
    boule46.dessiner(plateau.image_base)

    boule47 = Boule(52, 156, I)
    boule47.dessiner(plateau.image_base)

    #ligne 3----------------------------
    boule48 = Boule(92, 196, K)
    boule48.dessiner(plateau.image_base)

    boule49 = Boule(133, 236, L)
    boule49.dessiner(plateau.image_base)

    boule50 = Boule(174, 277, A)
    boule50.dessiner(plateau.image_base)

    #ETAGE 3:--------------------------------------------------------------------------------------------------

    #ligne 1----------------------------
    boule51 = Boule(214, 318, B)
    boule51.dessiner(plateau.image_base)

    boule52 = Boule(52, 236, C)
    boule52.dessiner(plateau.image_base)

    #ligne 2----------------------------
    boule53 = Boule(92, 277, D)
    boule53.dessiner(plateau.image_base)

    boule54 = Boule(133, 318, E)
    boule54.dessiner(plateau.image_base)

    #ETAGE 4:--------------------------------------------------------------------------------------------------

    boule55 = Boule(174, 358, F)
    boule55.dessiner(plateau.image_base)
    
    """




        


    


    en_cours = True
    while en_cours:
        # 1. Dimensions actuelles de la fenêtre
        largeur_f = fenetre.get_width()
        hauteur_f = fenetre.get_height()

        #Centrage de l'image
        plateau.rect.center = (largeur_f // 2, hauteur_f // 2)


        # 3. Gestion des événements (clavier + souris)
        pos_souris = pygame.mouse.get_pos()
        clic_souris = (False, False, False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "difficulte_3d_pyramidal"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clic_souris = (True, False, False)


        # 5. Affichage dynamique
        fenetre.fill(BLANC)

        # Titre centré à 7% de la hauteur
        titre = police_titre.render("JEU", True, NOIR)
        titre_rect = titre.get_rect(center=(largeur_f // 2, int(hauteur_f * 0.07)))
        fenetre.blit(titre, titre_rect)

        # Dessiner le plateau
        plateau.dessiner(fenetre)

        # Message d'information centré à 94% de la hauteur
        info = police_info.render("Appuie sur ECHAP pour revenir à la sélection de la difficulté", True, BLEU)
        info_rect = info.get_rect(center=(largeur_f // 2, int(hauteur_f * 0.94)))
        fenetre.blit(info, info_rect)

        pygame.display.flip()
        horloge.tick(60)