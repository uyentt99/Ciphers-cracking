import RSA.otherCode as func
#-----------------------------------------------------
file1 = open('input.inp')
c = file1.readline().split(' ')
e = int(file1.readline())
n = int(file1.readline())
file1.close()
#---------------------------------------------------
print('RSA Encryption parameters. Public key: [e,N]')
print('Engish text: ',c)
print('e: ',e)
print('n: ',n)
#---------------------------------------------------
def textInt(str):
    encodeStr = int(0)
    for ch in str:
        encodeStr = encodeStr*26 + ord(ch) - 97
    return encodeStr
#--------------------------------------------------
file2 = open('input2.inp','w')
file2.write('%d\n%d' %(e,n))
print('{: <22}'.format('text'),'{: <22}'.format('encode'),'Cipher')
for i in range(len(c)):
    s = c[i].replace('\n','')
    encodeC = textInt(s)
    Cipher = func.power(encodeC,e,n)
    print('{: <20}'.format(s), ': ','{: <20}'.format(encodeC),': ',Cipher)
    file2.write('\n%d'% Cipher)
file2.close()