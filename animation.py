import pygame 
import time

HAUTEUR = 600 
LONGUEUR = 800
COULEUR = "black"

"""Ce fichier a pour but d'animer les densités des 
cases au cours du temps"""

def init_screen():
    # Initialisation de l'écran
    pygame.init()
    screen = pygame.display.set_mode((LONGUEUR, HAUTEUR))
    pygame.display.set_caption("Animation traffic")
    return screen

def draw_rectangles(nbr_lignes, nbr_colonnes, screen): 
    """fonction pygame"""


    for i in range(nbr_lignes):
        pygame.draw.line(screen, COULEUR, (0, i*(HAUTEUR / nbr_lignes)), (LONGUEUR, i*(HAUTEUR / nbr_lignes)), width=1)

    for j in range(nbr_colonnes):
        pygame.draw.line(screen, COULEUR, (j * (LONGUEUR / nbr_colonnes), 0), (j * (LONGUEUR / nbr_colonnes), HAUTEUR), width=1)

    pygame.display.flip()


def animate_frame(densite, screen, nbr_lignes, nbr_colonnes):
    for i, ligne in enumerate(densite) : 
        for j, case in enumerate(ligne):
            rect_actuel = pygame.Rect(i * (LONGUEUR / nbr_colonnes), j * (HAUTEUR / nbr_lignes), LONGUEUR / nbr_colonnes, HAUTEUR / nbr_lignes)
            #pygame.draw.rect(screen, (0, 255 - case.densite, 255), rect_actuel)
            pygame.draw.rect(screen, (0, 255 - case, 255), rect_actuel)

def animate(nbr_lignes, nbr_colonnes, densite):
    screen = init_screen() 
    for tour in densite:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break;
        animate_frame(tour, screen, nbr_lignes, nbr_colonnes)
        draw_rectangles(nbr_lignes, nbr_colonnes, screen)
        pygame.display.flip()
        time.sleep(0.1)

#animate(2, 2, [[[7,49], [8, 38]], [[6,89], [6, 39]]])







