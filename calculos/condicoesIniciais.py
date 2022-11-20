"""
    Algumas condições iniciais que podem ser convenientes
"""

from math import sqrt, pi, cos, sin
from calculos.hamiltoniano import EC, U
import random

class condicoesIniciais:
    def __init__ (self, massas:list=[]):
        self.massas = massas
        self.qntdCorpos = len(massas)
        # par (1) ou ímpar (0)
        self.qntd_tipo = 1 if self.qntdCorpos % 2 == 0 else 0
    
    def juntar_ps (self, x, y, px, py):
        ps = []
        for i in range(self.qntdCorpos):
            ps += [x[i], px[i], y[i], py[i]]

    def gerar_massas (self, m_min: float, m_max:float, qntd:float, inteiras:bool=True):
        """Gera massas aleatórias num intervalo dado."""
        if inteiras: self.massas = [random.randint(m_min, m_max) for i in range(qntd)]
        else: self.massas = [random.randrange(m_min, m_max) for i in range(qntd)]
        self.qntdCorpos = len(self.massas)
        return self.massas


class condicoesArtigo (condicoesIniciais):
    def __init__ (self, massas:list=[]):
        super().__init__(massas)

    def circulo (self, raio:float):
        if len(self.massas) == 0: raise Exception("O vetor de massas está vazio.")

        # distância entre os corpos
        d = 2 * pi * raio / self.qntdCorpos

        # nesse caso, vai dar uma distância de d/2 do eixo das ordenadas
        l = d / 2
        R0 = []
        P0 = []
        i = 0
        while l <= pi * raio / 2:
            alpha = (0.5 * pi * raio - l)/raio

            xp = raio * cos(alpha)
            yp = raio * sin(alpha)

            R0.append([xp, yp])
            P0.append([-xp, -yp])

            fator1 = self.massas[4*i]/self.massas[4*i+1]
            R0.append([-fator1*xp, -fator1*yp])
            P0.append([xp, yp])

            R0.append([-xp, yp])
            P0.append([xp, -yp])

            fator2 = self.massas[4*i+2]/self.massas[4*i+3]
            R0.append([fator2*xp, -fator2*yp])
            P0.append([-xp, yp])

            l += d
            i += 1
        
        # calcula a energia potencial para saber da cinética
        ps = []
        for i in range(len(R0)):
            for j in range(len(R0[i])):
                ps.append(R0[i][j])
                ps.append(P0[i][j])
        
        fator = sqrt(-U(ps, self.massas)/EC(ps, self.massas))
        for i in range(self.qntdCorpos):
            P0[i] = [P0[i][0]*fator, P0[i][1]*fator]
        
        return R0, P0