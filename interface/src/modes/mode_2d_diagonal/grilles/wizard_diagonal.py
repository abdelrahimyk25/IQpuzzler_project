import sys
import pygame

from ui import Bouton, Bouton_image

# 1. Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS_CLAIR = (200, 200, 200)
BLEU = (50, 150, 250)


def afficher_grilles_wizard_2d_diagonal(fenetre):
    horloge = pygame.time.Clock()

    # Polices
    police_titre = pygame.font.Font(None, 48)
    police_bouton = pygame.font.Font(None, 32)
    police_info = pygame.font.Font(None, 24)

    # Instanciation initiale des 12 boutons images
    boutons = [
    # Colonne 1
    Bouton_image("113", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/113.png", "IQpuzzler_project/interface/src/assets/113.png"),
    Bouton_image("114", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/114.png", "IQpuzzler_project/interface/src/assets/114.png"),
    Bouton_image("115", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/115.png", "IQpuzzler_project/interface/src/assets/115.png"),
    Bouton_image("116", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/116.png", "IQpuzzler_project/interface/src/assets/116.png"),
    # Colonne 2
    Bouton_image("117", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/117.png", "IQpuzzler_project/interface/src/assets/117.png"),
    Bouton_image("118", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/118.png", "IQpuzzler_project/interface/src/assets/118.png"),
    Bouton_image("119", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/119.png", "IQpuzzler_project/interface/src/assets/119.png"),
    Bouton_image("120", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/120.png", "IQpuzzler_project/interface/src/assets/120.png"),
    # Colonne 3
    Bouton_image("121", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/121.png", "IQpuzzler_project/interface/src/assets/121.png"),
    Bouton_image("122", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/122.png", "IQpuzzler_project/interface/src/assets/122.png"),
    Bouton_image("123", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/123.png", "IQpuzzler_project/interface/src/assets/123.png"),
    Bouton_image("124", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/124.png", "IQpuzzler_project/interface/src/assets/124.png"),
    # Colonne 4
    Bouton_image("125", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/125.png", "IQpuzzler_project/interface/src/assets/125.png"),
    Bouton_image("126", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/126.png", "IQpuzzler_project/interface/src/assets/126.png"),
    Bouton_image("127", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/127.png", "IQpuzzler_project/interface/src/assets/127.png"),
    Bouton_image("128", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/128.png", "IQpuzzler_project/interface/src/assets/128.png")
    ]

    en_cours = True
    while en_cours:
        # 1. Dimensions actuelles de la fenêtre
        largeur_f = fenetre.get_width()
        hauteur_f = fenetre.get_height()

        # 2. Calculs pour centrer la grille de 3 colonnes x 4 lignes
        largeur_b, hauteur_b = 180, 100
        espacement_x, espacement_y = 200, 115

        # Origine de la grille centrée par rapport au milieu de l'écran
        x_depart = (largeur_f // 2) - int(espacement_x * 1.5) - (largeur_b // 2)
        y_depart = (hauteur_f // 2) - int(espacement_y * 1.5) - (hauteur_b // 2)

        for i, bouton in enumerate(boutons):
            colonne = i // 4  # 0, 1, 2
            ligne = i % 4     # 0, 1, 2, 3
            bouton.rect.x = x_depart + (colonne * espacement_x)
            bouton.rect.y = y_depart + (ligne * espacement_y)

        # 3. Gestion des événements (clavier + souris)
        pos_souris = pygame.mouse.get_pos()
        clic_souris = (False, False, False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "difficulte_2d_diagonal"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clic_souris = (True, False, False)

        # 4. Vérification des clics
        for bouton in boutons:
            bouton.verifier_survol(pos_souris)
            if bouton.a_ete_clique(pos_souris, clic_souris):
                print(f"Lancement de la grille {bouton.texte}")
                return "wizard_diagonal"

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