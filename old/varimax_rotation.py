from scipy import eye, asarray, dot, sum, diag
from scipy.linalg import svd


def varimax(Phi, gamma = 0.0, q = 1000, tol = 1e-04):
    
    p,k = Phi.shape
    R = eye(k)
    d=0
    for i in range(q):
        d_old = d
        Lambda = dot(Phi, R)
        u,s,vh = svd(dot(Phi.T,asarray(Lambda)**2 - (gamma) * dot(Lambda, diag(diag(dot(Lambda.T,Lambda))))))
        R = dot(u,vh)
        d = sum(s)
        if d_old!=0 and d/d_old < 1 + tol: break
    return dot(Phi, R)

## WRITE DOWN THE URL

## iterate over gamma values, save png files with gamma values
## also with q