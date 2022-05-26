import pygame 
import time
import math

HAUTEUR =  600
LONGUEUR = 600
COULEUR_ROUTE = "white"
COULEUR_VOIE = "black"
INTERVALLE = 0.1

"""Ce fichier a pour but d'animer les densités des 
cases au cours du temps"""

bas_gauche = pygame.image.load("TIPE_images/Bas_Gauche.png")
bas_droite = pygame.image.load("TIPE_images/Bas_Droite.png")
haut_gauche = pygame.image.load("TIPE_images/Haut_gauche.png")
haut_droite = pygame.image.load("TIPE_images/Haut_droit.png")

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
            #couleur = case if case <= 255 else 255
            pygame.draw.rect(screen, (couleur, 0, 0), rect_actuel)
            screen.blit(haut_gauche, (0,0))
            """
            if (j%2 == 0 and i%2 == 0): 
                pygame.draw.rect(screen, (couleur, couleur, 255), rect_actuel)
            elif(j%2 == 0 and i%2 == 1): 
                pygame.draw.rect(screen, (couleur, 0, 255), rect_actuel)
            elif(j%2 == 1 and i%2 == 1): 
                pygame.draw.rect(screen, (couleur, 255, couleur), rect_actuel)
            else: 
                pygame.draw.rect(screen, (0, couleur, 0), rect_actuel)
            """
    #pygame.draw.polygon(screen, (0, 0, 0), ((0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0), (200, 100)))

	

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







