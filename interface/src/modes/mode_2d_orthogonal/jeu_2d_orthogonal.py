import sys
import pygame

from ui import Image, Boule

# 1. Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS_CLAIR = (200, 200, 200)
BLEU = (50, 150, 250)
ROUGE = (255, 0, 0)


def afficher_plateau_2d_orthogonal(fenetre):
    horloge = pygame.time.Clock()

    # Polices
    police_titre = pygame.font.Font(None, 48)
    police_bouton = pygame.font.Font(None, 32)
    police_info = pygame.font.Font(None, 24)

    # image plateau
    plateau = Image(0, 0, 594, 281, "IQpuzzler_project/interface/src/assets/plateau_2d_orthogonal.png")


    # 2. Création et ancrage de la boule directement sur la surface du plateau

    #LIGNE 1:----------------------------------------------
    boule1 = Boule(40, 34, BLEU)
    boule1.dessiner(plateau.image_base)

    boule2 = Boule(93, 34, BLEU)
    boule2.dessiner(plateau.image_base)

    boule3 = Boule(145, 34, BLEU)
    boule3.dessiner(plateau.image_base)

    boule4 = Boule(197, 34, BLEU)
    boule4.dessiner(plateau.image_base)

    boule5 = Boule(249, 34, BLEU)
    boule5.dessiner(plateau.image_base)

    boule6 = Boule(301, 34, BLEU)
    boule6.dessiner(plateau.image_base)

    boule7 = Boule(354, 34, BLEU)
    boule7.dessiner(plateau.image_base)

    boule8 = Boule(406, 34, BLEU)
    boule8.dessiner(plateau.image_base)

    boule9 = Boule(458, 34, BLEU)
    boule9.dessiner(plateau.image_base)

    boule10 = Boule(510, 34, BLEU)
    boule10.dessiner(plateau.image_base)

    boule11 = Boule(563, 34, BLEU)
    boule11.dessiner(plateau.image_base)
    
    #LIGNE 2:----------------------------------------------
    boule12 = Boule(40, 87, ROUGE)
    boule12.dessiner(plateau.image_base)

    boule13 = Boule(93, 87, ROUGE)
    boule13.dessiner(plateau.image_base)

    boule14 = Boule(145, 87, ROUGE)
    boule14.dessiner(plateau.image_base)

    boule15 = Boule(197, 87, ROUGE)
    boule15.dessiner(plateau.image_base)

    boule16 = Boule(249, 87, ROUGE)
    boule16.dessiner(plateau.image_base)

    boule17 = Boule(301, 87, ROUGE)
    boule17.dessiner(plateau.image_base)

    boule18 = Boule(354, 87, ROUGE)
    boule18.dessiner(plateau.image_base)

    boule19 = Boule(406, 87, ROUGE)
    boule19.dessiner(plateau.image_base)

    boule20 = Boule(458, 87, ROUGE)
    boule20.dessiner(plateau.image_base)

    boule21 = Boule(510, 87, ROUGE)
    boule21.dessiner(plateau.image_base)

    boule22 = Boule(563, 87, ROUGE)
    boule22.dessiner(plateau.image_base)

    #LIGNE 3:----------------------------------------------
    boule23 = Boule(40, 140, BLEU)
    boule23.dessiner(plateau.image_base)

    boule24 = Boule(93, 140, BLEU)
    boule24.dessiner(plateau.image_base)

    boule25 = Boule(145, 140, BLEU)
    boule25.dessiner(plateau.image_base)

    boule26 = Boule(197, 140, BLEU)
    boule26.dessiner(plateau.image_base)

    boule27 = Boule(249, 140, BLEU)
    boule27.dessiner(plateau.image_base)

    boule28 = Boule(301, 140, BLEU)
    boule28.dessiner(plateau.image_base)

    boule29 = Boule(354, 140, BLEU)
    boule29.dessiner(plateau.image_base)

    boule30 = Boule(406, 140, BLEU)
    boule30.dessiner(plateau.image_base)

    boule31 = Boule(458, 140, BLEU)
    boule31.dessiner(plateau.image_base)

    boule32 = Boule(510, 140, BLEU)
    boule32.dessiner(plateau.image_base)

    boule33 = Boule(563, 140, BLEU)
    boule33.dessiner(plateau.image_base)

    #LIGNE 4:----------------------------------------------
    boule34 = Boule(40, 192, ROUGE)
    boule34.dessiner(plateau.image_base)

    boule35 = Boule(93, 192, ROUGE)
    boule35.dessiner(plateau.image_base)

    boule36 = Boule(145, 192, ROUGE)
    boule36.dessiner(plateau.image_base)

    boule37 = Boule(197, 192, ROUGE)
    boule37.dessiner(plateau.image_base)

    boule38 = Boule(249, 192, ROUGE)
    boule38.dessiner(plateau.image_base)

    boule39 = Boule(301, 192, ROUGE)
    boule39.dessiner(plateau.image_base)

    boule40 = Boule(354, 192, ROUGE)
    boule40.dessiner(plateau.image_base)

    boule41 = Boule(406, 192, ROUGE)
    boule41.dessiner(plateau.image_base)

    boule42 = Boule(458, 192, ROUGE)
    boule42.dessiner(plateau.image_base)

    boule43 = Boule(510, 192, ROUGE)
    boule43.dessiner(plateau.image_base)

    boule44 = Boule(563, 192, ROUGE)
    boule44.dessiner(plateau.image_base)

    #LIGNE 5:----------------------------------------------
    boule45 = Boule(40, 245, BLEU)
    boule45.dessiner(plateau.image_base)

    boule46 = Boule(93, 245, BLEU)
    boule46.dessiner(plateau.image_base)

    boule47 = Boule(145, 245, BLEU)
    boule47.dessiner(plateau.image_base)

    boule48 = Boule(197, 245, BLEU)
    boule48.dessiner(plateau.image_base)

    boule49 = Boule(249, 245, BLEU)
    boule49.dessiner(plateau.image_base)

    boule50 = Boule(301, 245, BLEU)
    boule50.dessiner(plateau.image_base)

    boule51 = Boule(354, 245, BLEU)
    boule51.dessiner(plateau.image_base)

    boule52 = Boule(406, 245, BLEU)
    boule52.dessiner(plateau.image_base)

    boule53 = Boule(458, 245, BLEU)
    boule53.dessiner(plateau.image_base)

    boule54 = Boule(510, 245, BLEU)
    boule54.dessiner(plateau.image_base)

    boule55 = Boule(563, 245, BLEU)
    boule55.dessiner(plateau.image_base)

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
                return "difficulte_2d_orthogonal"
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