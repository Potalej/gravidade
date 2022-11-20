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

def Rcm (fs:list, m:list)->float:
    rcm = []    
    X, Y = fs[::4], fs[2::4]
    for i, mi in enumerate(m):
        rcm[0] += mi*X[i]
        rcm[1] += mi*Y[i]
    mtot = sum(m)
    rcm = [rcm[0]/mtot, rcm[1]/mtot]
    return rcm

def prodvetR2(a, b): return a[0]*b[1] - a[1]*b[0]

def momentoAngular (fs:list)->float:
    soma = 0
    X, Y = fs[::4], fs[2::4]
    Px, Py = fs[1::4], fs[3::4]
    for i in range(len(X)):
        soma += prodvetR2([X[i], Y[i]], [Px[i], Py[i]])
    return soma