from animacao.simular import Simulacao
from condicoesIniciais.condicoesArtigo import condicoesArtigo

### EXEMPLO GERAL COM E=0, P=0, J=0 E RCM=0 CONFORME O ARTIGO
configs = {
    'qntdCorpos': 50, # qntd de corpos
    'massas': {
        'min': 30,
        'max': 30
    },
    'posicoes': {
        'intervalo_x': [-500, 500],
        'dist_min_x': 1,
        'intervalo_y': [-500, 500],
        'dist_min_y': 1
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
S.simular(exibir=True, salvar=False)