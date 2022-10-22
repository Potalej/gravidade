# 🪐gravidade🪐
Para simulações básicas de gravidade.

Este repositório centraliza uma parte dos scripts que faço para praticar algumas coisas que tenho aprendido.

<img src="https://www.linux.ime.usp.br/~potalej/img/gravidade_exemplo.gif" alt="Exemplo" width="400" height="400">

Meu estudo atualmente está seguindo através de um artigo publicado na _Physical Review Letters_ de autoria de Julian Barbour, Tim Koslowski e Flavio Mercati, chamado [Identification of a Gravitational Arrow of Time](https://physics.aps.org/featured-article-pdf/10.1103/PhysRevLett.113.181101). Este, porém, ainda é um resumo de um artigo mais completo dos mesmos autores chamado [A Gravitational Origin of the Arrows of Time](https://arxiv.org/abs/1310.5167), mas que ainda não me atrevi a adentrar.

## Integração Numérica
Para resolver as equações diferenciais ordinárias (EDOs) que descrevem o comportamento mais básico dos corpos estou utilizando o [Método de Runge-Kutta](https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods) em uma versão explícita e adaptada ao tipo de programa que está sendo feito, de modo a conseguir um desempenho melhor.

O Runge-Kutta pode assumir várias formas. Fiz num formato geral que aceita uma ordem qualquer, bastando apenas informar as matrizes na forma do _tableau_ de Butcher. Para o propósito do programa, isso se tornou inútil, então será suprimido em versões futuras.

## Colisões
As colisões foram modeladas considerando corpos perfeitamente rígidos e atômicos, ou seja, não quebram e não se deformam. São apenas pontos com um raio, para todo efeito, possuindo uma massa e, dada uma densidade universal, tendo seu raio calculado como a razão entre a massa e a densidade.

Para fazer a modelagem desse movimento utilizei como base um [vídeo do canal Reducible](https://youtu.be/eED4bSkYCB8), que também é baseado num pequeno [texto de Chad Berchek](https://www.vobarian.com/collisions/2dcollisions2.pdf).

## Correções Numéricas
Além das imprecisões inevitáveis devido ao Python ser do jeito que é, há o erro natural cometido pelo método de integração em cada passo. Para fazer uma correção coerente, tenho em mente que o sistema é conservativo e que portanto o [hamiltoniano](https://en.wikipedia.org/wiki/Hamiltonian_mechanics) do sistema deve ser constante, então isso dá uma direção para a correção. Sendo a energia inicial uma qualquer, é possível usar o gradiente do hamiltoniano para corrigir os desvios que se derem no processo de integração numérica.

Quando preparei o script com a correção, no entanto, ainda não havia a questão da colisão, então no momento a correção não está sendo realizada. Desenvolvida a matemática que se adeque às colisões, consertarei o script e o sistema ficará preciso novamente.

## Animação
As animações 2D eram inicialmente feitas como um monte de plots do [Matplotlib](https://matplotlib.org/), o que era bastante ineficiente e pouco prático. Decidi então utilizar o [PyGame](https://www.pygame.org/news), já que por razões bastante óbvias desempenho é uma das preocupações dessa biblioteca.

Ainda assim, pretendo procurar algo mais elaborado para criar essas animações, principalmente na iminência de precisar fazer as coisas funcionarem em três dimensões.
