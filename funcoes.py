import pygame

def desenha_grid(screen, jump):
    x = 0
    while x < 1280:
        pygame.draw.line(screen,"white", [x, 0], [x, 620])
        x += jump

    y = 0

    while y < 620:
        pygame.draw.line(screen,"white", [0 , y], [1280, y])
        y += jump

    pygame.draw.line(screen, "white", [1279, 0], [1279, 620])
    pygame.draw.line(screen, "white", [0, 619], [1280, 619])
