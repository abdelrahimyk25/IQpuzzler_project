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
        #etage 0:

        (0,0,0) : (46, 342,  15),
        (0,0,1) : (77, 342,  15),
        (0,0,2) : (108, 342,  15),
        (0,0,3) : (139, 342,  15),
        (0,0,4) : (170, 342,  15),

        (0,1,0) : (44, 360,  16),
        (0,1,1) : (76, 360,  16),
        (0,1,2) : (108, 360,  16),
        (0,1,3) : (141, 360,  16),
        (0,1,4) : (173, 360,  16),

        (0,2,0) : (40, 380,  17),
        (0,2,1) : (74, 380,  17),
        (0,2,2) : (108, 380,  17),
        (0,2,3) : (142, 380,  17),
        (0,2,4) : (177, 380,  17),

        (0,3,0) : (36, 401,  18),
        (0,3,1) : (73, 401,  18),
        (0,3,2) : (108, 401,  18),
        (0,3,3) : (144, 401,  18),
        (0,3,4) : (180, 401,  18),

        (0,4,0) : (33, 426,  19),
        (0,4,1) : (70, 426,  19),
        (0,4,2) : (108, 426,  19),
        (0,4,3) : (146, 426,  19),
        (0,4,4) : (184, 426,  19),

        #etage 1:

        (1,0,0) : (62, 236,  15),
        (1,0,1) : (93, 236,  15),
        (1,0,2) : (124, 236,  15),
        (1,0,3) : (155, 236,  15),

        (1,1,0) : (59, 255,  16),
        (1,1,1) : (92, 255,  16),
        (1,1,2) : (124, 255,  16),
        (1,1,3) : (157, 255,  16),

        (1,2,0) : (57, 274,  17),
        (1,2,1) : (91, 274,  17),
        (1,2,2) : (125, 274,  17),
        (1,2,3) : (159, 274,  17),

        (1,3,0) : (54, 295,  18),
        (1,3,1) : (90, 295,  18),
        (1,3,2) : (127, 295,  18),
        (1,3,3) : (163, 295,  18),

        #etage 2:

        (2,0,0) : (77, 153,  15),
        (2,0,1) : (108, 153,  15),
        (2,0,2) : (139, 153,  15),

        (2,1,0) : (75, 173,  16),
        (2,1,1) : (108, 173,  16),
        (2,1,2) : (141, 173,  16),

        (2,2,0) : (74, 192,  17),
        (2,2,1) : (108, 192,  17),
        (2,2,2) : (142, 192,  17),

        #etage 3:

        (3,0,0) : (93, 89,  15),
        (3,0,1) : (124, 89,  15),

        (3,1,0) : (92, 109,  16),
        (3,1,1) : (125, 109,  16),

        #etage 4:

        (4,0,0) : (108, 24,  15)



    }
    

    
    

    """
    #Création et ancrage de la boule directement sur la surface du plateau

    #ETAGE 0:------------------------------------------------------------------------------------------
    
    #ligne 1--------------------------
    boule1 = Boule(46, 342, A, 15)
    boule1.dessiner(plateau.image_base)

    boule2 = Boule(77, 342, B, 15)
    boule2.dessiner(plateau.image_base)

    boule3 = Boule(108, 342, C, 15)
    boule3.dessiner(plateau.image_base)

    boule4 = Boule(139, 342, D, 15)
    boule4.dessiner(plateau.image_base)

    boule5 = Boule(170, 342, E, 15)
    boule5.dessiner(plateau.image_base)

    #ligne 2--------------------------
    boule6 = Boule(44, 360, F, 16)
    boule6.dessiner(plateau.image_base)

    boule7 = Boule(76, 360, G, 16)
    boule7.dessiner(plateau.image_base)

    boule8 = Boule(108, 360, H, 16)
    boule8.dessiner(plateau.image_base)

    boule9 = Boule(141, 360, I, 16)
    boule9.dessiner(plateau.image_base)

    boule10 = Boule(173, 360, J, 16)
    boule10.dessiner(plateau.image_base)
    
    #ligne 3---------------------------
    boule11 = Boule(40, 380, K, 17)
    boule11.dessiner(plateau.image_base)
    
    boule12 = Boule(74, 380, L, 17)
    boule12.dessiner(plateau.image_base)

    boule13 = Boule(108, 380, A, 17)
    boule13.dessiner(plateau.image_base)

    boule14 = Boule(142, 380, B, 17)
    boule14.dessiner(plateau.image_base)

    boule15 = Boule(177, 380, C, 17)
    boule15.dessiner(plateau.image_base)
    
    #ligne 4---------------------------
    boule16 = Boule(36, 401, D, 18)
    boule16.dessiner(plateau.image_base)

    boule17 = Boule(73, 401, C, 18)
    boule17.dessiner(plateau.image_base)

    boule18 = Boule(108, 401, D, 18)
    boule18.dessiner(plateau.image_base)

    boule19 = Boule(144, 401, E, 18)
    boule19.dessiner(plateau.image_base)

    boule20 = Boule(180, 401, F, 18)
    boule20.dessiner(plateau.image_base)
    
    #ligne 5---------------------------
    boule21 = Boule(33, 426, G, 19)
    boule21.dessiner(plateau.image_base)

    boule22 = Boule(70, 426, H, 19)
    boule22.dessiner(plateau.image_base)

    boule23 = Boule(108, 426, I, 19)
    boule23.dessiner(plateau.image_base)

    boule24 = Boule(146, 426, J, 19)
    boule24.dessiner(plateau.image_base)

    boule25 = Boule(184, 426, K, 19)
    boule25.dessiner(plateau.image_base)

    
    #ETAGE 1:-------------------------------------------------------------------------------------

    #ligne 1---------------------------
    boule26 = Boule(62, 236, L, 15)
    boule26.dessiner(plateau.image_base)

    boule27 = Boule(93, 236, A, 15)
    boule27.dessiner(plateau.image_base)

    boule28 = Boule(124, 236, B, 15)
    boule28.dessiner(plateau.image_base)

    boule29 = Boule(155, 236, C, 15)
    boule29.dessiner(plateau.image_base)
    
    #ligne 2---------------------------
    boule30 = Boule(59, 255, D, 16)
    boule30.dessiner(plateau.image_base)

    boule31 = Boule(92, 255, E, 16)
    boule31.dessiner(plateau.image_base)

    boule32 = Boule(124, 255, F, 16)
    boule32.dessiner(plateau.image_base)

    boule33 = Boule(157, 255, G, 16)
    boule33.dessiner(plateau.image_base)
    
    #ligne 3---------------------------
    boule34 = Boule(57, 274, H, 17)
    boule34.dessiner(plateau.image_base)

    boule35 = Boule(91, 274, I, 17)
    boule35.dessiner(plateau.image_base)

    boule36 = Boule(125, 274, J, 17)
    boule36.dessiner(plateau.image_base)

    boule37 = Boule(159, 274, K, 17)
    boule37.dessiner(plateau.image_base)
    
    #ligne 4----------------------------
    boule38 = Boule(54, 295, L, 18)
    boule38.dessiner(plateau.image_base)

    boule39 = Boule(90, 295, A, 18)
    boule39.dessiner(plateau.image_base)

    boule40 = Boule(127, 295, B, 18)
    boule40.dessiner(plateau.image_base)

    boule41 = Boule(163, 295, C, 18)
    boule41.dessiner(plateau.image_base)
    
    #ETAGE 2:--------------------------------------------------------------------------------------------------

    #ligne 1----------------------------
    boule42 = Boule(77, 153, D, 15)
    boule42.dessiner(plateau.image_base)

    boule43 = Boule(108, 153, E, 15)
    boule43.dessiner(plateau.image_base)

    boule44 = Boule(139, 153, F, 15)
    boule44.dessiner(plateau.image_base)
    
    #ligne 2----------------------------
    boule45 = Boule(75, 173, G, 16)
    boule45.dessiner(plateau.image_base)

    boule46 = Boule(108, 173, H, 16)
    boule46.dessiner(plateau.image_base)

    boule47 = Boule(141, 173, I, 16)
    boule47.dessiner(plateau.image_base)
    
    #ligne 3----------------------------
    boule48 = Boule(74, 192, K, 17)
    boule48.dessiner(plateau.image_base)

    boule49 = Boule(108, 192, L, 17)
    boule49.dessiner(plateau.image_base)

    boule50 = Boule(142, 192, A, 17)
    boule50.dessiner(plateau.image_base)
    
    #ETAGE 3:--------------------------------------------------------------------------------------------------

    #ligne 1----------------------------
    boule51 = Boule(93, 89, B, 15)
    boule51.dessiner(plateau.image_base)

    boule52 = Boule(124, 89, C, 15)
    boule52.dessiner(plateau.image_base)

    #ligne 2----------------------------
    boule53 = Boule(92, 109, D, 16)
    boule53.dessiner(plateau.image_base)

    boule54 = Boule(125, 109, E, 16)
    boule54.dessiner(plateau.image_base)
    
    #ETAGE 4:--------------------------------------------------------------------------------------------------

    boule55 = Boule(108, 24, F, 15)
    boule55.dessiner(plateau.image_base)
    
    """

    nb_boules = 5

    for etage in range(5):          
        for ligne in range(nb_boules):
            for boule in range (nb_boules):
                lettre = liste_plateau[etage][ligne][boule]
                if lettre is not None:  
                    cle = (etage,ligne,boule)
                    info_boule = coord[cle]
                    coord_x = info_boule[0]
                    coord_y = info_boule[1]
                    rayon = info_boule[2]
                    couleur = couleurs[lettre]
                    boules[(etage,ligne,boule)] = Boule(coord_x, coord_y, couleur, rayon)
        
        nb_boules -= 1

    for cle, boule in sorted(boules.items(), key=lambda item: item[0][1]):
        boule.dessiner(plateau.image_base)
  


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