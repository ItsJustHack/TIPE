from case import Case
from case import Direction
from random import randint 

MAX_DENSITE = 200


class Route : 
    def __init__(self, nbr_ligne, nbr_colonne):
        #randint(0, MAX_DENSITE))
        self.compteur1 = 0
        self.compteur2 = 0
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

        if len(voiture.prochain_mouvements) != 0: 
            next_move = voiture.prochain_mouvements[0]
            assert(next_move in case.direction_possible)
            voiture.prochain_mouvements.remove(next_move)
            self.avance_voiture(case, voiture, self.trouve_case_suivante(case, next_move))

        else: 

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
                    self.compteur1 += 1
                    if case.x < voiture.destination_colonne and self.route[voiture.destination_ligne][voiture.destination_colonne].direction_possible[0] == Direction.DROITE:
                        return self.avance_voiture(case, voiture, self.trouve_case_suivante(case, Direction.HAUT))
                    if case.x > voiture.destination_colonne and self.route[voiture.destination_ligne][voiture.destination_colonne].direction_possible[0] == Direction.GAUCHE:
                        return self.avance_voiture(case, voiture, self.trouve_case_suivante(case, Direction.HAUT))
                # Ajouter la même chose pour descendre
                if voiture.destination_ligne > case.y and up_or_down == Direction.BAS:
                    self.compteur2 += 1
                    if case.x < voiture.destination_colonne and self.route[voiture.destination_ligne][voiture.destination_colonne].direction_possible[0] == Direction.DROITE:
                        return self.avance_voiture(case, voiture, self.trouve_case_suivante(case, Direction.BAS))
                    if case.x > voiture.destination_colonne and self.route[voiture.destination_ligne][voiture.destination_colonne].direction_possible[0] == Direction.GAUCHE:
                        return self.avance_voiture(case, voiture, self.trouve_case_suivante(case, Direction.BAS))

                # On doit faire un cycle
                if self.cycle_possible(case, up_or_down):
                    self.creer_cycle(voiture, case, up_or_down)
                    return self.avance_direction(voiture, case)
                if self.une_seule_direction_possible(case):
                    self.avance_voiture(case, voiture, self.trouve_case_suivante(case, self.renvoie_direction_non_nulle(case)))
                    return;

                print("Pas normal")

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
                for voiture in case.voiture:
                    voiture.ajoute_vitesse()
                    proba = (case.densite*100)//MAX_DENSITE
                    voiture.ajoute_perturbation(proba, voiture.ralentir)
                    self.avance_direction(voiture, case)
        print("Nombre de voiture restante pour l'instant : ", self.voiture_total - self.arrive)
        print("Compteur1 = ", self.compteur1, "Compteur2 = ", self.compteur2)
        self.affiche_densite_total()

    def check_tous_arrive(self): 
        return self.arrive == self.voiture_total 

    def affiche_densite_total(self):
        self.affiche_densite_total_tab.append(self.voiture_total - self.arrive)


