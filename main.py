from animacao.simular import Simulacao
from calculos.condicoesIniciais import condicoesIniciais

m = [120, 200, 100]
R0, P0 = condicoesIniciais(m).energia_nula([-100, 100, 30], [-1, 1])
S = Simulacao(m, R0, P0)
S.simular(exibir=True, salvar=False)