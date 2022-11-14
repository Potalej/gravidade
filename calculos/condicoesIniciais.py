"""
    Algumas condições iniciais que podem ser convenientes
"""
from math import sqrt
from calculos.hamiltoniano import *
import random

class condicoesIniciais:
    def __init__ (self, massas:list=[]):
        self.massas = massas
        self.qntdCorpos = len(massas)

    def posicoes (self, intervalo:list, distancia_minima:float, inteiros:bool=True):
        a,b = intervalo
        x = random.sample(range(a, b, distancia_minima), self.qntdCorpos)
        y = random.sample(range(a, b, distancia_minima), self.qntdCorpos)
        return x, y
    
    def momentos (self, intervalo:list, inteiros:bool=True):
        a,b = intervalo
        x = [random.randrange(a, b) for i in range(self.qntdCorpos)]
        y = [random.randrange(a, b) for i in range(self.qntdCorpos)]
        return x, y

    def juntar_ps (self, x, y, px, py):
        ps = []
        for i in range(self.qntdCorpos):
            ps += [x[i], px[i], y[i], py[i]]
        return ps
    
    def energia_nula (self, intervalo_posicao:list, intervalo_momento:list):
        x,y = self.posicoes(intervalo_posicao[:2], intervalo_posicao[-1])
        px,py = self.momentos(intervalo_momento)
        ps = self.juntar_ps(x,y,px,py)

        fator = sqrt(-U(ps, self.massas)/EC(ps, self.massas))
        px = [pxi*fator for pxi in px]
        py = [pyi*fator for pyi in py]
        
        R = [[x[i], y[i]] for i in range(self.qntdCorpos)]
        P = [[px[i], py[i]] for i in range(self.qntdCorpos)]

        ps = self.juntar_ps(x,y,px,py)
        print(H(ps, self.massas))

        return R, P