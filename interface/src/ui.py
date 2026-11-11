# ui.py
import pygame

NOIR = (0, 0, 0)


class Bouton:

  def __init__(self, texte, x, y, largeur, hauteur, couleur_base, couleur_survol):
    self.texte = texte
    self.rect = pygame.Rect(x, y, largeur, hauteur)
    self.couleur_base = couleur_base
    self.couleur_survol = couleur_survol
    self.est_survole = False

  def dessiner(self, surface, police):
    couleur = self.couleur_survol if self.est_survole else self.couleur_base
    pygame.draw.rect(surface, couleur, self.rect, border_radius=10)

    texte_surface = police.render(self.texte, True, NOIR)
    texte_rect = texte_surface.get_rect(center=self.rect.center)
    surface.blit(texte_surface, texte_rect)

  def verifier_survol(self, pos_souris):
    self.est_survole = self.rect.collidepoint(pos_souris)

  def a_ete_clique(self, pos_souris, clic_souris):
    return self.est_survole and clic_souris[0]


class Bouton_image:

  def __init__(
      self,
      texte,
      x,
      y,
      largeur,
      hauteur,
      chemin_img_base,
      chemin_img_survol=None,
  ):
    self.texte = texte
    self.rect = pygame.Rect(x, y, largeur, hauteur)
    self.est_survole = False

    # Chargement et redimensionnement de l'image de base
    img_base = pygame.image.load(chemin_img_base).convert_alpha()
    self.image_base = pygame.transform.scale(img_base, (largeur, hauteur))

    # Chargement de l'image au survol (optionnel)
    if chemin_img_survol:
      img_survol = pygame.image.load(chemin_img_survol).convert_alpha()
      self.image_survol = pygame.transform.scale(img_survol, (largeur, hauteur))
    else:
      self.image_survol = self.image_base

  def dessiner(self, surface, police):
    # Choix de l'image selon l'état de survol
    image_active = self.image_survol if self.est_survole else self.image_base

    # Dessin de l'image
    surface.blit(image_active, self.rect)

    """
    if self.texte:
          texte_surface = police.render(self.texte, True, NOIR)
          texte_rect = texte_surface.get_rect(center=self.rect.center)
          surface.blit(texte_surface, texte_rect)
    """
    

  def verifier_survol(self, pos_souris):
    self.est_survole = self.rect.collidepoint(pos_souris)

  def a_ete_clique(self, pos_souris, clic_souris):
    return self.est_survole and clic_souris[0]