from calculos.gravidade import Gravidade
from calculos.integracao import RK4 as metodo_integracao
from calculos.hamiltoniano import H, U
from animacao.animacao import Animacao
from config.configs import animacao
from calculos.auxiliares import momento_inercia_cm_ps

QUANTIDADE_ANTES_SALVAR = animacao['QUANTIDADE_ANTES_SALVAR']

class Simulacao (Animacao):
    def __init__ (self, m:list, R0:list, P0:list, h:float=0.05, G:float=1, titulo="Animação"):
        """
            Informar condições iniciais.

            Parâmetros
            ----------
            m : list
                Lista de massas dos corpos.
            R0 : list
                Posições iniciais.
            P0 : list
                Momentos iniciais.
        """
        self.massas = m
        self.quantidade_corpos = len(m)
        self.R0, self.P0 = R0, P0
        # estabelecendo condições iniciais
        self.condicoesIniciais()
        # gerando as equações
        g = Gravidade(self.massas, G=G)
        equacoes = []
        for equacao in g.equacoes: equacoes += equacao
        # inicializa o método
        self.h = h
        self.metodo = metodo_integracao(m = self.massas, f = equacoes, h = self.h)
        # energia inicial
        self.E0 = H(self.yk, self.massas) 
        self.E = self.E0 # energia
        # titulo
        self.titulo = titulo
    
    def condicoesIniciais (self):
        self.tk, self.yk = 0, []
        for corpo in range(self.quantidade_corpos):
            for i in range(2): # 2 é a dimensão do espaço
                self.yk.append(self.R0[corpo][i])
                self.yk.append(self.P0[corpo][i])

    def funcaoLimitada (self):
        for _ in range(self.qntdFrames):
            self.tk, self.yk, self.F = self.metodo.aplicarNVezes(self.tk, self.yk, n=10, E=self.E0)
            self.E = H(self.yk, self.massas)
            self.V = U(self.yk, self.massas)
            yield [*self.yk[::2], self.E]    
    
    def funcaoIlimitada (self):
        while True:
            self.tk, self.yk, self.F = self.metodo.aplicarNVezes(self.tk, self.yk, n=10, E=self.E0)
            self.E = H(self.yk, self.massas)
            yield [*self.yk[::2], self.E]    

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
                yk = frame[:-1]
                E = frame[-1]
                YK.append(frame)
                if len(YK) == QUANTIDADE_ANTES_SALVAR:
                    self.salvarPontos(YK, nomeArquivo)
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
        for frame in self.funcaoLimitada():
            yk = frame[:-1]
            YK.append(yk)
            I.append(momento_inercia_cm_ps(self.massas, yk))
            C.append(self.complexidade(I[-1]))
            E_total.append(frame[-1])
        return I, E_total, C, YK