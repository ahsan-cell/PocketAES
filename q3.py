
def InputToMatrix(plaintext):
    return [[int(plaintext[0],16),int(plaintext[2],16)],[int(plaintext[1],16),int(plaintext[3],16)]]


def subNibble(nibble):  
    subNibbles={
    0b0000:0b1010,
    0b0001:0b0000,
    0b0010:0b1001,
    0b0011:0b1110,
    0b0100:0b0110,
    0b0101:0b0011,
    0b0110:0b1111,
    0b0111:0b0101,
    0b1000:0b0001,
    0b1001:0b1101,
    0b1010:0b1100,
    0b1011:0b0111,
    0b1100:0b1011,
    0b1101:0b0100,
    0b1110:0b0010,
    0b1111:0b1000,
    }
    return subNibbles[nibble]


def inversesubNibble(nibble):  #pass nibble in string format
    subNibbles={
    0b1010:0b0000,
    0b0000:0b0001,
    0b1001:0b0010,
    0b1110:0b0011,
    0b0110:0b0100,
    0b0011:0b0101,
    0b1111:0b0110,
    0b0101:0b0111,
    0b0001:0b1000,
    0b1101:0b1001,
    0b1100:0b1010,
    0b0111:0b1011,
    0b1011:0b1100,
    0b0100:0b1101,
    0b0010:0b1110,
    0b1000:0b1111,
    }
    return subNibbles[nibble]


def generateRoundKeys(masterKey): #masterkey as a string
    Rcon1=0b1110
    Rcon2=0b1010
    w4=int(masterKey[0],16)^subNibble(int(masterKey[3],16))^Rcon1
    w5=int(masterKey[1],16)^w4
    w6=int(masterKey[2],16)^w5
    w7=int(masterKey[3],16)^w6

    w8=w4^subNibble(w7)^Rcon2
    w9=w5^w8
    w10=w6^w9
    w11=w7^w10

    k1=[[w4,w6],
        [w5,w7]]
    k2=[[w8,w10],
        [w9,w11]]
    return k1,k2

def AddRoundKey(inputMatrix,keyMatrix):
    for i in range(2):
        for j in range(2):
            inputMatrix[j][i]=inputMatrix[j][i]^keyMatrix[j][i]
    return inputMatrix


def Multiplication(a,b):
    m=0b0000
    while b>0:
        if b&1:
            m=m^a
        
        if a & 0b1000:
            a=a<<1
            a=a^0b10011
        else:
            a=a<<1
        b=b>>1
    return m 

def shiftRow(matrix):
    temp=matrix[0][1]
    matrix[0][1]=matrix[0][0]
    matrix[0][0]=temp
    return matrix

def inverseMixColumns(matrix):
    d0=Multiplication(9,matrix[0][0])^Multiplication(2,matrix[1][0])
    d1=Multiplication(2,matrix[0][0])^Multiplication(9,matrix[1][0])
    d2=Multiplication(9,matrix[0][1])^Multiplication(2,matrix[1][1])
    d3=Multiplication(2,matrix[0][1])^Multiplication(9,matrix[1][1])

    return [[d0,d2],
             [d1,d3]]

def MixColumns(matrix):
    d0=Multiplication(1,matrix[0][0])^Multiplication(4,matrix[1][0])
    d1=Multiplication(4,matrix[0][0])^Multiplication(1,matrix[1][0])
    d2=Multiplication(1,matrix[0][1])^Multiplication(4,matrix[1][1])
    d3=Multiplication(4,matrix[0][1])^Multiplication(1,matrix[1][1])

    return [[d0,d2],
             [d1,d3]]
    

def InputPlainText():
    plaintext=input('Enter a hexadecimal input (16 bit): ')
    if len(plaintext)>4:
        print('Input was invalid')
    else:
        diff=4-len(plaintext)
        for i in range(diff):
            plaintext='0'+plaintext
    return plaintext

def Inputkey():
    masterKey=input('Enter a hexadecimal key (16 bit): ')
    if len(masterKey)>4:
        print('Input was invalid')
    else:
        diff=4-len(masterKey)
        for i in range(diff):
            masterKey='0'+masterKey
    return masterKey

def MatrixToCipher(matrix):
    cipher=[]
    for i in range(2):
        for j in range(2):
            cipher.append(str(hex(matrix[j][i]))[2:])
    cipher=''.join(cipher)
    return cipher

def Encrypt(plaintext=None,masterKey=None):
    if plaintext==None:
        plaintext=InputPlainText()
    if masterKey==None:
        masterKey=Inputkey()
    matrix=InputToMatrix(plaintext)
    #sub nibble
    for i in range(2):
        for j in range(2):
            matrix[i][j]=subNibble(matrix[i][j])
    # add round key
    k1,k2=generateRoundKeys(masterKey)
    matrix=AddRoundKey(matrix,k1)
    #mix columns
    matrix=MixColumns(matrix)
    # print(matrix)
    #shift rows
    matrix=shiftRow(matrix)
    # Round 2
    #sub nibble
    # print(matrix)
    for i in range(2):
        for j in range(2):
            matrix[i][j]=subNibble(matrix[i][j])
    
    # add round key 
    matrix=AddRoundKey(matrix,k2)
    #shift rows
    matrix=shiftRow(matrix)
    # print(MatrixToCipher(matrix))
    return MatrixToCipher(matrix)


def Decrypt(plaintext=None,masterKey=None):
    if plaintext==None:
        plaintext=InputPlainText()
    if masterKey==None:
        masterKey=Inputkey()
    matrix=InputToMatrix(plaintext)

    matrix=shiftRow(matrix)
    k1,k2=generateRoundKeys(masterKey)

    matrix=AddRoundKey(matrix,k2)
    for i in range(2):
        for j in range(2):
            matrix[i][j]=inversesubNibble(matrix[i][j])
    
    matrix=shiftRow(matrix)

    matrix=inverseMixColumns(matrix)

    matrix=AddRoundKey(matrix,k1)
    for i in range(2):
        for j in range(2):
            matrix[i][j]=inversesubNibble(matrix[i][j])
    # print(MatrixToCipher(matrix))

    return MatrixToCipher(matrix)


   
def EncodeInputFile(filename):
    f=open(filename,'r')
    content=f.read()
    asci=[]


    for i in range(0,len(content),2):
        # print(i)
        first=str(hex(ord(content[i])))[2:]
        if i+1<len(content):
            second=str(hex(ord(content[i+1])))[2:]
        else:
            second='00'

        asci.append(first+second)
    return asci


def EncryptFile():
    print('--------------File Encryption---------------')
    filename=str(input("Enter filename: "))
    file=EncodeInputFile(filename)
    
    masterKey=Inputkey()
    print('Encrypting....')
    encrypted=''
    for block in file:
        encrypted+=Encrypt(block,masterKey)+' '
    return encrypted

def DecryptFile():
    print('--------------File Decryption---------------')
    filename=str(input("Enter filename: "))
    masterKey=Inputkey()
    f=open(filename)
    contents=f.read()
    contents=contents.split()
    decrypted=''
    print('Decrypting.....')
    for content in contents:
        x=Decrypt(content,masterKey)
        first=chr(int(x[:2],16))
        second=chr(int(x[2:4],16))
        decrypted+=first+second
    # print(decrypted)
    if ord(decrypted[-1])==0:
        decrypted=decrypted[:-1]
    return decrypted

# print(EncryptFile())

plainMsg=DecryptFile()
print(plainMsg)
f=open('plain.txt','w')
f.write(plainMsg)



        

