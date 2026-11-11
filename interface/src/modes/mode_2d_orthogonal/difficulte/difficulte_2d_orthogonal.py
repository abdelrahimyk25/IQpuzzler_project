import sys
import pygame
from ui import Bouton

# 1. Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS_CLAIR = (200, 200, 200)
BLEU = (50, 150, 250)


def afficher_difficulte_2d_orthogonal(fenetre):
    horloge = pygame.time.Clock()

    # Polices
    police_titre = pygame.font.Font(None, 48)
    police_bouton = pygame.font.Font(None, 32)
    police_info = pygame.font.Font(None, 24)

    # Instanciation initiale des 5 boutons
    boutons = [
        Bouton("STARTER", 0, 0, 200, 50, GRIS_CLAIR, BLEU),
        Bouton("JUNIOR", 0, 0, 200, 50, GRIS_CLAIR, BLEU),
        Bouton("EXPERT", 0, 0, 200, 50, GRIS_CLAIR, BLEU),
        Bouton("MASTER", 0, 0, 200, 50, GRIS_CLAIR, BLEU),
        Bouton("WIZARD", 0, 0, 200, 50, GRIS_CLAIR, BLEU)
    ]

    en_cours = True
    while en_cours:
        # 1. Dimensions actuelles de la fenêtre
        largeur_f = fenetre.get_width()
        hauteur_f = fenetre.get_height()

        # 2. Recalcul des positions centrées pour les 5 boutons
        largeur_b, hauteur_b = 200, 50
        espacement_y = 65  # Hauteur du bouton + décalage entre chaque bouton

        centre_x = (largeur_f // 2) - (largeur_b // 2)
        # 2 * espacement_y décale le premier bouton vers le haut pour centrer les 5 boutons
        y_depart = (hauteur_f // 2) - (2 * espacement_y)

        for i, bouton in enumerate(boutons):
            bouton.rect.x = centre_x
            bouton.rect.y = y_depart + (i * espacement_y)

        # 3. Gestion des événements (clavier + souris)
        pos_souris = pygame.mouse.get_pos()
        clic_souris = (False, False, False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "selection_mode"  # Revenir à la sélection du mode
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clic_souris = (True, False, False)

        # 4. Vérification des clics
        for bouton in boutons:
            bouton.verifier_survol(pos_souris)

            if bouton.a_ete_clique(pos_souris, clic_souris):
                if bouton.texte == "STARTER":
                    return "starter_orthogonal"
                elif bouton.texte == "JUNIOR":
                    return "difficulte_2d_orthogonal"
                elif bouton.texte == "EXPERT":
                    return "difficulte_2d_orthogonal"
                elif bouton.texte == "MASTER":
                    return "difficulte_2d_orthogonal"
                elif bouton.texte == "WIZARD":
                    return "difficulte_2d_orthogonal"

        # 5. Affichage dynamique
        fenetre.fill(BLANC)

        # Titre centré à 12% de la hauteur
        titre = police_titre.render("Sélectionnez la difficulté", True, NOIR)
        titre_rect = titre.get_rect(center=(largeur_f // 2, int(hauteur_f * 0.12)))
        fenetre.blit(titre, titre_rect)

        # Dessiner les boutons
        for bouton in boutons:
            bouton.dessiner(fenetre, police_bouton)

        # Message d'information centré à 90% de la hauteur
        info = police_info.render("Appuie sur ECHAP pour revenir à la sélection du mode", True, BLEU)
        info_rect = info.get_rect(center=(largeur_f // 2, int(hauteur_f * 0.90)))
        fenetre.blit(info, info_rect)

        pygame.display.flip()
        horloge.tick(60)