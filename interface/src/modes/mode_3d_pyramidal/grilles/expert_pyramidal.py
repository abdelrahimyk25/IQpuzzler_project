import sys
import pygame

from ui import Bouton, Bouton_image

# 1. Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS_CLAIR = (200, 200, 200)
BLEU = (50, 150, 250)


def afficher_grilles_expert_3d_pyramidal(fenetre):
    horloge = pygame.time.Clock()

    # Polices
    police_titre = pygame.font.Font(None, 48)
    police_bouton = pygame.font.Font(None, 32)
    police_info = pygame.font.Font(None, 24)

    # Instanciation initiale des 12 boutons images
    boutons = [
        # Colonne 1
        Bouton_image("153", 0, 0, 78, 211, "IQpuzzler_project/interface/src/assets/153.png", "IQpuzzler_project/interface/src/assets/153.png"),
        Bouton_image("154", 0, 0, 78, 211, "IQpuzzler_project/interface/src/assets/154.png", "IQpuzzler_project/interface/src/assets/154.png"),
        Bouton_image("155", 0, 0, 78, 211, "IQpuzzler_project/interface/src/assets/155.png", "IQpuzzler_project/interface/src/assets/155.png"),
        Bouton_image("156", 0, 0, 78, 211, "IQpuzzler_project/interface/src/assets/156.png", "IQpuzzler_project/interface/src/assets/156.png"),
        # Colonne 2
        Bouton_image("157", 0, 0, 78, 211, "IQpuzzler_project/interface/src/assets/157.png", "IQpuzzler_project/interface/src/assets/157.png"),
        Bouton_image("158", 0, 0, 78, 211, "IQpuzzler_project/interface/src/assets/158.png", "IQpuzzler_project/interface/src/assets/158.png"),
        Bouton_image("159", 0, 0, 78, 211, "IQpuzzler_project/interface/src/assets/159.png", "IQpuzzler_project/interface/src/assets/159.png"),
        Bouton_image("160", 0, 0, 78, 211, "IQpuzzler_project/interface/src/assets/160.png", "IQpuzzler_project/interface/src/assets/160.png"),
        # Colonne 3
        Bouton_image("161", 0, 0, 78, 211, "IQpuzzler_project/interface/src/assets/161.png", "IQpuzzler_project/interface/src/assets/161.png"),
        Bouton_image("162", 0, 0, 78, 211, "IQpuzzler_project/interface/src/assets/162.png", "IQpuzzler_project/interface/src/assets/162.png"),
        Bouton_image("163", 0, 0, 78, 211, "IQpuzzler_project/interface/src/assets/163.png", "IQpuzzler_project/interface/src/assets/163.png"),
        Bouton_image("164", 0, 0, 78, 211, "IQpuzzler_project/interface/src/assets/164.png", "IQpuzzler_project/interface/src/assets/164.png")
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
                return "expert_pyramidal"

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