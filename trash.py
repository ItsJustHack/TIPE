"""Implémentation du modèle de Nagel-Schreckenberg"""

VITESSE_MAX = 5

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
        self.destination_colonne = nbr_colonne 


    def ajoute_vitesse(self):
        if (self.vitesse < VITESSE_MAX - 1):
            self.vitesse += 1

class Case: 
    def __init__(self, y, x, nbr_ligne, nbr_colonne, voiture_dessus = False, voiture = None):
        self.voiture_dessus = voiture_dessus 
        self.voiture = voiture
        self.nbr_ligne = nbr_ligne 
        self.nbr_colonne = nbr_colonne
        self.x = x 
        self.y = y
        self.densite = 0

    def ajoute_voiture(self):
        if not self.voiture_dessus: 
            self.voiture_dessus = True 
            self.voiture = Voiture(self.nbr_ligne, self.nbr_colonne)
            

class Route : 
    def __init__(self, nbr_ligne, nbr_colonne):
        self.nbr_ligne = nbr_ligne 
        self.nbr_colonne = nbr_colonne
        self.route = [[Case(j,i, nbr_ligne, nbr_colonne, False, None) for i in range(nbr_colonne) ] for j in range(nbr_ligne)]
        self.ajoute_voiture_aleatoire()
        self.arrive = 0

    def ajoute_voiture_aleatoire(self):
        for i in range(self.nbr_ligne - 1) : 
            for j in range(self.nbr_colonne): 
                if bool_aleatoire():
                    self.route[i][j].ajoute_voiture()
    
    def check_libre(self, case):
        if not case.voiture_dessus: 
            return False, False
        bas, droite, haut = False, False, False
        position_x = case.x 
        position_y = case.y 
        if position_x != self.nbr_colonne -1 :
            if not self.route[position_y][position_x +1 ].voiture_dessus:
                droite = self.route[position_y][position_x +1 ]
        if position_y != self.nbr_ligne - 1 :
            if not self.route[position_y+1][position_x].voiture_dessus:
                bas = self.route[position_y+1][position_x]
        if position_y != 0 :
            if not self.route[position_y-1][position_x].voiture_dessus:
                haut = self.route[position_y-1][position_x]
        return bas,haut,droite

    def avance_voiture(self, case, case_suivante): 
        if (case_suivante.x == case.voiture.destination_ligne and case_suivante.y == case.voiture.destination_colonne):
            self.arrive += 1
            case.voiture = None
            case.voiture_dessus = False
            return ;
        case.voiture_dessus = False 
        case_suivante.voiture_dessus = True 
        case_suivante.voiture = case.voiture 
        case.voiture = None


    def avance_direction(self, case):
        if not case.voiture_dessus:
            return False
        #print("La direction de la voiture est", case.voiture.destination_ligne, case.voiture.destination_colonne)
        destination_x = case.voiture.destination_ligne
        destination_y = case.voiture.destination_colonne
        bas, haut, droite = self.check_libre(case)       
        if (case.y < destination_y) and bas != False : 
            self.avance_voiture(case, bas)
            print("J'avance vers le bas")
            return ;
        if (case.y > destination_y) and haut != False:
            self.avance_voiture(case, haut)
            print("J'avance vers le haut")
            return ;
        if (case.x < destination_x and droite != False):
            self.avance_voiture(case, droite)
            print("J'avance vers la droite")
            return ;
        print("Je ne bouge pas") 

    def check_tous_arrive(self):
        for ligne in self.route:
            for case in ligne: 
                if case.voiture_dessus:
                    return False
        return True 

    def affiche_voiture(self):
        truc =" machine "
        for ligne in self.route:
            for case in ligne: 
                print(case.voiture, case.x, case.y, truc) 

def jouer_tour(route1):
    for i in range(route1.nbr_ligne):
        for j in range(route1.nbr_colonne):
            route1.avance_direction(route1.route[route1.nbr_ligne - i - 1][route1.nbr_colonne - j - 1])

def main(nbr_ligne, nbr_colonne):
    route1 = Route(nbr_ligne, nbr_colonne)
    i = 0
    while (not route1.check_tous_arrive()):
        i += 1
        jouer_tour(route1)
        route1.affiche_voiture()
    return i 




print(main(3,4))
