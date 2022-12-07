"""
    Funções auxiliares que são usadas com alguma frequência nos scripts
    Inclui funções de mecânica e de geometria analítica.

    Matemática:
    => norma2: norma euclidiana ao quadrado de um vetor qualquer passado;
    => prodvetR2: produto vetorial no R2;
    => prodvetR3: produto vetorial no R3;

    Física:
    => momento_inercia_cm: momento de inércia relativo ao centro de massas.
    => momento_inercia_cm_ps: momento de inércia a partir dos pontos em forma de integração.
    => momentos_angulares: momneto angular de cada partícula do sistema.
    => centro_massas: ponto do centro de massas do sistema.
    => momento_linear_total_velocidade: momento linear total do sistema a partir das velocidades e massas.
"""

## Matemática

def norma2 (u:list)->float:
    """Quadrado da norma euclidiana."""
    return sum(ui**2 for ui in u)

def prodvetR2 (u:list, v:list)->float:
    """Produto vetorial no R2. Retorna um escalar real."""
    return u[0]*v[1]-u[1]*v[0]

def prodvetR3 (u:list, v:list)->list:
    """Produto vetorial no R3. Retorna um vetor no R3 que é ortogonal a `u` e a `v`."""
    return [u[1]*v[2]-v[1]*u[2], -u[0]*v[2]+v[0]*u[2], u[0]*v[1]-v[0]*u[1]]


## Física

def momento_inercia_cm (m:list, r:list)->float:
    """Momento de inércia relativo ao centro de massas."""
    return sum(m[i] * norma2(r[i]) for i in range(len(m)))

def momento_inercia_cm_ps (m:list, ps:list)->float:
    """Momento de inércia a partir dos pontos em forma de integração."""
    return sum(m[i] * norma2([ps[2*i], ps[2*i+1]]) for i in range(len(m)))

def momentos_angulares (m:list, r:list, v:list)->list:
    """Momento angular de cada partícula do sistema."""
    return [prodvetR3([r[i][0], r[i][1], 0], [v[i][0]*m[i], v[i][1]*m[i], 0]) for i in range(len(m))]

def centro_massas (m:list, r:list)->list:
    """Ponto do centro de massas do sistema."""
    rcm = [0 for i in range(len(r[0]))]
    for i in range(len(m)):
        for j in range(len(r[i])):
            rcm[j] += m[i]*r[i][j]
    mtot = sum(m)
    rcm = [rcm_i/mtot for rcm_i in rcm]
    return rcm

def momento_linear_total_velocidade (m:list, v:list)->list:
    """Momento linear total do sistema a partir das velocidades e massas."""
    P = [0 for i in range(len(v[0]))]
    for i in range(len(m)):
        for j in range(len(v[i])):
            P[j] += m[i]*v[i][j]
    return P