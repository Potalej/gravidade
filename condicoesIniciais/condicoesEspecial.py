from condicoesIniciais.condicoesIniciais import condicoesIniciais
from math import sqrt, sin, cos, pi
from calculos.hamiltoniano import U, EC


class condicoesArtigoEspecial (condicoesIniciais):
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