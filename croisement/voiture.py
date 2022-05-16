from random import randint
VITESSE_MAX = 2

class Voiture: 
    #Définition de mon objet
    def __init__(self, nbr_ligne, nbr_colonne):
        self.vitesse = 1

        def destination_y():
            return randint(0, nbr_ligne-1)

        def destination_x():
            return randint(0, nbr_colonne - 1)

        self.destination_ligne = destination_y()
        self.destination_colonne = destination_x()

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
