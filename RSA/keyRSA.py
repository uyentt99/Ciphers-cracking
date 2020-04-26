import RSA.otherCode as func
import random
import time
import math
#--------------------------------------------------
def isPrime(n):
    if (n<=3):
        return True
    random.seed(time.time() * 10)
    for _ in range(min(n,100)):
        x = random.randrange(2,n-1)
        y = func.power(x,n-1,n)
        if (y!=1):
            return False
    return True
#----------------------------------------------------
def findPQ(n):
    p = 1
    if (n%2==0):
        p = 2
    else:
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if (n % i == 0):
                p = i
                break
    q = n//p
    kt = (p!=1) and (q != p)  and isPrime(q)
    print('p: ', p)
    print('q: ', q)
    if (not kt):
        print('n khong thoa man')
    return p,q,kt
#-------------------------------------------------------
def createKeyPQ(p,q):
    print('p: ', p)
    print('q: ', q)
    if (p==q):
        print('Wrong')
    n = p * q
    pn = (p-1)*(q-1)
    print('n: ', n)
    for i in range (10000):
        random.seed(time.time()*15)
        e = random.randrange(1,int(1e9))
        if (math.gcd(pn,e)==1):
            print('e: ', e)
            return e, n
    print("Need try again")
#---------------------------------------------------------
def createKey():
    fileP = open('primes.inp')
    listPrimes = fileP.read().split('\n')
    NPrimes = len(listPrimes)
    random.seed(time.time() * 10)
    p = int(listPrimes[random.randrange(NPrimes)])
    random.seed(time.time() * 20)
    q = int(listPrimes[random.randrange(NPrimes)])
    createKeyPQ(p,q)
#----------------------------------------------------------