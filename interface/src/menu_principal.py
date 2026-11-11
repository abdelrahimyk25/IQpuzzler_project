import sys
import pygame
from ui import Bouton

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS_CLAIR = (200, 200, 200)
BLEU = (50, 150, 250)


def afficher_menu_principal(fenetre):
    horloge = pygame.time.Clock()
    police_titre = pygame.font.Font(None, 64)
    police_bouton = pygame.font.Font(None, 36)

    # Instanciation initiale des boutons (les positions X et Y seront calculées dynamiquement)
    boutons = [
        Bouton("Jouer", 0, 0, 200, 50, GRIS_CLAIR, BLEU),
        Bouton("Options", 0, 0, 200, 50, GRIS_CLAIR, BLEU),
        Bouton("Quitter", 0, 0, 200, 50, GRIS_CLAIR, BLEU)
    ]

    en_cours = True
    while en_cours:
        # 1. Dimensions actuelles de la fenêtre
        largeur_f = fenetre.get_width()
        hauteur_f = fenetre.get_height()

        # 2. Recalcul des positions centrées pour les 3 boutons
        largeur_b, hauteur_b = 200, 50
        espacement_y = 70  # Hauteur du bouton + espace vertical

        centre_x = (largeur_f // 2) - (largeur_b // 2)
        y_depart = (hauteur_f // 2) - espacement_y  # Centre le bloc des boutons verticalement

        for i, bouton in enumerate(boutons):
            bouton.rect.x = centre_x
            bouton.rect.y = y_depart + (i * espacement_y)

        # 3. Gestion des événements
        pos_souris = pygame.mouse.get_pos()
        clic_souris = (False, False, False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clic_souris = (True, False, False)

        # 4. Interaction avec les boutons
        for bouton in boutons:
            bouton.verifier_survol(pos_souris)
            if bouton.a_ete_clique(pos_souris, clic_souris):
                if bouton.texte == "Jouer":
                    return "selection_mode"
                elif bouton.texte == "Options":
                    print("Ouverture des options...")
                elif bouton.texte == "Quitter":
                    return "quitter"

        # 5. Affichage dynamique
        fenetre.fill(BLANC)

        # Titre centré à 15% de la hauteur de l'écran
        titre_surface = police_titre.render("MON JEU", True, NOIR)
        titre_rect = titre_surface.get_rect(center=(largeur_f // 2, int(hauteur_f * 0.15)))
        fenetre.blit(titre_surface, titre_rect)

        # Dessiner les boutons
        for bouton in boutons:
            bouton.dessiner(fenetre, police_bouton)

        pygame.display.flip()
        horloge.tick(60)