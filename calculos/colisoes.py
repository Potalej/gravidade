"""
    Contém funções relacionadas à colisão de partículas.
"""

from config.configs import particulas
from numpy import array, einsum, argsort

densidade = particulas["DENSIDADE"]

def colisoes (m1, m2, x1, y1, x2, y2, px1, py1, px2, py2):
    c1_c2 = array([x1,y1]) - array([x2,y2])
    c1_c2_norma2 = einsum('i,i', c1_c2, c1_c2)
    
    v1 = array([px1,py1])/m1
    v2 = array([px2,py2])/m2

    dif_vel = v1 - v2
    v1v2_c1c2 = einsum('i,i', dif_vel, c1_c2)

    fator = 2 * v1v2_c1c2 / ((m1+m2) * c1_c2_norma2)

    v1_ = v1 - m2*c1_c2*fator
    v2_ = v2 + m1*c1_c2*fator

    return v1_.tolist(), v2_.tolist()    

def dist (x1, y1, x2, y2):
    return ((x2-x1)**2 + (y2-y1)**2)**.5

def verificaColisoes (massas, yk):
    qntd = len(massas)

    X = yk[::4]
    Y = yk[2::4]
    I = argsort(X) # sweep and prune

    idx = 0
    C = []

    houve_colisao = False

    while idx < qntd:
        jdx = idx if len(C)== 0 else C[-1]
        jdx += 1

        while jdx < qntd:
            if X[I[idx]]*densidade + massas[I[idx]] >= X[I[jdx]]*densidade - massas[I[jdx]]:
                C.append(jdx)
                houve_colisao = True
                jdx += 1
            else: break

        if len(C) > 0:
            x1, y1 = X[I[idx]], Y[I[idx]]
            m1 = massas[I[idx]]
            for jdx_C in C:
                x2, y2 = X[I[jdx_C]], Y[I[jdx_C]]
                m2 = massas[I[jdx_C]]

                if dist(x1,y1,x2,y2) * densidade <= (m1+m2):
                    px1, px2 = yk[I[idx]*4+1], yk[I[jdx_C]*4+1]
                    py1, py2 = yk[I[idx]*4+3], yk[I[jdx_C]*4+3]
                    v1, v2 = colisoes(m1, m2, x1, y1, x2, y2, px1, py1, px2, py2)

                    yk[I[idx] * 4 + 1] = v1[0] * m1
                    yk[I[idx] * 4 + 3] = v1[1] * m1

                    yk[I[jdx_C] * 4 + 1] = v2[0] * m2
                    yk[I[jdx_C] * 4 + 3] = v2[1] * m2
            
            idx = C[0]
        else: idx += 1

        C = C[1:]

    return yk, houve_colisao
