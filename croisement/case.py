
from voiture import Voiture
from direction import Direction
from random import randint

DENSITE_ACCIDENT = 50

class Case: 
    def __init__(self, y, x, nbr_ligne, nbr_colonne, densite = 0):
        self.nbr_ligne = nbr_ligne 
        self.nbr_colonne = nbr_colonne
        self.densite = densite
        self.x = x 
        self.y = y
        self.direction_possible = []
        self.voiture = [] 
        self.arrete = False #Tous les feux sont aux verts au début
        print("Case : ", x, y)
        self.direction_possible_case()
    
    def ajoute_perturbation(self, proba, action):
        if randint(0, 100) <  proba: 
            action()
    
    def case_bord(self):
        return self.x == 0 or self.x == self.nbr_colonne - 1 or self.y == 0 or self.y == self.nbr_ligne - 1

    def case_bord_gauche(self):
        return self.x == 0

    def case_bord_droite(self):
        return self.x == self.nbr_colonne - 1

    def case_bord_haut(self):
        return self.y == 0

    def case_bord_bas(self):
        return self.y == self.nbr_ligne - 1
    

    def direction_possible_case(self):
        if not self.case_bord():
            if self.y % 2 == 0: 
                self.direction_possible.append(Direction.DROITE)
            else: 
                self.direction_possible.append(Direction.GAUCHE)
            if self.x % 2 == 0: 
                self.direction_possible.append(Direction.BAS)
            else: 
                self.direction_possible.append(Direction.HAUT)
        else: 
            if self.case_bord_gauche():
                if self.y % 2 == 0: 
                    self.direction_possible.append(Direction.NONE)
                else: 
                    self.direction_possible.append(Direction.DROITE)
                if self.y == self.nbr_ligne - 1:
                    self.direction_possible.append(Direction.NONE)
                else:
                    self.direction_possible.append(Direction.BAS)
            elif self.case_bord_droite():
                if self.y % 2 == 0:
                    self.direction_possible.append(Direction.GAUCHE)
                else: 
                    self.direction_possible.append(Direction.NONE)
                if self.y == 0: #Cela suppose une grille de dimension paire
                    self.direction_possible.append(Direction.NONE)
                else:
                    self.direction_possible.append(Direction.HAUT)
            elif self.case_bord_haut():
                if self.x == 0:
                    self.direction_possible.append(Direction.NONE)
                else:
                    self.direction_possible.append(Direction.GAUCHE)
                if self.x % 2 == 0:
                    self.direction_possible.append(Direction.BAS)
                else:
                    self.direction_possible.append(Direction.NONE)
            elif self.case_bord_bas():
                if self.x == self.nbr_colonne - 1:
                    self.direction_possible.append(Direction.NONE)
                else:
                    self.direction_possible.append(Direction.DROITE)
                if self.x % 2 == 0:
                    self.direction_possible.append(Direction.NONE)
                else:
                    self.direction_possible.append(Direction.HAUT)
                
                    
                
                    
            """
            print("Je suis dans le cas 2")
            if self.y == 0: 
                if self.x % 2 == 1: 
                    self.direction_possible.append(Direction.NONE)
                    compteur += 1
                else: 
                    self.direction_possible.append(Direction.BAS)
                    compteur += 1
            if self.y == self.nbr_ligne - 1: 
                if self.x % 2 == 0: 
                    self.direction_possible.append(Direction.NONE)
                    compteur += 1
                else: 
                    self.direction_possible.append(Direction.HAUT)
                    compteur += 1
            if self.x == 0:
                if self.y % 2 == 0:
                    self.direction_possible.append(Direction.NONE)
                    compteur += 1
                else: 
                    self.direction_possible.append(Direction.DROITE)
                    compteur += 1
            if self.x == self.nbr_colonne - 1: 
                if self.y % 2 == 1: 
                    self.direction_possible.append(Direction.NONE)
                    compteur += 1
                else: 
                    self.direction_possible.append(Direction.GAUCHE)
                    compteur += 1
            """
        #print(compteur)
                    

    def accident(self):
        if self.densite > DENSITE_ACCIDENT:
            for voiture in self.voiture:
                if voiture.vitesse > 0:
                    voiture.vitesse -= 1

    def ajoute_voiture(self, nbr_ligne, nbr_colonne):
        self.voiture.append(Voiture(nbr_ligne, nbr_colonne))

    def ajoute_densite(self):
        self.densite += 1

    def retire_densite(self):
        if self.densite > 0:
            self.densite -= 1
