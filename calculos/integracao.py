"""
    Integração numérica via Runge-Kutta de 4ª ordem (RK4).
"""

from numpy import array, transpose, identity, ones, einsum, true_divide
from calculos.colisoes import verificaColisoes

class RK4:

    """
        O método RK4 já se encontra adaptado para as condições
        de sistemas de partículas do problema inicial. Uma versão
        mais generalizada pode ser encontrada em commits antigos.

        Parâmetros
        ----------
        massas : list
            Lista de massas das partículas.
        h : float = 0.05
            Tamanho do passo de integração.
        G : float = 1
            Constante de gravitação universal.
    """

    def __init__ (self, massas:list, h:float=0.05, G:float=1):

        # quantidade de partículas
        self.qntd = len(massas)

        # passo de integração
        self.h = h

        # constante de gravitação universal
        self.G = G

        # monta os vetores de massas
        self.guardar_massas(massas)

        self.vetorUm = ones((self.qntd, self.qntd))
        self.identidade = identity(self.qntd)

    def guardar_massas (self, massas:list)->None:
        """
            Guarda a lista de massas passadas nas formas
            de matriz (`prodM`) e vetor de massas inversas.

            Parâmetros
            ----------
            massas : list
                Lista de massas das partículas.
        """
        # vetor de massas
        self.massas = array(massas)

        # vetor de massas invertidas
        self.massasDuplicadasInvertidas = []
        for mi in massas: self.massasDuplicadasInvertidas += [[1/mi, 1/mi]]
        self.massasDuplicadasInvertidas = array(self.massasDuplicadasInvertidas)

        # matriz de produto de massas (facilita o cálculo das forças)
        MA = array([
            [0 if j == i else self.massas[j] for j in range(self.qntd)]
        for i in range(self.qntd)])
        self.prodM = MA * transpose(MA)
    
    def forcas (self, R)->tuple:
        """
            Monta a matriz de forças entre cada partícula e a matriz de soma das forças
            para cada partícula.

            Parâmetros
            ----------
            R : np.array
                Vetor de posições das partículas.
        """
        # coordenadas
        X = [[Ri] for Ri in R]
        # matriz X cheia
        X_cheia = einsum('ij,ijk->ijk', self.vetorUm, X)
        # matriz X sem a diagonal
        X = X_cheia - einsum('ij,ijk->ijk', self.identidade, X)
        # diferença
        difX = X - X.transpose(1,0,2)
        # norma
        norma = einsum('ijk,ijk->ij', difX, difX)**(3/2) + self.identidade
        # matriz de forças
        F = true_divide(self.prodM, norma)
        F = self.G*einsum('ij,ijk->ijk', -F, difX)

        # matriz de soma das forças
        FSomas = []
        for linha in F:
            FSomas += [[0,0]]
            for coluna in linha:
                FSomas[-1][0] += coluna[0]
                FSomas[-1][1] += coluna[1]
        return F, array(FSomas)

    def runge_kutta4 (self, R, P, FSomas):
        """
            Método RK4 adaptado para os sistemas em questão.
        """
        # faz a integração sobre as equações x'
        k1_vet = P*self.massasDuplicadasInvertidas
        k1_1m = k1_vet*self.massasDuplicadasInvertidas
        k1_2m = k1_1m*self.massasDuplicadasInvertidas
        k1_3m = k1_2m*self.massasDuplicadasInvertidas

        fator = (self.h/6) * (6*k1_vet + 3*self.h*k1_1m + self.h**2 * k1_2m + 0.25*self.h**3 * k1_3m)
        novas_posicoes = R + fator

        # integração sobre as equações p'
        novos_momentos = P + self.h*FSomas

        return novas_posicoes, novos_momentos

    def aplicarNVezes (self, R, P, n=1, E=0):
        for _ in range(n):
            F, FSomas = self.forcas(R)
            R, P = self.runge_kutta4(R, P, FSomas)
            R, P, houve_colisao = verificaColisoes(self.massas, R, P)
        return R, P, F 