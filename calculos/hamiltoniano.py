"""
    Cálculos ligados ao hamiltoniano do sistema.
"""

from math import sqrt

def EC (ps:list, m:list)->float:
    soma = 0
    for a in range(len(m)):
        pa = [
            ps[4*a+1], ps[4*a+3]
        ]
        pi_pa = sum(pa_i**2 for pa_i in pa)
        soma += pi_pa/(2*m[a])
    return soma

def U (ps:list, m:list)->float:
    soma = 0
    for b in range(1, len(m)):
        for a in range(b):
            ra = [ps[4*a], ps[4*a+2]]
            rb = [ps[4*b], ps[4*b+2]]
            dist = sqrt(sum((ra[i] - rb[i])**2 for i in range(len(ra))))
            if dist > 10:
                soma += m[a]*m[b]/dist
    return -soma

def H (ps:list, m:list)->float:
    """Energia total"""
    return EC(ps, m) + U(ps, m)

def gradH (fs:list, tk:float, yk:list, F:float):
    comps = []
    for i in range(0, len(yk), 2):
        comps.append(-fs[i+1](tk, F, *yk))
        comps.append(fs[i](tk, F,*yk))
    return comps

def ajustar (fs:list, tk:float, yk:list, m:list, e0:float, F:float)->float:

    e = H(yk, m)
    grad = gradH(fs, tk, yk, F)
    norma_grad2 = sum(g*g for g in grad)
        
    fator = (e - e0)/norma_grad2
    dif = [fator*gradi for gradi in grad]

    for i in range(len(grad)):
        yk[i] -= dif[i]

    return yk, e