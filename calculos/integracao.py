"""
    Onde é feita a integração numérica via Runge-Kutta.
"""
from numpy import array, transpose, identity, einsum, true_divide, ones
from calculos.colisoes import verificaColisoes
from calculos.hamiltoniano import ajustar, H
from time import time

class RK4:
    def __init__ (self, m:list, f:list, h:float=0.05):
        self.qntd = len(m)
        self.m = m
        self.guardar_massas()
        self.f = f # funções
        self.h = h
        self.A = [array([]), array([1/2]), array([0,1/2]), array([0,0,1])]
        self.A = [Ai * h for Ai in self.A]
        self.B = self.h * array([0,1/2,1/2,1])
        self.C = self.h * array([0,1/2,1/2,1])
        self.tempork4 = []

    def guardar_massas (self):
        """Armazena os produtos das massas em uma matriz"""
        MA = array([
            [0 if j == i else self.m[j] for j in range(self.qntd)]
        for i in range(self.qntd)])
        self.prodM = MA * transpose(MA)

    def forcas (self, yk):
        # coordenadas
        X = [[[yk[4*i], yk[4*i+2]]] for i in range(self.qntd)]
        # matriz X cheia
        X_cheia = einsum('ij,ijk->ijk', ones((self.qntd, self.qntd)), X)
        # matriz identidade
        I_n = identity(self.qntd)
        # matriz X sem a diagonal
        X = X_cheia - einsum('ij,ijk->ijk', I_n, X)
        # diferença
        difX = X - X.transpose(1,0,2)
        # norma
        norma = (einsum('ijk,ijk->ij', difX, difX))**(3/2) + I_n
        # matriz de forças
        F = true_divide(self.prodM, norma)
        F = einsum('ij,ijk->ijk', -F, difX)
        return F

    def runge_kutta4(self, tn:list, yn:list, F):
        yn1 = []
        for indice, fi in enumerate(self.f):
            tk = time()
            # k1 = h f(x0,y0)
            k1 = self.h*fi(tn, F, *yn)

            # k2 = hf(x0 + 0.5*h, y0 + 0.5*k1)
            k2 = self.h*fi(tn + 0.5*self.h, F, *[yni + 0.5*k1 for yni in yn])

            # k3 = hf(x0 + 0.5*h, 60 + 0.5*k2)
            k3 = self.h*fi(tn + 0.5*self.h, F, *[yni + 0.5*k2 for yni in yn])

            # k4 = hf(x0 + h, y0 + k3)
            k4 = self.h*fi(tn + self.h, F, *[yni + k3 for yni in yn])
            
            y1 = yn[indice] + (1/6) * (k1 + 2*k2 + 2*k3 + k4)
            yn1.append(y1)
            self.tempork4.append(time() - tk)
        return tn + self.h, yn1

    def runge_kutta4_geral(self, tn:list, yn:list, F): # mais lenta
        yn1 = []
        for indice, fi in enumerate(self.f):
            kappas = []
            tk = time()
            kappas.append(fi(tn+self.C[0]*self.h, F, *yn))
            for i in range(1,4):
                ein = einsum('i,i', self.A[i], array(kappas))
                kappa = yn + ein
                kappas.append(fi(tn+self.C[i], F, *kappa))
            y1 = yn[indice] + einsum('i,i', array(kappas), self.B)
            yn1.append(y1)
            self.tempork4.append(time() - tk)
        return tn + self.h, yn1

    def aplicarNVezes (self, tn:float, yn:list, n=1, E=0):
        for _ in range(n):
            F = self.forcas(yn)
            tn, yn = self.runge_kutta4(tn, yn, F)
            yn, houve_colisao = verificaColisoes(self.m, yn)
            # tem que fazer a correção aqui
            # if not houve_colisao:
            #     yn, e = ajustar(self.f, tn, yn, self.m, E, F)

        return tn, yn, F
