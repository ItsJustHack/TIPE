"""Implémentation du modèle de Nagel-Schreckenberg"""

"""Ce modèle a pour but de modéliser les intersections acec 
les interactions avec des feux"""

VITESSE_MAX = 2
MAX_DENSITE = 4
DENSITE_ACCIDENT = 50

from route import Route
from animation import animate

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
    """
    for route in route1.route: 
        for case in route: 
            print(case.direction_possible)
    """
    
    animate(nbr_ligne, nbr_colonne, route1.densite_par_tour)

main(10, 10)
