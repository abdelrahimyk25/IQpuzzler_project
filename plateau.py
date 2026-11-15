
# definir les dims (5x11)
HAUTEUR = 5 #0...4
LARGEUR = 11 #0....10
INTERDIT = "#"
class Plateau :
    #Un grid[y][x] : 
    def __init__(self, largeur= LARGEUR, hauteur = HAUTEUR, cases_interdites =()):

        self.largeur = largeur
        self.hauteur = hauteur
       
        self.grille = [[None] * self.largeur for _ in range (self.hauteur)]
        #Listes des pieces placees et verrouillees
        self.pieces_placees = {} 
        self.pieces_verrouillees = set() # set pour pas permettre de bougé les pieces intialisé au debut
        #mettre des case inutilisable pour la losange
        self.cases_interdites = set(cases_interdites)
        for x,y in self.cases_interdites:
            assert self.dans_plateau(x,y), f"case interdite hors grille : {(x,y)}"
            self.grille[y][x]= INTERDIT

    def dans_plateau(self, x, y): # une fonction pour checker si une piece est dans le plateau ou pas
        return 0 <= x < self.largeur and 0 <= y < self.hauteur

    # Fonction pour verifier si une pieces peut etre placé ou pas
    # forme ici est une orientation normalisée
    #x0, y0 sont la position du coin haut-gauche de la forme sur le plateau
    def peut_placer(self, forme, x0, y0):
        for dx, dy in forme :
            #coordonnée réelle de la bille sur le plateau
            x,y = x0 + dx, y0 + dy
            #echec si on sort de plateau ou la case est déja occupée
            if not self.dans_plateau(x,y) or not self._est_vide(x,y):
                return False
        return True


    def poser_piece(self,id_piece,forme,x0,y0,verrouillee=False)->bool:
        # verification que la piece est placée une seule fois
        if id_piece in self.pieces_placees:
            return False
        #verif avant d'ecrire
        if not self.peut_placer(forme, x0, y0):
            return False
        #calcul des coords absolues de chauqe bille
        coords = [(x0+dx,y0+dy)for dx, dy in forme]
        for x,y in coords:
            self.grille[y][x] = id_piece

        # on les memoris pour pouvoir retirer plutard
        self.pieces_placees[id_piece] = coords
        #piece de défi initial interdit de la retirer ensuite
        if verrouillee:
            self.pieces_verrouillees.add(id_piece)
        return True

    def retirer_piece(self,id_piece)->bool:
        # pas possible de retirer un truc qui n'est pas sur le plateau Mdrr
        if id_piece not in self.pieces_placees:
            return False
        #eviter de retirer un piece de defi initial
        if id_piece in self.pieces_verrouillees:
            return False
        # retire l'entree du catalogue avec pop() et envoie ses coords
        for x,y in self.pieces_placees.pop(id_piece):
            self.grille[y][x] = None # on vide les cases
        return True


    def premiere_case_vide(self) -> tuple[int,int]:
        # on parcours col par col et de ligne haut a ligne bas jusqu'a quand on trouve la case
        for x in range(self.largeur):
            for y in range(self.hauteur):
                if self._est_vide(x,y):
                    return(x,y)
        return None

    # fonction pour la fin de jeu quand le plateau est complet
    def est_complet(self) -> bool: 
        return self.premiere_case_vide() is None

    # fonction pour verifier si le plateau est vide ou pas 
    def _est_vide(self, x , y): 
        return self.grille[y][x] in (None, '.')
    # constructeur pour copier un plateau
    def copier(self) -> "Plateau":
        p = type(self)()
        p.hauteur = self.hauteur
        p.largeur = self.largeur
        p.cases_interdites = set(self.cases_interdites)
        p.grille = [ligne[:] for ligne in self.grille]
        p.pieces_placees = {i : j[:] for i,j in self.pieces_placees.items()}
        p.pieces_verrouillees = set(self.pieces_verrouillees)
        return p

    #fonction pour afficher le plateau
    def afficher(self):
        for ligne in self.grille:
            print(" ".join(c if c else "." for c in ligne ))
        print()






    
