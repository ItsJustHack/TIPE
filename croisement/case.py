
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
        self.direction_possible_case()
    
    def ajoute_perturbation(self, proba, action):
        if randint(0, 100) <  proba: 
            action()
    
    def case_bord(self):
        return self.x == 0 or self.x == self.nbr_colonne - 1 or self.y == 0 or self.y == self.nbr_ligne - 1

    def direction_possible_case(self):
        if not self.case_bord():
            if self.y % 2 == 0: 
                self.direction_possible.append(Direction.DROITE)
            else: 
                self.direction_possible.append(Direction.GAUCHE)
            if self.x % 2 == 0: 
                self.direction_possible.append(Direction.HAUT)
            else: 
                self.direction_possible.append(Direction.BAS)
        else: 
            if self.y == 0: 
                if self.x % 2 == 0: 
                    self.direction_possible.append(Direction.NONE)
                else: 
                    self.direction_possible.append(Direction.BAS)
            elif self.y == self.nbr_colonne - 1: 
                if self.x % 2 == 1: 
                    self.direction_possible.append(Direction.NONE)
                else: 
                    self.direction_possible.append(Direction.HAUT)
            if self.x == 0:
                if self.y % 2 == 0:
                    self.direction_possible.append(Direction.NONE)
                else: 
                    self.direction_possible.append(Direction.DROITE)
            if self.x == self.nbr_colonne - 1: 
                if self.y % 2 == 1: 
                    self.direction_possible.append(Direction.NONE)
                else: 
                    self.direction_possible.append(Direction.GAUCHE)
                    

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
