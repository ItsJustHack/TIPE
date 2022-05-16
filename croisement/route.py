from case import Case
from random import randint 

MAX_DENSITE = 200

class Route : 
    def __init__(self, nbr_ligne, nbr_colonne):
        #randint(0, MAX_DENSITE))
        self.nbr_ligne = nbr_ligne 
        self.nbr_colonne = nbr_colonne
        self.route = [[Case(j,i,nbr_ligne, nbr_colonne, self.placement_voiture(j), )  for i in range(nbr_colonne) ] for j in range(nbr_ligne)]
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
    
    #def avance_direction(self, voiture, case): 
    #    up_or_down = case.direction_possible[0]
    #    left_or_right = case.direction_possible[1]
    #    if voiture.destination_x 
    

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


