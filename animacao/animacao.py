"""
    Faz a animação a partir de um conjunto de dados armazenados 
    em um arquivo de texto.
"""
from config.configs import animacao, dados
import pygame

class Animacao:

    # def __init__ (self, titulo:str='Animação'):
    #     self.iniciarPyGame(titulo)

    def iniciarPyGame (self, titulo):
        self.LARGURA, self.ALTURA = animacao['LARGURA'], animacao['ALTURA']
        self.ESCALA = animacao['ESCALA']
        self.DENSIDADE = animacao['DENSIDADE']
        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        self.superficie = pygame.Surface((self.LARGURA*self.ESCALA, self.ALTURA*self.ESCALA))
        pygame.display.set_caption(titulo)

    def ler_arquivo (self):
        """Faz a leitura de um arquivo com as informações"""
        with open(self.diretorio, 'r') as arquivo:
            arquivo = arquivo.read()
            partes = arquivo.split(dados['SEPARADOR'])
            
            self.massas = [float(massa) for massa in partes[0].split(',')]
            if self.salvar:
                self.abrirArquivo(self.massas, self.nomeArquivo)
            self.quantidade_corpos = len(self.massas)
            self.salvar_cores(self.quantidade_corpos)
            
            passos = partes[1].split('\n')
            self.qntd_passos = len(passos)

            # se quiser aumentar a velocidade, só colocar um [::x] aqui embaixo
            for posicao in passos:
                yield [float(coord) for coord in posicao.split(',')]

    def desenhar (self, R):
        """Animação de um passo"""
        for corpo in range(self.quantidade_corpos):
            x = R[corpo][0] + self.ESCALA * self.LARGURA / 2
            y = R[corpo][1] + self.ESCALA * self.ALTURA / 2
            pygame.draw.circle(
                self.superficie, 
                self.CORES[corpo], 
                (x,y), 
                self.massas[corpo]/self.DENSIDADE
            )
    
    def salvar_cores (self, qntd:int):
        self.CORES = animacao["CORES"](qntd)

    def animar_salvo (self, diretorio:str):
        """Animar a partir de um arquivo de texto."""
        self.diretorio = diretorio
        self.animar(self.ler_arquivo)

    def abrirArquivo (self, massas:list, nome='pontos.txt'):
        with open('pontos/' + nome, 'w') as arq:
            m = ','.join(str(m) for m in massas)
            arq.write(m + dados['SEPARADOR'][:-1])

    def salvarPontos (self, pontos:list, nome='pontos.txt'):
        coords = [[str(ponto) for ponto in lista] for lista in pontos]
        coords = '\n'.join([','.join(ponto) for ponto in coords])
        with open('pontos/' + nome, 'a') as arq:
            arq.write('\n' + coords)

    def animar (self, geradora, salvar=False, nome='pontos.txt'):
        self.iniciarPyGame('Animação')
        pygame.init()
        clock = pygame.time.Clock()

        self.salvar = salvar
        if self.salvar: self.YK = []
        self.nomeArquivo = nome

        if animacao['EXIBIR_FPS']:
            texto_fps = pygame.font.SysFont(animacao['FONTE'], animacao['TAMANHO_FONTE'])
        if animacao['EXIBIR_ENERGIA']:
            texto_energia = pygame.font.SysFont(animacao['FONTE'], animacao['TAMANHO_FONTE'])
        
        for frame in geradora():

            R, P, E = frame
            if self.salvar: 
                self.YK.append(R)
                if len(self.YK) == animacao['QUANTIDADE_ANTES_SALVAR']:
                    self.salvarPontos(self.YK, self.nomeArquivo)
                    self.YK = []

            clock.tick(animacao['TAXA_ATUALIZACAO'])
            self.superficie.fill(animacao['FUNDO'])
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT: return

            self.desenhar(R)

            redimensionado = pygame.transform.smoothscale(self.superficie, self.tela.get_size())
            self.tela.blit(redimensionado, (0,0))
            # pygame.display.flip()

            if animacao['EXIBIR_FPS']:
                fps = texto_fps.render(f"FPS: {round(clock.get_fps(), 2)}", True, animacao['COR_FONTE'])
                self.tela.blit(fps, (self.LARGURA-150, 0))
            if animacao['EXIBIR_ENERGIA']:
                energia = texto_energia.render(f"H={round(E,2)}", True, animacao['COR_FONTE'])
                self.tela.blit(energia, (self.LARGURA-150, 30))

            pygame.display.update()
        
        if len(self.YK) >= 0:
            self.salvarPontos(self.YK, self.nomeArquivo)
