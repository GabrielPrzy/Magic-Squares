from functools import reduce
import random
import pygame, random
from pygame.locals import *

class Magic_squares:
    def __init__(self):
        # Funções para trabalhar com números
        self.string = lambda n: str(n)
        self.separar = lambda n: [int(i) for i in self.string(n)]
        self.juntar = lambda l: reduce(self.somar, [str(i) for i in l])
        self.somar = lambda x, y: x + y
        self.somarDigitos = lambda n: reduce(self.somar, self.separar(n))

        # Retorna quanto falta para um número completar outro
        # ex: ec(8, 1) = 7, falta 7 pro 1 completar 8
        self.complemento = lambda k, v: [i if self.somarDigitos(int(self.juntar([k, i]))) == v else -1 for i in range(0, 16)]
        self.encontrar_complemento = lambda v, k: list(filter(lambda i: i != -1, self.complemento(k, v)))

        # Funções que retornam os dados de uma matriz
        self.index_central = lambda m: int((len(m) - 1)/2 + 1 - 1)
        self.cruz_matriz = lambda m: [[m[self.index_central(m)][i] for i in range(len(m))], [m[i][self.index_central(m)] for i in range(len(m))]]
        self.x_matriz = lambda m: [[m[i][i] for i in range(len(m))], [m[i][self.encontrar_complemento(8, i)[0]] for i in range(len(m))]]

        # Funções que somam e validam se um quadrado é mágico
        self.showSquare = lambda m: [print(i) for i in m]
        self.somaLinhas = lambda m: [sum(i) for i in m]
        self.somaX = lambda m: [sum(self.x_matriz(m)[0]), sum(self.x_matriz(m)[1])]
        self.somaColunas = lambda m: [sum([m[i][0] for i in range(len(m))]) for k in range(len(m))]
        self.comparador = lambda m: [self.somaX(m), self.somaLinhas(m), self.somaColunas(self.magic)]
        self.validar = lambda m: [True if sum(i) == len(i) * i[0] else False for i in m]

        # Inicializando o quadrado padrão
        self.criar_magic = lambda len: [[0,0,0,0,0,0,0,0,0] for i in range(int(len**(1/2)))]
        self.magic = self.criar_magic(81)
        self.padrao = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    # /////////////////////////////////////////////////////////////////////////////////////////////////////

    # Função que constrói o quadrado padrão
    def buildPattern(self, pattern):
        self.padrao = pattern
        self.magic[self.index_central(self.magic)] = self.padrao

        for i in range(len(self.magic)):
            self.magic[i][self.index_central(self.magic)] = self.padrao[i]

        #---------------------------------------------------------------------------- Cruz x

        for i in range(self.index_central(self.magic) + 1, len(self.magic)):
            self.magic[0][i] = self.padrao[i - self.index_central(self.magic)]

        for i in range(0, self.index_central(self.magic)):
            self.magic[0][i] = self.padrao[i + self.index_central(self.magic) + 1]

        #---------------------------------------------------------------------------- cruz y

        for i in range(self.index_central(self.magic) + 1, len(self.magic)):
            self.magic[-1][i] = self.padrao[i - self.index_central(self.magic) - 1]

        for i in range(self.index_central(self.magic)):
            self.magic[-1][i] = self.padrao[i - self.index_central(self.magic) - 1]

        #---------------------------------------------------------------------------- Diagonal direita-esquerda

        for k in range(8, 0, -1):
            for i in range(1, len(self.magic) - (self.encontrar_complemento(8, k)[0])):
                self.magic[i][self.encontrar_complemento(k, i)[0]] = self.magic[0][k]

        #---------------------------------------------------------------------------- Diagonal esquerda direita

        for k in range(1, 8):
            for i in range(k, len(self.magic)):
                self.magic[self.encontrar_complemento(k + 8, i)[0]][i] = self.magic[8][k]

    # /////////////////////////////////////////////////////////////////////////////////////////////////////

    # Função que gera um novo padrão a partir do padrão base
    def generateNums(self):
        pattern = [1,6,2,7,3,8,4,9,5]
        new_pattern = [0,0,0,0,0,0,0,0,0]

        # Multiplica cada número do padrão por n e gera um novo
        n = random.randint(1,50)
        nums = [i * n for i in pattern]

        # Reposiciona cada elemento do padrão com o novo número do padrão no padrão novo em ordem
        for k in range(len(nums)):
            for i in range(len(pattern)):
                if self.somarDigitos(self.somarDigitos(self.somarDigitos((nums[i])))) == pattern[k]:
                    new_pattern[k] = nums[i]

        return new_pattern

    # /////////////////////////////////////////////////////////////////////////////////////////////////////

    # Função que constrói um quadrado aleatório e reposiciona os elementos no quadrado padrão
    def Random_square(self, nums):
        square = []
        initial_pattern = nums

        for i in range(len(self.magic)):
            square.append([])

        for i in square:
            for k in range(len(self.magic)):
                i.append(0)

        nums.sort()

        # Reposiciona cada elemento do padrão com o novo número do padrão no quadrado novo
        for i in range(0, len(self.magic)):
            for k in range(0, len(self.magic)):
                for n in range(1, 10):
                    if self.magic[i][k] == n:
                        square[i][k] = int(nums[n - 1])
                        continue

        return [square, initial_pattern]

    # /////////////////////////////////////////////////////////////////////////////////////////////////////

    # Função que renderiza o novo quadrado criado
    def render(self, magic):
        screen = pygame.display.set_mode((595, 595))
        font = pygame.font.Font('freesansbold.ttf', 18)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        screen.fill((0, 0, 0))

        for x in range(0, 595, 66):
            pygame.draw.line(screen, (148, 189, 177), (x, 0), (x, 594))     # Draw vertical lines
        for y in range(0, 595, 66):
            pygame.draw.line(screen, (148, 189, 177), (0, y), (594, y))     # Draw horizontal lines

        passo = 66
        pos = -45

        # Definindo as distâncias dos elementos entre si
        n = [3.5 + (2.55 * i) for i in range(-1, 9)]
        n[0] = 1

        # Renderiza cada número do novo quadrado na grid
        for k in range(9):
            pos = -45
            for i in range(9):
                nums_font = font.render(str(magic[k][i]), True, (255, 255, 255))
                num_rect = nums_font.get_rect()
                pos += passo
                num_rect.topleft = (pos, n[k] * 26)
                screen.blit(nums_font, num_rect)

        # /////////////////////////////////////////////////////////////////////////////////////////////////////
