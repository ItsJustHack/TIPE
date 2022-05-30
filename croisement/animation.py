import pygame 
import time
import math

HAUTEUR =  800
LONGUEUR = 1200
COULEUR_ROUTE = "white"
COULEUR_VOIE = "black"
INTERVALLE = 0.1

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


def animate_frame(densite, screen, nbr_lignes, nbr_colonnes, liste_images):
    """Cette fonction affiche une frame"""
    for i, ligne in enumerate(densite) : 
        for j, case in enumerate(ligne):
            rect_actuel = pygame.Rect(j * (LONGUEUR / nbr_colonnes), i * (HAUTEUR / nbr_lignes), LONGUEUR / nbr_colonnes, HAUTEUR / nbr_lignes)
            couleur = 255 - case if 255 - case > 0 else 0
            pygame.draw.rect(screen, (couleur, couleur, couleur), rect_actuel)
            #couleur = case if case <= 255 else 255
            
            if (j%2 == 0 and i%2 == 0): 
                pygame.Surface.blit(screen, liste_images[0], (j * (LONGUEUR // nbr_colonnes), i * (HAUTEUR // nbr_lignes)))
            elif(j%2 == 0 and i%2 == 1): 
                pygame.Surface.blit(screen, liste_images[2], (j * (LONGUEUR // nbr_colonnes), i * (HAUTEUR // nbr_lignes)))
            elif(j%2 == 1 and i%2 == 1): 
                pygame.Surface.blit(screen, liste_images[3], (j * (LONGUEUR // nbr_colonnes), i * (HAUTEUR // nbr_lignes)))
            else: 
                pygame.Surface.blit(screen, liste_images[1], (j * (LONGUEUR // nbr_colonnes), i * (HAUTEUR // nbr_lignes)))
           
    #pygame.draw.polygon(screen, (0, 0, 0), ((0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0), (200, 100)))

	

def animate(nbr_lignes, nbr_colonnes, densite):
    
    # Chargement des images
    bas_gauche = pygame.image.load("TIPE_images/Bas_Gauche2.png")
    bas_droite = pygame.image.load("TIPE_images/Bas_Droite2.png")
    haut_gauche = pygame.image.load("TIPE_images/Haut_gauche2.png")
    haut_droite = pygame.image.load("TIPE_images/Haut_droit2.png")

    # Rescale des images
    bas_gauche = pygame.transform.scale(bas_gauche, (LONGUEUR / nbr_colonnes, HAUTEUR / nbr_lignes))
    bas_droite = pygame.transform.scale(bas_droite, (LONGUEUR / nbr_colonnes, HAUTEUR / nbr_lignes))
    haut_gauche = pygame.transform.scale(haut_gauche, (LONGUEUR / nbr_colonnes, HAUTEUR / nbr_lignes))
    haut_droite = pygame.transform.scale(haut_droite, (LONGUEUR / nbr_colonnes, HAUTEUR / nbr_lignes))

    liste_image = [haut_gauche, haut_droite, bas_gauche, bas_droite]

    screen = init_screen() 
    stop = False
    for tour in densite:
        if stop:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True
        animate_frame(tour, screen, nbr_lignes, nbr_colonnes, liste_image)
        #draw_routes(nbr_lignes, nbr_colonnes, screen)
        draw_voies(nbr_lignes, nbr_colonnes, screen)
        pygame.display.flip()
        time.sleep(INTERVALLE)
    #time.sleep(30)

#animate(2, 2, [[[7,49], [8, 38]], [[6,89], [6, 39]]])







