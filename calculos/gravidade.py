"""
    Gera as equações de movimento e faz o controle geral dos eventos de gravidade.
"""

from numpy import array, sqrt, einsum

class Gravidade:

    def __init__ (self, massas=list, dim:int=2, G:float=1)->None:
        self.massas = massas
        self.dim = dim
        self.G = G

        self.equacoes = [ self.geraEquacoes(a) for a in range(len(self.massas)) ]

    def r_ab (self, r1:list, r2:list)->float:
        """ Distância euclidiana entre dois pontos. """
        r1_ = array(r1)
        r2_ = array(r2)
        dif = r1_ - r2_
        return sqrt(einsum('i,i', dif, dif))

    def geraEquacoes (self, a:int)->list:
        """ Gera as equações de movimento e momento para um corpo `a`."""
        eq = []

        for i in range(self.dim):
            # função do x'
            eq.append(
                lambda t, F, *Ps, a=a, i=i, ma=self.massas[a]: Ps[4*a+2*i+1]/ma
            )
            # função do p'
            def func_p (t, F, *Ps, a=a, i=i, m=self.massas):
                soma = 0
                for b in range(len(m)):
                    if b != a:
                        el = F[a][b][i]
                        soma += el
                total = soma
                return total
            eq.append(func_p)
        return eq