"""Implémentation du modèle de Nagel-Schreckenberg"""

"""Ce modèle a pour but de modéliser les intersections acec 
les interactions avec des feux"""

VITESSE_MAX = 2
MAX_DENSITE = 200
DENSITE_ACCIDENT = 50

from animation import animate
import matplotlib.pyplot as plt
import numpy as np
from random import randint
from random import randrange
import keyboard

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
        if (self.vitesse < VITESSE_MAX):
            self.vitesse += 1

    def ajoute_perturbation(self, proba, action):
        if randint(0, 100) <  proba: 
            action()
        
    def ralentir(self):
        if self.vitesse > 0:
            self.vitesse -= 1

    def get_vitesse(self):
        return self.vitesse

class Case: 
    def __init__(self, y, x, densite = 0):
        self.densite = densite
        self.x = x 
        self.y = y
        self.voie = None
        self.voiture = [] 
    
    def ajoute_perturbation(self, proba, action):
        if randint(0, 100) <  proba: 
            action()
    

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

class Route : 
    def __init__(self, nbr_ligne, nbr_colonne):
        #randint(0, MAX_DENSITE))
        self.nbr_ligne = nbr_ligne 
        self.nbr_colonne = nbr_colonne
        self.route = [[Case(j,i,self.placement_voiture(j))  for i in range(nbr_colonne) ] for j in range(nbr_ligne)]
        self.arrive = 0
        self.tour = 0
        self.voiture_total = 0
        self.affiches_tour = []
        self.affiche_densite_total_tab = []
        self.ajoute_voiture_case()
        self.densite_par_tour = [self.creer_tableau_densite()]
        
    def ajoute_voiture_case(self):
        for ligne in self.route:
            for case in ligne: 
                for _ in range(case.densite):
                    case.ajoute_voiture(self.nbr_ligne, self.nbr_colonne)
                    self.voiture_total += 1

    def placement_voiture(self, position_x):
        return randint(0, MAX_DENSITE - position_x * 5)
        
    def avance_voiture(self, case, voiture1, case_suivante): 
        case_suivante.voiture.append(voiture1)
        case_suivante.ajoute_densite()
        case.voiture.remove(voiture1)
        case.retire_densite()
    
    def chemin_opti(self, liste_case):
        meilleur_case = liste_case[0]
        for i in range(1,len(liste_case)): 
            if liste_case[i].densite < meilleur_case.densite: 
                meilleur_case = liste_case[i]
        return meilleur_case
            
    """A fixer"""
    def avance_direction(self, voiture, case):
        cases_possibles = []
        #if voiture.destination_ligne == case.y:
        if case.x == self.nbr_colonne - 1: 
            if voiture.destination_ligne == case.y:
                self.arrive += 1
                case.voiture.remove(voiture)
                case.retire_densite()
                return;
        elif voiture.vitesse + case.x >= self.nbr_colonne:
            if voiture.destination_ligne == case.y:
                self.arrive += 1
                case.voiture.remove(voiture)
                case.retire_densite()
                return;
            #else :
                #cases_possibles.append(self.route[case.y][self.nbr_colonne - 1])
        else :
            cases_possibles.append(self.route[case.y][case.x+voiture.vitesse ])
            #self.avance_voiture( case, voiture, self.route[case.y][case.x+voiture.vitesse ])
        if voiture.destination_ligne < case.y:
            #if case.y + voiture.vitesse < voiture.destination_ligne : cases_possibles.append(self.route[case.y - voiture.vitesse][case.x])
            #else: 
            cases_possibles.append(self.route[case.y - 1][case.x])
            #self.avance_voiture(case, voiture, self.route[case.y - 1][case.x])
        elif voiture.destination_ligne > case.y:
            #if case.voiture + voiture.vitesse > self.nbr_ligne: 
            #else:  cases_possibles.append(self.route[case.y + voiture.vitesse][case.x])
            cases_possibles.append(self.route[case.y + 1][case.x])
            #self.avance_voiture(case, voiture, self.route[case.y + 1][case.x])
        #print(len(cases_possibles))
        meilleur_case = self.chemin_opti(cases_possibles)
        self.avance_voiture(case, voiture, meilleur_case)

    def creer_tableau_densite(self):
        tab = []
        for i, ligne in enumerate(self.route):
            tab.append([])
            for case in ligne: 
                tab[i].append(case.densite)
        return tab
                
        
    
    def jouer_tour(self):
        self.tour += 1
        self.densite_par_tour.append(self.creer_tableau_densite())
        for i in range(self.nbr_ligne):
            for j in range(self.nbr_colonne):
                case = self.route[self.nbr_ligne - i - 1][self.nbr_colonne - j - 1]
                #case.ajoute_perturbation(30, case.accident)
                for voiture in case.voiture:
                    voiture.ajoute_vitesse()
                    proba = (case.densite*100)//MAX_DENSITE
                    voiture.ajoute_perturbation(proba, voiture.ralentir)
                    
                    self.avance_direction(voiture, case)
                    #print(voiture.vitesse)
        self.affiche_densite_total()
        #print(self.route[19][19].densite)
        print(self.voiture_total - self.arrive)

    def check_tous_arrive(self): 
        return self.arrive == self.voiture_total 

    def affiche_densite_total(self):
        self.affiche_densite_total_tab.append(self.voiture_total - self.arrive)

def main(nbr_ligne, nbr_colonne):
    route1 = Route(nbr_ligne, nbr_colonne)
    while not route1.check_tous_arrive():
        route1.jouer_tour()

    print(route1.arrive,"voitures arrivées en", route1.tour, "tours")
    """Affichage du plot"""
    #x = [i for i in range(route1.tour)]
    #y = route1.affiche_densite_total_tab
    #plt.plot(x, y)
    #plt.show()
    
    animate(nbr_ligne, nbr_colonne, route1.densite_par_tour)

main(11, 11)
