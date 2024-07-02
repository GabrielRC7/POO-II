import numpy as np
import pygame

class Guerreiro:
    def __init__(self, nome: str, forca: int, furia: bool, agilidade: int, arma: str, 
                    resistencia: int, saude: int, alcance: int, visao: int) -> None:

        self.nome = nome
        self.forca = forca
        self.furia = furia
        self.agilidade = agilidade
        self.arma = arma
        self.resistencia = resistencia
        self.saude = saude
        self.alcance = alcance
        self.visao = visao
        self.posicao: np.array = None
        self.id_exercito: int = None


    def desenhar(self, screen):
        cores = ["white", "blue"]
        pygame.draw.circle(screen, cores[self.id_exercito], self.posicao, 10)
        barra = pygame.rect.Rect(int(self.posicao[0]) - 5, int(self.posicao[1]), 10, 5)
        hp = pygame.rect.Rect(int(self.posicao[0]) - 5, int(self.posicao[1]), self.saude / 100, 5)
        pygame.draw.rect(screen, 'red', barra)
        pygame.draw.rect(screen, 'green', hp)


    def mover_reto(self, direita: bool):
        deslocamento = 1 + self.agilidade
        self.posicao[0] += deslocamento if direita else -deslocamento


    def acha_adjacente(self, grid: list, posicao_grid, ) -> list:
        linha_inicio = int(posicao_grid[0] - self.visao) if (posicao_grid[0] - self.visao) >= 0 else 0
        linha_fim = int(posicao_grid[0] + self.visao) if (posicao_grid[0] + self.visao) <= len(grid) else len(grid)

        coluna_inicio = int(posicao_grid[1] - self.visao) if (posicao_grid[1] - self.visao) >= 0 else 0
        coluna_fim = int(posicao_grid[1] + self.visao) if (posicao_grid[1] + self.visao) <= len(grid[0]) else len(grid[0])

        ret = []

        for visao_linha in range(linha_inicio, linha_fim):
            for visao_coluna in range(coluna_inicio, coluna_fim):
                for guerreiro in grid[visao_linha][visao_coluna]:
                    if guerreiro.id_exercito != self.id_exercito:
                        ret.append(guerreiro)

        return ret
    
    def acha_mais_proximo(self, disponiveis: list) -> list:
        mais_proximo = disponiveis[0]
        distancia_mais_proxima = np.linalg.norm(self.posicao - disponiveis[0].posicao)
        for guerreiro in disponiveis:
            distancia_atual = np.linalg.norm(self.posicao - guerreiro.posicao)
            if distancia_atual <= distancia_mais_proxima:
                mais_proximo = guerreiro
                distancia_mais_proxima = distancia_atual

        if distancia_mais_proxima <= 25 + self.alcance:
            return True, mais_proximo

        return False, mais_proximo

    def move_para_guerreiro(self, alvo) -> None:
        minha_posicao = self.posicao
        alvo_posicao = alvo.posicao
        vetor_diferenca = minha_posicao - alvo_posicao
        tamanho_diferenca = np.linalg.norm(vetor_diferenca)

        versor = vetor_diferenca / tamanho_diferenca
        self.move_vetorial(versor)

    def move_vetorial(self, deslocamento) -> None:
        self.posicao[0] -= deslocamento[0] * self.agilidade * 1.5
        self.posicao[1] -= deslocamento[1] * self.agilidade * 1.5

    def movimenta(self, grid, posicao_grid, direita):
        adjacentes = self.acha_adjacente(grid, posicao_grid)
        if adjacentes:
            inimigo_perto, alvo = self.acha_mais_proximo(adjacentes)

            if inimigo_perto:
                return alvo
            
            self.move_para_guerreiro(alvo)
            return None
                
        self.mover_reto(direita)

