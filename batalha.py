# Imports
from guerreiro import Guerreiro
import numpy as np

# Classe Batalha
class Batalha:
    def __init__(self) -> None:
        self.grid = [[[] for _ in range(22)] for _ in range(11)]
        self.exercitos = {}
        self.mostra_alvo = False
        
    def add_batalha(self, entidade: Guerreiro, quantidade: int, exercito: str):
        
        if not self.exercitos.get(exercito):
            self.exercitos[exercito] = []
            
        temp = []
        for _ in range(quantidade):
            temp.append(entidade)

        self.exercitos[exercito].append(temp)

    # Prepara a batalha
    def preparar_batalha(self):
        numero_exercitos = len(self.exercitos)
        assert numero_exercitos <= 2, f"Essa versão ainda nao suporta mais de 2 exercitos ({self.exercitos.keys()})"
        assert numero_exercitos == 2, f"é necessario 2 exercitos para lutar ({self.exercitos.keys()})"

        nome_exercitos = list(self.exercitos.keys())

        self.gerar_posicoes(nome_exercitos[0], True)
        self.gerar_posicoes(nome_exercitos[1], False)

    # Gera as posições inicias de cada guerreiro no seu exército
    def gerar_posicoes(self, id, primeiro):
        exercito = self.exercitos[id]

        posicao_x = 15 if primeiro else 1265
        salto_x = 30 if primeiro else -30

        grid_x = 0 if primeiro else 20        

        for fileira in exercito:
            salto_y = 620 / (len(fileira) + 1)
            for contagem, guerreiro in enumerate(fileira, 1):
                posicao_y = salto_y * contagem
                grid_y = posicao_y // 60

                posicao = np.array([posicao_x, posicao_y])
                id_exercito = int(primeiro)

                self.grid[int(grid_y)][int(grid_x)].append(self.novo_guerreiro(guerreiro, posicao, id_exercito))

            posicao_x += salto_x
            grid_x = posicao_x // 60
        else:
            guerreiro.id_exercito = 123

    # Define o id do guerreiro
    def print_ids_grid(self):
        for linha in self.grid:
            for coluna in linha:
                if len(coluna) > 0:
                    for guerreiro in coluna:
                        print(guerreiro.id_exercito, end=",")
                else:
                    print("-", end="")
                print(" ", end="")
            print()

    # Define o guerreiro
    def novo_guerreiro(self, guerreiro, posicao, id):
        temp = Guerreiro(guerreiro.forca, guerreiro.agilidade,
                         guerreiro.arma, guerreiro.resistencia, guerreiro.saude, guerreiro.alcance, guerreiro.visao, 
                         guerreiro.ataque_speed)
        
        temp.id_exercito = id
        temp.posicao = np.array(posicao)
        
        return temp
    
    # Move os guerreiros e atualiza sua posição no grid a cada tick
    def tick_guerra(self, screen):
        guerreiro: Guerreiro
        for linha_index, linha in enumerate(self.grid):
            for coluna_index, coluna in enumerate(linha):
                for index, guerreiro in enumerate(coluna):
                    alvo = guerreiro.movimenta(self.grid, [linha_index, coluna_index], guerreiro.id_exercito)
                    
                    if alvo:
                        self.lutar(guerreiro, alvo, screen)

                    grid_x = int(guerreiro.posicao[0] // 60)
                    grid_y = int(guerreiro.posicao[1] // 60)

                    self.grid[grid_y][grid_x].append(guerreiro)

                    del(self.grid[linha_index][coluna_index][index])

        self.desenha_guerra(screen)

    def desenha_guerra(self, screen):
        for linha in self.grid:
            for coluna in linha:
                for guerreiro in coluna:
                    guerreiro.desenhar(screen)

    # Quando um alvo entra na sua distancia de ataque, começa a luta
    def lutar(self, agressor, vitima, screen): 
        agressor.ataque_cd += 1

        if agressor.ataque_cd >= 60 / agressor.ataque_speed:
            dano = agressor.forca - vitima.resistencia
            vitima.saude -= dano if dano > 10 else 10
            agressor.ataque_cd = 0

        if self.mostra_alvo:
            agressor.desenha_alvo(vitima, screen)

        if vitima.saude <= 0:
            posicao_vitima = vitima.posicao
            grid_x = int(posicao_vitima[0]) // 60
            grid_y = int(posicao_vitima[1]) // 60
            self.grid[grid_y][grid_x].remove(vitima)


