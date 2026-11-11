import sys
import pygame

from ui import Bouton

# 1. Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS_CLAIR = (200, 200, 200)
BLEU = (50, 150, 250)


def afficher_selection_mode(fenetre):
    horloge = pygame.time.Clock()

    # Polices
    police_titre = pygame.font.Font(None, 48)
    police_bouton = pygame.font.Font(None, 32)
    police_info = pygame.font.Font(None, 24)

    # Instanciation initiale des boutons (les positions X et Y seront mises à jour dans la boucle)
    boutons = [
        Bouton("2D orthogonal", 0, 0, 220, 50, GRIS_CLAIR, BLEU),
        Bouton("2D diagonal", 0, 0, 220, 50, GRIS_CLAIR, BLEU),
        Bouton("3D pyramidal", 0, 0, 220, 50, GRIS_CLAIR, BLEU)
    ]

    en_cours = True
    while en_cours:
        # 1. Récupération des dimensions actuelles de la fenêtre
        largeur_f = fenetre.get_width()
        hauteur_f = fenetre.get_height()

        # 2. Recalcul des positions centrées pour les 3 boutons
        largeur_b, hauteur_b = 220, 50
        espacement_y = 70  # Hauteur du bouton + décalage vertical

        centre_x = (largeur_f // 2) - (largeur_b // 2)
        y_depart = (hauteur_f // 2) - espacement_y  # Centre le bloc des 3 boutons verticalement

        for i, bouton in enumerate(boutons):
            bouton.rect.x = centre_x
            bouton.rect.y = y_depart + (i * espacement_y)

        # 3. Gestion des événements
        pos_souris = pygame.mouse.get_pos()
        clic_souris = (False, False, False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"  # Revenir au menu principal
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clic_souris = (True, False, False)

        # 4. Vérification des clics
        for bouton in boutons:
            bouton.verifier_survol(pos_souris)

            if bouton.a_ete_clique(pos_souris, clic_souris):
                if bouton.texte == "2D orthogonal":
                    return "difficulte_2d_orthogonal"
                elif bouton.texte == "2D diagonal":
                    return "difficulte_2d_diagonal"
                elif bouton.texte == "3D pyramidal":
                    return "difficulte_3d_pyramidal"

        # 5. Affichage dynamique
        fenetre.fill(BLANC)

        # Titre centré horizontalement à 15% de la hauteur de l'écran
        titre = police_titre.render("Sélection du Mode de Jeu", True, NOIR)
        titre_rect = titre.get_rect(center=(largeur_f // 2, int(hauteur_f * 0.15)))
        fenetre.blit(titre, titre_rect)

        # Dessiner les boutons
        for bouton in boutons:
            bouton.dessiner(fenetre, police_bouton)

        # Message d'information centré à 85% de la hauteur de l'écran
        info = police_info.render("Appuie sur ECHAP pour revenir au menu", True, BLEU)
        info_rect = info.get_rect(center=(largeur_f // 2, int(hauteur_f * 0.85)))
        fenetre.blit(info, info_rect)

        pygame.display.flip()
        horloge.tick(60)