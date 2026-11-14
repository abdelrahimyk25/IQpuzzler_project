import sys
import pygame

from ui import Bouton, Bouton_image

# 1. Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS_CLAIR = (200, 200, 200)
BLEU = (50, 150, 250)


def afficher_grilles_master_2d_orthogonal(fenetre):
    horloge = pygame.time.Clock()

    # Polices
    police_titre = pygame.font.Font(None, 48)
    police_bouton = pygame.font.Font(None, 32)
    police_info = pygame.font.Font(None, 24)

    # Instanciation initiale des 12 boutons images
    boutons = [
    # Colonne 1
    Bouton_image("41", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/41.png", "IQpuzzler_project/interface/src/assets/41.png"),
    Bouton_image("42", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/42.png", "IQpuzzler_project/interface/src/assets/42.png"),
    Bouton_image("43", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/43.png", "IQpuzzler_project/interface/src/assets/43.png"),
    Bouton_image("44", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/44.png", "IQpuzzler_project/interface/src/assets/44.png"),
    # Colonne 2
    Bouton_image("45", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/45.png", "IQpuzzler_project/interface/src/assets/45.png"),
    Bouton_image("46", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/46.png", "IQpuzzler_project/interface/src/assets/46.png"),
    Bouton_image("47", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/47.png", "IQpuzzler_project/interface/src/assets/47.png"),
    Bouton_image("48", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/48.png", "IQpuzzler_project/interface/src/assets/48.png"),
    # Colonne 3
    Bouton_image("49", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/49.png", "IQpuzzler_project/interface/src/assets/49.png"),
    Bouton_image("50", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/50.png", "IQpuzzler_project/interface/src/assets/50.png"),
    Bouton_image("51", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/51.png", "IQpuzzler_project/interface/src/assets/51.png"),
    Bouton_image("52", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/52.png", "IQpuzzler_project/interface/src/assets/52.png"),
    # Colonne 4
    Bouton_image("53", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/53.png", "IQpuzzler_project/interface/src/assets/53.png"),
    Bouton_image("54", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/54.png", "IQpuzzler_project/interface/src/assets/54.png"),
    Bouton_image("55", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/55.png", "IQpuzzler_project/interface/src/assets/55.png"),
    Bouton_image("56", 0, 0, 180, 100, "IQpuzzler_project/interface/src/assets/56.png", "IQpuzzler_project/interface/src/assets/56.png")
]

    en_cours = True
    while en_cours:
        # 1. Dimensions actuelles de la fenêtre
        largeur_f = fenetre.get_width()
        hauteur_f = fenetre.get_height()

        # 2. Calculs pour centrer la grille de 3 colonnes x 4 lignes
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
                return "master_orthogonal"

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