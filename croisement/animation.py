import pygame 
import time

HAUTEUR =  800
LONGUEUR = 800
COULEUR_ROUTE = "black"
COULEUR_VOIE = "white"
INTERVALLE = 0.3

"""Ce fichier a pour but d'animer les densités des 
cases au cours du temps"""

def init_screen():
    # Initialisation de l'écran
    pygame.init()
    screen = pygame.display.set_mode((LONGUEUR, HAUTEUR))
    pygame.display.set_caption("Animation traffic")
    return screen

def draw_voies(nbr_lignes, nbr_colonnes, screen):
    for i in range(nbr_lignes // 2):
        pygame.draw.line(screen, COULEUR_VOIE, (0, 2*i*(HAUTEUR / nbr_lignes) + (HAUTEUR / nbr_lignes)), (LONGUEUR, 2*i*(HAUTEUR / nbr_lignes)+ (HAUTEUR / nbr_lignes)), width=3)

    for j in range(nbr_colonnes // 2):
        pygame.draw.line(screen, COULEUR_VOIE, (2*j * (LONGUEUR / nbr_colonnes)+ (LONGUEUR / nbr_lignes), 0), (2*j * (LONGUEUR / nbr_colonnes)+ (LONGUEUR / nbr_lignes), HAUTEUR), width=3)

    pygame.display.flip()



def draw_routes(nbr_lignes, nbr_colonnes, screen): 
    """fonction pygame"""
    for i in range(nbr_lignes // 2 ):
        pygame.draw.line(screen, COULEUR_ROUTE, (0, 2*i*(HAUTEUR / nbr_lignes)), (LONGUEUR, 2*i*(HAUTEUR / nbr_lignes)), width=1)

    for j in range(nbr_colonnes // 2):
        pygame.draw.line(screen, COULEUR_ROUTE, (2*j * (LONGUEUR / nbr_colonnes), 0), (2*j * (LONGUEUR / nbr_colonnes), HAUTEUR), width=1)

    pygame.display.flip()


def animate_frame(densite, screen, nbr_lignes, nbr_colonnes):
    """Cette fonction affiche une frame"""
    for i, ligne in enumerate(densite) : 
        for j, case in enumerate(ligne):
            rect_actuel = pygame.Rect(j * (LONGUEUR / nbr_colonnes), i * (HAUTEUR / nbr_lignes), LONGUEUR / nbr_colonnes, HAUTEUR / nbr_lignes)
            couleur = 255 - case if 255 - case > 0 else 0
            pygame.draw.rect(screen, (0, couleur, 255), rect_actuel)


def animate(nbr_lignes, nbr_colonnes, densite):
    screen = init_screen() 
    stop = False
    for tour in densite:
        if stop:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True
        animate_frame(tour, screen, nbr_lignes, nbr_colonnes)
        draw_routes(nbr_lignes, nbr_colonnes, screen)
        draw_voies(nbr_lignes, nbr_colonnes, screen)
        pygame.display.flip()
        time.sleep(INTERVALLE)
    #time.sleep(30)

#animate(2, 2, [[[7,49], [8, 38]], [[6,89], [6, 39]]])







