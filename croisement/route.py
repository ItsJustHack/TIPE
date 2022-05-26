from case import Case
from case import Direction
from random import randint 

MAX_DENSITE = 200

class Route : 
    def __init__(self, nbr_ligne, nbr_colonne):
        #randint(0, MAX_DENSITE))
        self.nbr_ligne = nbr_ligne 
        self.nbr_colonne = nbr_colonne
        self.route = [[Case(j,i,nbr_ligne, nbr_colonne, self.placement_voiture(j))   for i in range(nbr_colonne) ] for j in range(nbr_ligne)]
#self.placement_voiture(j) )        print("Longueur de ma liste totale", len(self.route[0]))
        self.arrive = 0
        self.tour = 0
        self.voiture_total = 0
        self.affiches_tour = []
        self.affiche_densite_total_tab = []
        self.ajoute_voiture_case()
        self.densite_par_tour = [self.creer_tableau_densite()]
        self.prochain_mouvements = []
        
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

    def trouve_case_suivante(self, case, direction):
        if direction == Direction.HAUT:
            return self.route[case.y - 1][case.x]
        elif direction == Direction.BAS: 
            return self.route[case.y + 1][case.x]
        elif direction == Direction.DROITE: 
            return self.route[case.y][case.x + 1]
        else: 
            return self.route[case.y][case.x - 1]

    def creer_cycle(self, voiture, case, direction): #Direction designe haut ou bas
        if direction == Direction.HAUT: 
            if Direction.HAUT in case.direction_possible:
                voiture.prochain_mouvements.append(Direction.HAUT)
                case_suivante = self.trouve_case_suivante(case, Direction.HAUT)
                voiture.prochain_mouvements.append(case_suivante.direction_possible[1])
            else: 
                print("Ajout impossible car la direction du cycle est impossible")
        elif direction == Direction.BAS: 
            if Direction.BAS in case.direction_possible:
                voiture.prochain_mouvements.append(Direction.BAS)
                case_suivante = self.trouve_case_suivante(case, Direction.BAS)
                voiture.prochain_mouvements.append(case_suivante.direction_possible[1])
            else: 
                print("Ajout impossible car la direction du cycle est impossible")
        else: 
            print("La direction donnée en argument est invalide")

    def cycle_possible(self, case, direction): #Direction désigne haut ou bas
        if case.y != self.nbr_ligne - 1 and case.y != 0:
            return direction in case.direction_possible 
        else: 
            if case.y == self.nbr_ligne - 1: 
                return direction == Direction.HAUT and Direction.HAUT in case.direction_possible
            elif case.y == 0: 
                return direction == Direction.BAS and Direction.BAS in case.direction_possible
            else: 
                print("wtf")
                
                    
                

    def une_seule_direction_possible(self, case):
        return (case.direction_possible[0] != Direction.NONE and case.direction_possible[1] == Direction.NONE) or (case.direction_possible[0] == Direction.NONE and case.direction_possible[1] != Direction.NONE)

    def renvoie_direction_non_nulle(self, case):
        if case.direction_possible[0] != Direction.NONE: 
            return case.direction_possible[0]
        return case.direction_possible[1]

    def voiture_arrivee(self, voiture, case):
        if case.x == voiture.destination_colonne and case.y == voiture.destination_ligne:
            self.arrive += 1
            case.voiture.remove(voiture)
            case.retire_densite()
            return True
        return False

        
    def avance_direction(self, voiture, case): 

        if self.voiture_arrivee(voiture, case): #On vérifie si la voiture est arrivée
            return;

        # ajouter un cas si une des deux directions est nulle
        
        up_or_down = case.direction_possible[1] #Stockage des possibles directions
        left_or_right = case.direction_possible[0]
        #print(case.x, case.y)
        #print(left_or_right, up_or_down)

        if len(voiture.prochain_mouvements) != 0: 
            next_move = voiture.prochain_mouvements[0]
            #print(next_move)
            #print(case.direction_possible)
            assert(next_move in case.direction_possible)
            voiture.prochain_mouvements.remove(next_move)
            self.avance_voiture(case, voiture, self.trouve_case_suivante(case, next_move))

        else: 
            #print("Il n'y a pas de cycle en cours")
            if voiture.destination_ligne == case.y and voiture.destination_colonne < case.x and Direction.GAUCHE in case.direction_possible: 
                return self.avance_voiture(case, voiture, self.trouve_case_suivante(case, Direction.GAUCHE))
            elif voiture.destination_ligne == case.y and voiture.destination_colonne > case.x and Direction.DROITE in case.direction_possible: 
                return self.avance_voiture(case, voiture, self.trouve_case_suivante(case, Direction.DROITE))
            elif voiture.destination_colonne == case.x and voiture.destination_ligne < case.y and Direction.HAUT in case.direction_possible: 
                return self.avance_voiture(case, voiture, self.trouve_case_suivante(case, Direction.HAUT))
            elif voiture.destination_colonne == case.x and voiture.destination_ligne > case.y and Direction.BAS in case.direction_possible: 
                return self.avance_voiture(case, voiture, self.trouve_case_suivante(case, Direction.BAS))
            else: #On est pas dans une situation évidente ou l'objectif est sur la voie
                #On cherche d'abord à être sur une voie pour avoir l'objectif au dessus ou en bas 
                if voiture.destination_ligne < case.y and up_or_down == Direction.HAUT: #Si l'on est sur une case qui permet de rejoindre de façon directe en remontant on le prend 
                    #print("On est dans le cas 1")
                    #print(voiture.destination_ligne, voiture.destination_colonne)
                    #print("Longueur de ma liste : ", len(self.route[voiture.destination_ligne][voiture.destination_colonne].direction_possible))
                    if case.x < voiture.destination_colonne and self.route[voiture.destination_ligne][voiture.destination_colonne].direction_possible[0] == Direction.DROITE:
                        return self.avance_voiture(case, voiture, self.trouve_case_suivante(case, Direction.HAUT))
                    if case.x > voiture.destination_colonne and self.route[voiture.destination_ligne][voiture.destination_colonne].direction_possible[0] == Direction.GAUCHE:
                        return self.avance_voiture(case, voiture, self.trouve_case_suivante(case, Direction.HAUT))
                # Ajouter la même chose pour descendre
                if voiture.destination_ligne > case.y and up_or_down == Direction.BAS:
                    #print("On est dans le cas 2")
                    if case.x < voiture.destination_colonne and self.route[voiture.destination_ligne][voiture.destination_colonne].direction_possible[0] == Direction.DROITE:
                        return self.avance_voiture(case, voiture, self.trouve_case_suivante(case, Direction.BAS))
                    if case.x > voiture.destination_colonne and self.route[voiture.destination_ligne][voiture.destination_colonne].direction_possible[0] == Direction.GAUCHE:
                        return self.avance_voiture(case, voiture, self.trouve_case_suivante(case, Direction.BAS))

                """
                if voiture.destination_colonne < case.x + 1 and left_or_right == Direction.DROITE: 
                    return self.avance_voiture(case, voiture, self.trouve_case_suivante(case, Direction.DROITE))
                if voiture.destination_colonne > case.x - 1 and left_or_right == Direction.GAUCHE: 
                    return self.avance_voiture(case, voiture, self.trouve_case_suivante(case, Direction.GAUCHE))
                """
                # On doit faire un cycle
                if self.cycle_possible(case, up_or_down):
                    self.creer_cycle(voiture, case, up_or_down)
                    return self.avance_direction(voiture, case)
                if self.une_seule_direction_possible(case):
                    self.avance_voiture(case, voiture, self.trouve_case_suivante(case, self.renvoie_direction_non_nulle(case)))
                    return;
                """
                if voiture.destination_ligne <= case.y:
                    #print(case.y)
                    if self.cycle_possible(case, Direction.BAS):
                        self.creer_cycle(voiture, case, Direction.BAS)
                        return self.avance_direction(voiture, case);
                    if self.une_seule_direction_possible(case): # Cas ou un cycle n'est pas possible donc le cas normalement où il n'y a qu'une direction possible
                        self.avance_voiture(case, voiture, self.trouve_case_suivante(case, self.renvoie_direction_non_nulle(case)))
                        return;
                    else: 
                        #print(case.x, case.y)
                        print("Pas normal + je sais pas ce qui ce passe")
                        
                if voiture.destination_ligne > case.y:
                    #print(case.y)
                    if self.cycle_possible(case, Direction.HAUT):
                        self.creer_cycle(voiture, case, Direction.HAUT)
                        return self.avance_direction(voiture, case)
                    if self.une_seule_direction_possible(case): # Cas ou un cycle n'est pas possible donc le cas normalement où il n'y a qu'une direction possible
                        return self.avance_voiture(case,voiture, self.trouve_case_suivante(case, self.renvoie_direction_non_nulle(case)))
                    else:
                        print("Pas normal + je sais pas ce qui ce passe")
                        #print()
                    #print(case.y)
                pass #Créer un cycle pour pouvoir atteindre la bonne voie
                


                

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
       
    """

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
                    #voiture.ajoute_perturbation(proba, voiture.ralentir)
                    
                    self.avance_direction(voiture, case)
                    #print(voiture.vitesse)
                print("Nombre de voiture restante pour l'instant : ", self.voiture_total - self.arrive)
                print("Nombre de voiture total : ", self.voiture_total)
        self.affiche_densite_total()
        #print(self.route[19][19].densite)
        print(self.voiture_total - self.arrive)

    def check_tous_arrive(self): 
        return self.arrive == self.voiture_total 

    def affiche_densite_total(self):
        self.affiche_densite_total_tab.append(self.voiture_total - self.arrive)


