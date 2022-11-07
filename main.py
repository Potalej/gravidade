# # from animacao.animacao import Animacao
from animacao.simular import Simulacao

# m = [120, 200, 100]
# R0 = [[-100, 0], [0,0], [100, 0]]
# P0 = [[0,0], [0,0], [0,0]]

# S = Simulacao(m, R0, P0)
# S.simular(exibir=True, salvar=False)

# # from animacao.animacao import Animacao
# # Animacao().animar_salvo('pontos/pontos.txt')

from condicoesIniciais import condicoesIniciais

m = [120, 200, 100]
R0, P0 = condicoesIniciais(m).energia_nula([-100, 100, 30], [-1, 1])
S = Simulacao(m, R0, P0)
S.simular(exibir=True, salvar=False)