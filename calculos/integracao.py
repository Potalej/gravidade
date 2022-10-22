"""
    Onde é feita a integração numérica via Runge-Kutta.
"""
from numpy import array, transpose, identity, einsum, true_divide, ones
from calculos.colisoes import verificaColisoes

class RK4:
    def __init__ (self, m:list, f:list, h:float=0.05):
        self.qntd = len(m)
        self.m = m
        self.guardar_massas()
        self.f = f # funções
        self.A = [[], array([1/2]), array([0,1/2]), array([0,0,1])]
        self.B = array([0,1/2,1/2,1])
        self.C = array([0,1/2,1/2,1])
        self.h = h

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
            kappas = []
            for i in range(4):
                kappa = yn + self.h * einsum('i,i', self.A[i], kappas)
                kappas.append(fi(tn+self.C[i]*self.h, F, *kappa))
            y1 = yn[indice] + self.h * einsum('i,i', array(kappas), self.B)
            yn1.append(y1)
        return tn + self.h, yn1

    def aplicarNVezes (self, tn:float, yn:list, n=1):
        for _ in range(n):
            F = self.forcas(yn)
            tn, yn = self.runge_kutta4(tn, yn, F)
            yn = verificaColisoes(self.m, yn)
        return tn, yn, F
