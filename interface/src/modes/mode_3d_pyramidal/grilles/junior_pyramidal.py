import sys
import pygame

from ui import Bouton, Bouton_image

# 1. Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS_CLAIR = (200, 200, 200)
BLEU = (50, 150, 250)


def afficher_grilles_junior_3d_pyramidal(fenetre):
    horloge = pygame.time.Clock()

    # Polices
    police_titre = pygame.font.Font(None, 48)
    police_bouton = pygame.font.Font(None, 32)
    police_info = pygame.font.Font(None, 24)

    # Instanciation initiale des 12 boutons images
    boutons = [
        # Colonne 1
        Bouton_image("141", 0, 0, 78, 211, "IQpuzzler_project/interface/src/assets/141.png", "IQpuzzler_project/interface/src/assets/141.png"),
        Bouton_image("142", 0, 0, 78, 211, "IQpuzzler_project/interface/src/assets/142.png", "IQpuzzler_project/interface/src/assets/142.png"),
        Bouton_image("143", 0, 0, 78, 211, "IQpuzzler_project/interface/src/assets/143.png", "IQpuzzler_project/interface/src/assets/143.png"),
        Bouton_image("144", 0, 0, 78, 211, "IQpuzzler_project/interface/src/assets/144.png", "IQpuzzler_project/interface/src/assets/144.png"),
        # Colonne 2
        Bouton_image("145", 0, 0, 78, 211, "IQpuzzler_project/interface/src/assets/145.png", "IQpuzzler_project/interface/src/assets/145.png"),
        Bouton_image("146", 0, 0, 78, 211, "IQpuzzler_project/interface/src/assets/146.png", "IQpuzzler_project/interface/src/assets/146.png"),
        Bouton_image("147", 0, 0, 78, 211, "IQpuzzler_project/interface/src/assets/147.png", "IQpuzzler_project/interface/src/assets/147.png"),
        Bouton_image("148", 0, 0, 78, 211, "IQpuzzler_project/interface/src/assets/148.png", "IQpuzzler_project/interface/src/assets/148.png"),
        # Colonne 3
        Bouton_image("149", 0, 0, 78, 211, "IQpuzzler_project/interface/src/assets/149.png", "IQpuzzler_project/interface/src/assets/149.png"),
        Bouton_image("150", 0, 0, 78, 211, "IQpuzzler_project/interface/src/assets/150.png", "IQpuzzler_project/interface/src/assets/150.png"),
        Bouton_image("151", 0, 0, 78, 211, "IQpuzzler_project/interface/src/assets/151.png", "IQpuzzler_project/interface/src/assets/151.png"),
        Bouton_image("152", 0, 0, 78, 211, "IQpuzzler_project/interface/src/assets/152.png", "IQpuzzler_project/interface/src/assets/152.png")
    ]

    en_cours = True
    while en_cours:
        # 1. Dimensions actuelles de la fenêtre
        largeur_f = fenetre.get_width()
        hauteur_f = fenetre.get_height()

        # Dimensions des boutons (réduites en largeur pour que 6 colonnes rentrent à l'écran)
        largeur_b, hauteur_b = 78, 211
        espacement_x, espacement_y = 115, 220

        x_depart = (largeur_f // 2) - int(espacement_x * 2.5) - (largeur_b // 2)
        y_depart = (hauteur_f // 2) - (espacement_y // 2) - (hauteur_b // 2)

        for i, bouton in enumerate(boutons):
            colonne = i // 2  # 0, 1, 2, 3, 4, 5 (6 colonnes)
            ligne = i % 2     # 0, 1 (2 lignes)
            bouton.rect.x = x_depart + (colonne * espacement_x)
            bouton.rect.y = y_depart + (ligne * espacement_y)

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

        # 4. Vérification des clics
        for bouton in boutons:
            bouton.verifier_survol(pos_souris)
            if bouton.a_ete_clique(pos_souris, clic_souris):
                print(f"Lancement de la grille {bouton.texte}")
                return "junior_pyramidal"

        # 5. Affichage dynamique
        fenetre.fill(BLANC)

        # Titre centré à 7% de la hauteur
        titre = police_titre.render("Sélectionnez la grille", True, NOIR)
        titre_rect = titre.get_rect(center=(largeur_f // 2, int(hauteur_f * 0.07)))
        fenetre.blit(titre, titre_rect)

        # Dessiner les boutons
        for bouton in boutons:
            bouton.dessiner(fenetre, police_bouton)

        # Message d'information centré à 94% de la hauteur
        info = police_info.render("Appuie sur ECHAP pour revenir à la sélection de la difficulté", True, BLEU)
        info_rect = info.get_rect(center=(largeur_f // 2, int(hauteur_f * 0.94)))
        fenetre.blit(info, info_rect)

        pygame.display.flip()
        horloge.tick(60)