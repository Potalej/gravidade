# from animacao.animacao import Animacao
from animacao.simular import Simulacao

# m = [120, 200, 100]
# R0 = [[-100, 0], [0,0], [100, 0]]
# P0 = [[0,0], [0,0], [0,0]]

# S = Simulacao(m, R0, P0)
# S.simular(False, True, 1000)

from animacao.animacao import Animacao

Animacao().animar_salvo('pontos/pontos.txt')