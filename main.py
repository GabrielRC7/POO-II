# Example file showing a basic pygame "game loop"
import pygame
from batalha import Batalha, Guerreiro
from funcoes import desenha_grid

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 620))
clock = pygame.time.Clock()
running = True
linhas = True


guerreiro = Guerreiro('joao', 5, 1, 2, 'bla', 5, 1000, 1, 3)
arqueiro = Guerreiro('joao', 3, 1, 2, 'bla', 1, 600, 200, 5)
lanceiro = Guerreiro('joaoTBM', 2, 1, 2, 'lanca?', 1, 1500, 50, 3)

guerra = Batalha()

guerra.add_batalha(arqueiro, 3, 'esquerda') 
guerra.add_batalha(lanceiro, 3, 'esquerda')
guerra.add_batalha(guerreiro, 10, 'esquerda')


guerra.add_batalha(arqueiro, 3, 'direita')
guerra.add_batalha(lanceiro, 5, 'direita')
guerra.add_batalha(guerreiro, 4, 'direita')


guerra.preparar_batalha()



while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                linhas = not linhas

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    if linhas:
        desenha_grid(screen, 60)

    guerra.tick_guerra(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()


    clock.tick(60)  # limits FPS to 60

pygame.quit()