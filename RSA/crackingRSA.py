import RSA.otherCode as func
import RSA.keyRSA as key
#-----------------------------------------------------
file2 = open('input2.inp')
e = int(file2.readline())
n = int(file2.readline())
s = file2.read().split();
C = [int(x) for x in s]
#-----------------------------------------------------
print('RSA Encryption parameters. Public key: [e,N]')
print('e: ',e)
print('n: ',n)
print('Cipher: ',C)
p,q,kt = key.findPQ(n)
if (kt==False):
    exit()
pn = (p-1)*(q-1)
r, d = func.extGCD(e,pn)
if (r!=1):
    print('gcd(e,pn)!=1')
    exit()
print('d: ',d)
#-----------------------------
def intText(encodeStr):
    str = []
    while encodeStr>0:
        x = encodeStr % 26 + 97
        str.append(chr(x))
        encodeStr = encodeStr//26
    str = str[len(str)::-1]
    return ''.join(str)
#--------------------------------
for c in C:
    encodeC = func.power(c,d,n)
    print('{: <25}'.format(c), ': ',intText(encodeC))