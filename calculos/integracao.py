"""
    Onde é feita a integração numérica via Runge-Kutta.
"""
from numpy import array, transpose, identity, einsum, true_divide, ones, ravel
from calculos.colisoes import verificaColisoes
from calculos.hamiltoniano import ajustar, H

class RK4:
    def __init__ (self, m:list, h:float=0.05):
        self.qntd = len(m)
        self.m = m

        self.m2vezesdiv = []
        for mi in m: self.m2vezesdiv += [1/mi, 1/mi]
        self.m2vezesdiv = array([self.m2vezesdiv])

        self.guardar_massas()
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
        
        Fsoma = []
        for linha in F:
            Fsoma += [0,0]
            for coluna in linha:
                Fsoma[-2] += coluna[0]
                Fsoma[-1] += coluna[1]
        return F, Fsoma

    def runge_kutta4(self, tn:list, yn, F, Fsoma):
        # separando a lista por posições e momentos
        P = [yn[1::2]]
        R = [yn[::2]]

        # faz a integração sobre as equações x'
        k1_vet = P*self.m2vezesdiv
        k1_1m = k1_vet*self.m2vezesdiv
        k1_2m = k1_1m*self.m2vezesdiv
        k1_3m = k1_2m*self.m2vezesdiv

        fator = (self.h/6) * (6*k1_vet + 3*self.h*k1_1m + self.h**2 * k1_2m + 0.25*self.h**3 * k1_3m)
        posicoes = R + fator

        # integração sobre as equações p'
        vetores_forcas = P[0] + self.h*array([Fsoma])

        # intercalando
        yn1 = ravel([posicoes[0], vetores_forcas[0]], order="F")

        return tn + self.h, yn1

    def aplicarNVezes (self, tn:float, yn:list, n=1, E=0):
        for _ in range(n):
            F, Fsoma = self.forcas(yn)
            tn, yn = self.runge_kutta4(tn, yn, F, Fsoma)
            yn, houve_colisao = verificaColisoes(self.m, yn)
            # tem que fazer a correção aqui
            # if not houve_colisao:
            #     yn, e = ajustar(self.f, tn, yn, self.m, E, F)
            # yn, e = ajustar(self.f, tn, yn, self.m, E, F)

        return tn, yn, F
