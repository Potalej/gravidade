from animacao.simular import Simulacao
# from calculos.condicoesIniciais import condicoesArtigo
from condicoesIniciais.condicoesArtigo import condicoesArtigo

### EXEMPLO COM E=0, P = 0 e J = 0 CONFORME O ARTIGO
# condicoes = condicoesArtigo([])
# m = condicoes.gerar_massas(m_min=50, m_max=50, qntd=20)
# R0, P0 = condicoes.circulo(raio=200)

### EXEMPLO QUALQUER
# m = [30, 40, 50]
# R0 = [[100, 100],[-100, -100],[-30, 65]]
# P0 = [[0, 0],[10, 5],[0, 0]]

### EXEMPLO GERAL COM E=0, P=0, J=0 E RCM=0 CONFORME O ARTIGO
configs = {
    'N': 50, # qntd de corpos
    'massas': {
        'min': 200,
        'max': 500
    },
    'posicoes': {
        'intervalo_x': [-30000, 30000],
        'dist_min_x': 100,
        'intervalo_y': [-30000, 30000],
        'dist_min_y': 100
    },
    'velocidades': {
        'intervalo_x': [-1, 1],
        'intervalo_min_x': 1,
        'intervalo_y': [-1, 1],
        'intervalo_min_y': 1
    }
}

condicoes = condicoesArtigo()
condicoes.gerarBasico(configs)
condicoes.condicionar()

S = Simulacao(condicoes.massas, condicoes.r, condicoes.p)
## S.simular(exibir=False, salvar=True, qntdFrames=1500)
# S.simular(exibir=True, salvar=False)
I, E, C, YK = S.simularMomentoInercia(500)
