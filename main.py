# Imports
import pygame
from batalha import Batalha, Guerreiro
from funcoes import desenha_grid

# Config pygame
pygame.init()
screen = pygame.display.set_mode((1280, 620))
clock = pygame.time.Clock()
running = True
linhas = False

# Adicionando fundo 
bg = pygame.image.load("bg.jpg")

# Definindo as características de cada guerreiro
guerreiro = Guerreiro(15, 2, 'Espada', 10, 1000, 1, 3, 5)
arqueiro = Guerreiro(10, 1, 'Arco', 4, 500, 200, 8, 6)
lanceiro = Guerreiro(8, 1.5, 'Lança', 8, 800, 50, 4, 5)

guerra = Batalha()

# Definindo os 2 exércitos
guerra.add_batalha(arqueiro, 6, 'esquerda') 
guerra.add_batalha(lanceiro, 4, 'esquerda')
guerra.add_batalha(guerreiro, 10, 'esquerda')

guerra.add_batalha(arqueiro, 6, 'direita')
guerra.add_batalha(lanceiro, 6, 'direita')
guerra.add_batalha(guerreiro, 8, 'direita')

# Iniciar batalha
guerra.preparar_batalha()

# Loop
dt = 60
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Revela o grid
            if event.key == pygame.K_DOWN:
                linhas = not linhas
                
            # Revela o alvo de cada guerreiro
            if event.key == pygame.K_UP:
                guerra.mostra_alvo = not guerra.mostra_alvo

            # Aumenta a velocidade da simulação 
            if event.key == pygame.K_RIGHT:
                dt = dt * 2
            
            # Diminui a velocidade da simulação
            if event.key == pygame.K_LEFT:
                dt = dt // 2

    screen.fill("black")

    screen.blit(bg, (0, 0))

    if linhas:
        desenha_grid(screen, 60)

    guerra.tick_guerra(screen)

    pygame.display.flip()

    clock.tick(dt)

pygame.quit()