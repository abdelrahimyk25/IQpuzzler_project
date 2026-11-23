
from PIL import Image

img = Image.open("IQpuzzler_project/interface/src/assets/plateau_3d_pyramidal.png")
print(img.size)
"""



from PIL import Image, ImageDraw


def arrondir_angles(chemin_entree, chemin_sortie, rayon):
    # 1. Ouvrir l'image et la convertir en RGBA (pour gérer la transparence)
    image = Image.open(chemin_entree).convert("RGBA")
    largeur, hauteur = image.size

    # 2. Créer un masque haute résolution (x4) pour un lissage parfait (anti-aliasing)
    facteur = 4
    masque = Image.new("L", (largeur * facteur, hauteur * facteur), 0)
    dessin = ImageDraw.Draw(masque)

    # 3. Dessiner un rectangle blanc aux coins arrondis sur le masque
    dessin.rounded_rectangle(
        [(0, 0), (largeur * facteur, hauteur * facteur)],
        radius=rayon * facteur,
        fill=255,
    )

    # 4. Redimensionner le masque à la taille d'origine avec un filtre doux
    masque = masque.resize((largeur, hauteur), Image.Resampling.LANCZOS)

    # 5. Appliquer le masque à l'image et sauvegarder en PNG
    resultat = Image.new("RGBA", (largeur, hauteur), (0, 0, 0, 0))
    resultat.paste(image, (0, 0), mask=masque)
    resultat.save(chemin_sortie, format="PNG")
    print(f"Image sauvegardée avec succès : {chemin_sortie}")


# --- Exemple d'utilisation ---
arrondir_angles(
    chemin_entree="IQpuzzler_project/interface/src/assets/plateau_3d_pyramidal.png",
    chemin_sortie="image_arrondie.png",
    rayon=200,  # Rayon de courbure en pixels
)





"""