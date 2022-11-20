from animacao.simular import Simulacao
from calculos.condicoesIniciais import condicoesArtigo

### EXEMPLO COM E=0, P = 0 e J = 0 CONFORME O ARTIGO
condicoes = condicoesArtigo([])
m = condicoes.gerar_massas(m_min=30, m_max=30, qntd=44)
R0, P0 = condicoes.circulo(raio=200)

S = Simulacao(m, R0, P0)
# S.simular(exibir=False, salvar=True, qntdFrames=1500)
S.simular(exibir=True, salvar=False)