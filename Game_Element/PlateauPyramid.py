from collections import deque



class PlateauPyramid:
    BASE = 5



    def __init__(self,base = BASE):
        if not isinstance(base, int) or base <= 0:
            raise ValueError('la base doit etre une entier positif')
        self.base = base
        self.grille = [[[None for _ in range(base-z)]for _ in range(base-z)] for z in range(base)]
        self.pieces_placees = {}
        self.pieces_verrouillees = set()



    def dans_plateau(self,x,y,z):
        return (0 <= z < self.base and 0 <= x < self.base-z and 0 <= y < self.base-z)

    def _est_vide(self, x,y,z):
        return self.dans_plateau(x,y,z) and self.grille[z][y][x] is None



    def peut_placer(self, forme, x0,y0,z0):
        return bool(forme) and all(self._est_vide(x0+dx, y0+dy, z0 + dz) for dx,dy,dz in forme)




    def poser_piece(self, id_piece, forme, x0,y0,z0, verrouillee = False):
        if id_piece in self.pieces_placees or not self.peut_placer(forme, x0, y0, z0):
            return False

        coords = [(x0+dx, y0+dy,z0+dz) for dx, dy, dz in forme]
        for x,y,z in coords:
            self.grille[z][y][x] = id_piece
        self.pieces_placees[id_piece] = coords

        if verrouillee:
            self.pieces_verrouillees.add(id_piece)
        return True


    def retirer_piece(self, id_piece):
        if id_piece not in self.pieces_placees or id_piece in self.pieces_verrouillees:
            return False
        for x,y,z in self.pieces_placees.pop(id_piece):
            self.grille[z][y][x] = None
        return True


    def premiere_case_vide(self):
        for z in range(self.base):
            for y in range(self.base-z):
                for x in range(self.base-z):
                    if self._est_vide(x,y,z):
                        return x,y,z

        return None


    def get_ilots_vides(self):
        ilots, visitees = [], set()
        for z in range(self.base):
            for y in range(self.base-z):
                for x in range(self.base-z):
                    depart = (x,y,z)
                    if not self._est_vide(*depart) or depart in visitees:
                        continue
                    file,ilot = deque([depart]), set()
                    visitees.add(depart)
                    while file:
                        p = file.popleft()
                        ilot.add(p)
                        for voisin in self._voisins(*p):
                            if voisin not in visitees and self._est_vide(*voisin):
                               visitees.add(voisin)
                               file.append(voisin)
                ilots.append(ilot)
        return ilots            


    def _voisins(self, x,y,z):

        for dx,dy,dz in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
            nx,ny,nz = x+dx , y+dy, z+dz
            if self.dans_plateau(nx,ny,nz):
                yield nx,ny,nz



    def est_complet(self):
        return self.premiere_case_vide() is None

    def copier(self):
        p = type(self)(self.base)
        p.grille = [[ligne[:] for ligne in niveau] for niveau in self.grille]
        p.pieces_placees = {ident: coords[:] for ident , coords in self.pieces_placees.items()}
        p.pieces_verrouillees = set(self.pieces_verrouillees)
        return p


    def afficher(self):
        for z, niveau in enumerate(self.grille):
            print(f'Niveau {z} ({self.base-z}x{self.base-z})')
            for ligne in niveau:
                print(' '.join(str(case) if case is not None else '.' for case in ligne))
            print()


    def case_la_plus_contrainte(self):
        meilleure, min_voisins = None, float('inf')
        for z in range(self.base):
            for y in range(self.base-z):
                for x in range(self.base - z):
                    if not self._est_vide(x,y,z):
                        continue
                    n = sum(self._est_vide(*v) for v in self._voisins(x,y,z))
                    if n == 0:
                        return (x,y,z)
                    if n < min_voisins:
                        min_voisins, meilleure = n,(x,y,z)
        return meilleure

    

