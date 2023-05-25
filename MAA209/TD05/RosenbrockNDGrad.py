def J(x):
    if variant==1:
        v1 = x[1:]
        v0 = x[:-1]
        return np.sum(100*(v1-v0**2)**2+(1-v0)**2)
    if variant==2:
        return 0.5*np.dot(x,A@x)-np.dot(b,x)

def GradJ(x):
    if variant==1:
        v1 = x[1:]
        v0 = x[:-1]
        res = np.zeros(x.shape)
        res[:-1] = res[:-1]-2*(1-v0)-400*(v1-v0**2)*v0
        res[1:]  = res[1:] +200*(v1-v0**2)
        return res
    if variant==2:
        return A@x-b

def Hess(x):
    if variant==1:
        H = np.diag(-400*x[:-1],1) - np.diag(400*x[:-1],-1)
        diagonal = np.zeros(x.shape)
        diagonal[0] = 1200*x[0]-400*x[1]+2
        diagonal[-1] = 200
        diagonal[1:-1] = 202 + 1200*x[1:-1]**2 - 400*x[2:]
        H = H + np.diag(diagonal)
        return H
    if variant==2:
        return A
