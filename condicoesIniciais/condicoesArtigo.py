from condicoesIniciais.condicoesIniciais import condicoesIniciais
from calculos.hamiltoniano import U, EC
from calculos.auxiliares import *

class condicoesArtigo (condicoesIniciais):
    
    def __init__ (self, massas:list=[]):
        super().__init__(massas)

    def gerarBasico (self, configs:dict)->None:
        """Gera as coordenadas básicas."""
        # quantidade
        N = configs['qntdCorpos']
        massas, posicoes, velocidades = configs['massas'], configs['posicoes'], configs['velocidades']
        # gerando massas
        self.gerar_massas(massas['min'], massas['max'], N)
        # gerando posições
        self.gerar_posicoes(
            N, 
            posicoes['intervalo_x'], 
            posicoes['intervalo_y'], 
            posicoes['dist_min_x'], 
            posicoes['dist_min_y']
        )
        # gerando velocidades
        self.gerar_velocidades(
            N,
            velocidades['intervalo_x'],
            velocidades['intervalo_y'],
            velocidades['intervalo_min_x'],
            velocidades['intervalo_min_y']
        )


    def condicionar (self)->None:
        """
            Aplica as condições sobre os valores já gerados.
        """
        self.rcm = centro_massas(self.massas, self.r)

        # 1) zerar rcm
        self.zerar_centro_massas()
        # print('1ª Condição: rcm =', self.rcm)
        
        # 2) zerar vcm = r'cm
        self.zerar_velocidade_centro_massas()
        # print('2ª Condição: P =', self.P)

        # 3) zerar o momento angular
        self.zerar_momento_angular()
        # print('3ª Condição: L =', self.L)

        energia_potencial = U(self.juntar_ps(), self.massas)

        # 4) zerar a energia total
        self.zerar_energia_total(energia_potencial)
        self.juntar_ps()
        # energia_cinetica = EC(self.ps, self.massas)
        # print('4ª garantia: Ec + V = ', energia_cinetica+energia_potencial)

    def transformar_posicoes (self):
        """Arruma as posições em relação ao centro de massas."""
        r_til = [
            [self.r[i][0] - self.rcm[0], self.r[i][1] - self.rcm[1]] 
        for i in range(self.qntdCorpos)]
        self.r = r_til
        return r_til

    def transformar_velocidades (self):
        """Arruma as velocidades"""
        v_til = [
            [self.v[i][0] - self.P[0]/self.mtot, self.v[i][1] - self.P[1]/self.mtot] 
        for i in range(self.qntdCorpos)]
        self.v = v_til
        return self.v

    def zerar_centro_massas (self):
        """Posiciona o centro de massas na origem."""
        # arruma as posições
        self.transformar_posicoes()
        self.rcm = centro_massas(self.massas, self.r)

    def zerar_velocidade_centro_massas (self):
        """Zera a velocidade do centro de massasm, i.e., o momento linear total."""
        self.P = momento_linear_total_velocidade(self.massas, self.v)
        self.transformar_velocidades()
        self.P = momento_linear_total_velocidade(self.massas, self.v)

    def zerar_momento_angular (self):
        """Zera o momento angular."""
        L_estrelas = momentos_angulares(self.massas, self.r, self.v)
        L_estrela = [
            sum(x[0] for x in L_estrelas),
            sum(y[1] for y in L_estrelas),
            sum(z[2] for z in L_estrelas),
        ]
        self.Icm = momento_inercia_cm(self.massas, self.r)

        fator_L_x = lambda ra: prodvetR3(L_estrela, ra + [0])[0]
        fator_L_y = lambda ra: prodvetR3(L_estrela, ra + [0])[1]

        v_til = [[
            self.v[i][0] - fator_L_x(self.r[i])/self.Icm, self.v[i][1] - fator_L_y(self.r[i])/self.Icm
        ] for i in range(self.qntdCorpos)]

        self.v = v_til
        self.L = sum(self.massas[i] * prodvetR2(self.r[i], self.v[i]) for i in range(self.qntdCorpos))

    def zerar_energia_total (self, energia_potencial):
        self.juntar_ps()
        energia_cinetica = EC(self.ps, self.massas)
        fator = (-energia_potencial/energia_cinetica)**.5
        
        for i in range(self.qntdCorpos):
            self.v[i][0] *= fator
            self.v[i][1] *= fator

        return self.v