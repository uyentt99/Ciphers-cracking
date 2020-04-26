#calc a modul b
def power(a,b,BASE):
    if (b==0):
        return 1
    if (b==1):
        return a
    w = power(a,b>>1,BASE)
    w = (w*w)%BASE
    if (b&1==1):
        w = (w*a)%BASE
    return w
##tinh nghich dao dong du
def extGCD(a, b):
    m, n = a, b
    xm, xn = 1, 0
    while (n!=0):
        q = m//n
        r, xr = m-q*n,  xm - q*xn
        m, xm = n, xn
        n, xn = r, xr
    return m, xm%b