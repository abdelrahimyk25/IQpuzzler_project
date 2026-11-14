import sys
import pygame

from ui import Bouton, Bouton_image

# 1. Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS_CLAIR = (200, 200, 200)
BLEU = (50, 150, 250)


def afficher_grilles_expert_2d_orthogonal(fenetre):
    horloge = pygame.time.Clock()

    # Polices
    police_titre = pygame.font.Font(None, 48)
    police_bouton = pygame.font.Font(None, 32)
    police_info = pygame.font.Font(None, 24)

    # Instanciation initiale des 16 boutons images (25 à 40)
    boutons = [
        # Colonne 1
        Bouton_image("25", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/25.png", "IQpuzzler_project/interface/src/assets/25.png"),
        Bouton_image("26", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/26.png", "IQpuzzler_project/interface/src/assets/26.png"),
        Bouton_image("27", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/27.png", "IQpuzzler_project/interface/src/assets/27.png"),
        Bouton_image("28", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/28.png", "IQpuzzler_project/interface/src/assets/28.png"),
        # Colonne 2
        Bouton_image("29", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/29.png", "IQpuzzler_project/interface/src/assets/29.png"),
        Bouton_image("30", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/30.png", "IQpuzzler_project/interface/src/assets/30.png"),
        Bouton_image("31", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/31.png", "IQpuzzler_project/interface/src/assets/31.png"),
        Bouton_image("32", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/32.png", "IQpuzzler_project/interface/src/assets/32.png"),
        # Colonne 3
        Bouton_image("33", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/33.png", "IQpuzzler_project/interface/src/assets/33.png"),
        Bouton_image("34", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/34.png", "IQpuzzler_project/interface/src/assets/34.png"),
        Bouton_image("35", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/35.png", "IQpuzzler_project/interface/src/assets/35.png"),
        Bouton_image("36", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/36.png", "IQpuzzler_project/interface/src/assets/36.png"),
        # Colonne 4
        Bouton_image("37", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/37.png", "IQpuzzler_project/interface/src/assets/37.png"),
        Bouton_image("38", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/38.png", "IQpuzzler_project/interface/src/assets/38.png"),
        Bouton_image("39", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/39.png", "IQpuzzler_project/interface/src/assets/39.png"),
        Bouton_image("40", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/40.png", "IQpuzzler_project/interface/src/assets/40.png")
    ]

    en_cours = True
    while en_cours:
        # 1. Dimensions actuelles de la fenêtre (se met à jour au redimensionnement)
        largeur_f = fenetre.get_width()
        hauteur_f = fenetre.get_height()

        # 2. Calculs pour centrer la grille de 4 colonnes x 4 lignes
        largeur_b, hauteur_b = 180, 100
        espacement_x, espacement_y = 200, 115

        # MODIFICATION : Décalage de 1.5 colonne et 1.5 ligne pour centrer un bloc 4x4
        x_depart = (largeur_f // 2) - int(espacement_x * 1.5) - (largeur_b // 2)
        y_depart = (hauteur_f // 2) - int(espacement_y * 1.5) - (hauteur_b // 2)

        for i, bouton in enumerate(boutons):
            colonne = i // 4  # 0, 1, 2, 3 (4 colonnes)
            ligne = i % 4     # 0, 1, 2, 3 (4 lignes)
            bouton.rect.x = x_depart + (colonne * espacement_x)
            bouton.rect.y = y_depart + (ligne * espacement_y)

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

        # 4. Vérification des clics
        for bouton in boutons:
            bouton.verifier_survol(pos_souris)
            if bouton.a_ete_clique(pos_souris, clic_souris):
                print(f"Lancement de la grille {bouton.texte}")
                return "expert_orthogonal"

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