from animacao.animacao import Animacao
from config.configs import animacao
from calculos.auxiliares import momento_inercia_cm
from calculos.integracao import RK4 as metodo_integracao
from calculos.hamiltoniano import H, U
from time import time

QUANTIDADE_ANTES_SALVAR = animacao['QUANTIDADE_ANTES_SALVAR']

class Simulacao (Animacao):

    def __init__ (self, massas:list, R0:list, P0:list, h:float=0.05, G:float=1, titulo='Animação'):
        
        self.massas = massas
        self.quantidade_corpos = len(self.massas)
        
        self.R, self.P = R0, P0

        # inciializa o método
        self.h = h
        self.metodo = metodo_integracao(self.massas, self.h, G)
        
        # energia inicial
        self.E0 = H(self.R, self.P, self.massas)
        self.E = self.E0

        # título
        self.titulo = titulo

    def funcaoLimitada (self):
        for _ in range(self.qntdFrames):
            self.R, self.P, self.F = self.metodo.aplicarNVezes(self.R, self.P, n=10, E=self.E0)
            self.E = H(self.R, self.P, self.massas)
            self.V = U(self.R, self.massas)
            yield self.R, self.P, self.E
    
    def funcaoIlimitada (self):
        while True:
            self.R, self.P, self.F = self.metodo.aplicarNVezes(self.R, self.P, n=10, E=self.E0)
            self.E = H(self.R, self.P, self.massas)
            self.V = U(self.R, self.massas)
            yield self.R, self.P, self.E
    
    def funcaoIlimitadaIcm (self):
        self.R, self.P, self.F = self.metodo.aplicarNVezes(self.R, self.P, n=100, E=self.E0)
        self.E = H(self.R, self.P, self.massas)
        self.V = U(self.R, self.massas)
        I = momento_inercia_cm(self.massas, self.R)
        C = self.complexidade(I)
        self.r.data_source.stream({'x': [self.i], 'y': [C]})
        self.i += 1
        # return self.R, self.P, self.E
    
    def simular (self, exibir=True, salvar=False, qntdFrames=0, nomeArquivo='pontos.txt'):
        """"""
        self.salvar_cores(self.quantidade_corpos)
        self.qntdFrames = qntdFrames
        print("E0: ", self.E0)
        if exibir:
            # inicia o PyGame
            self.iniciarPyGame(self.titulo)
            funcao = self.funcaoIlimitada if qntdFrames == 0 else self.funcaoLimitada
            self.animar(funcao, salvar)
        else:
            # se não quiser exibir, é óbvio que vai salvar
            YK = []
            self.abrirArquivo(self.massas, nomeArquivo)
            for frame in self.funcaoLimitada():
                R, P, E = frame
                yk = []
                x, y = list(zip(*R))
                px, py = list(zip(*P))
                for i in range(self.quantidade_corpos):
                    yk += [x[i], px[i], y[i], py[i]]
                YK.append(yk)
                if len(YK) == QUANTIDADE_ANTES_SALVAR:
                    self.salvarPontos(YK, nomeArquivo)
                    qnts += len(YK)
                    YK = []
            if len(YK) >= 0:
                self.salvarPontos(YK, nomeArquivo)   

    # PROVISÓRIO
    def complexidade (self, I):
        L_rms = (I**.5)/self.mtot
        L_mhl = (self.mtot**2)/abs(self.V)
        C = L_rms/L_mhl
        return C

    def simularMomentoInercia (self, qntdFrames=1):
        """Para testar o momento de inércia."""
        self.qntdFrames = qntdFrames
        I = []
        YK = []
        C = []
        E_total = []
        self.mtot = sum(self.massas)
        tempo = []
        tempo0 = time()
        for frame in self.funcaoLimitada():
            tempo.append(time() - tempo0)
            R, P, E = frame
            YK.append(R)
            I.append(momento_inercia_cm(self.massas, R))
            C.append(self.complexidade(I[-1]))
            E_total.append(E)
            tempo0 = time()
        return I, E_total, C, YK, tempo