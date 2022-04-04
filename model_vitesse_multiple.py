"""Implémentation du modèle de Nagel-Schreckenberg"""

VITESSE_MAX = 1
MAX_DENSITE = 20

import matplotlib.pyplot as plt
import numpy as np
from random import randint

def bool_aleatoire():
    temp = randint(0,1)
    return 0 if temp == 0 else 1


class Voiture: 
    #Définition de mon objet
    def __init__(self, nbr_ligne, nbr_colonne):
        self.vitesse = 1

        def destination():
            return randint(0, nbr_ligne-1)

        self.destination_ligne = destination()
        self.destination_colonne = nbr_colonne - 1


    def ajoute_vitesse(self):
        if (self.vitesse < VITESSE_MAX - 1):
            self.vitesse += 1

    def get_vitesse(self):
        return self.vitesse

class Case: 
    def __init__(self, y, x, densite = 0):
        self.densite = densite
        self.x = x 
        self.y = y
        self.voiture = [] 

    def ajoute_voiture(self, nbr_ligne, nbr_colonne):
        self.voiture.append(Voiture(nbr_ligne, nbr_colonne))
        self.densite += 1

    def ajoute_densite(self):
        self.densite += 1

    def retire_densite(self):
        if self.densite > 0:
            self.densite -= 1

class Route : 
    def __init__(self, nbr_ligne, nbr_colonne):
        self.nbr_ligne = nbr_ligne 
        self.nbr_colonne = nbr_colonne
        self.route = [[Case(j,i, randint(0, MAX_DENSITE)) for i in range(nbr_colonne) ] for j in range(nbr_ligne)]
        self.arrive = 0
        self.tour = 0
        self.voiture_total = 0
        self.affiches_tour = []
        self.affiche_densite_total_tab = []
        self.ajoute_voiture_case()
        
    def ajoute_voiture_case(self):
        for ligne in self.route:
            for case in ligne: 
                for _ in range(case.densite):
                    case.ajoute_voiture(self.nbr_ligne, self.nbr_colonne)
                    self.voiture_total += 1

    def avance_voiture(self, case, voiture1, case_suivante): 
        case_suivante.voiture.append(voiture1)
        case_suivante.ajoute_densite()
        case.voiture.remove(voiture1)
        case.retire_densite()

    def add_affiche_tour(self):
        pass

    def animate(self, i): 
        return self.affiches_tour[i]
    
    def avance_direction(self, voiture, case):
        if voiture.destination_ligne == case.y:
            if voiture.vitesse + case.x >= self.nbr_colonne:
                self.arrive += 1
                case.voiture.remove(voiture)
                return;
            self.avance_voiture( case, voiture, self.route[case.y][case.x+voiture.vitesse ])
        elif voiture.destination_ligne < case.y:
            self.avance_voiture(case, voiture, self.route[case.y - 1][case.x])
        else :
            self.avance_voiture(case, voiture, self.route[case.y + 1][case.x])
        
    def jouer_tour(self):
        self.tour += 1
        for i in range(self.nbr_ligne):
            for j in range(self.nbr_colonne):
                case = self.route[self.nbr_ligne - i - 1][self.nbr_colonne - j - 1]
                for voiture in case.voiture:
                    voiture.ajoute_vitesse()
                    self.avance_direction(voiture, case)

        self.affiche_densite_total()
    def check_tous_arrive(self): 
        return self.arrive == self.voiture_total 

    def affiche_densite_total(self):
        self.affiche_densite_total_tab.append(self.voiture_total - self.arrive)



def main(nbr_ligne, nbr_colonne):
    route1 = Route(nbr_ligne, nbr_colonne)
    while not route1.check_tous_arrive():
        route1.jouer_tour()
        #while(not route1.check_tous_arrive()):
        #route1.jouer_tour()

    print(route1.arrive,"voitures arrivées en", route1.tour, "tours")
    x = [i for i in range(route1.tour)]
    y = route1.affiche_densite_total_tab
    plt.plot(x, y)
    plt.show()




main(100, 100)
