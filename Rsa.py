import random



class Rsa:
  BIT_SIZE = 1024
  def __init__(self):
    self.firstPrime = 0
    self.secondPrime = 0
    self.publicKey = 0
    self.privateKey = 0
    self.modulus = 1

  def initialize(self):
    
    with open("rsaEncryption.rsa",'r') as file:
        if file.read() == '':
          self.generateKeys()
        else:
          file.seek(0)
          self.firstPrime = int(file.readline())
          self.secondPrime = int(file.readline())

    self.modulus = self.firstPrime * self.secondPrime

    phi = (self.firstPrime-1) * (self.secondPrime-1)

    for number in range(phi,1,-1):
      if self.gcd(phi,number) == 1:
        self.publicKey = number
        break
      
    for number in range(phi,1,-1):
      if (self.publicKey * number) % phi == 1:
        self.privateKey = number
        break

  def generateKeys(self):
      self.firstPrime = self.generatePrime()
      self.secondPrime = self.generatePrime()
      
      with open("rsaEncryption.rsa",'w') as file:
        file.write(str(self.firstPrime)+'\n')
        file.write(str(self.secondPrime))

      self.initialize()

  def encrypt(self,message):
    ascii_values = []
    char_sequence = []

    for index,char in enumerate(message):
      if not (ord(char) in ascii_values):
        ascii_values.append(ord(char))
      char_sequence.append(ascii_values.index(ord(char)))
  
    print('\n')

    cipherNumList = []
    j = 3
    for index,ascii in enumerate(ascii_values):
      if index % 10 == 0:
        j-=1
      backSpace = '\b'
      if j < 0:
        j = 2
    
      completed = 100 * index/len(ascii_values)
      print('\tEncrypting...'+backSpace*j,'   ','\tProgress ->',"{0:.2f}".format(completed),'%',end = '\r')
      cipherNumList.append(pow(ascii,self.publicKey,self.modulus))
    
    print('****************** Done!...Data Encrypted! *********************')
    return str(cipherNumList)+'\n'+str(char_sequence)

  def decrypt(self,formattedCipherText):
    formattedCipherText = formattedCipherText.replace(']','',2)
    formattedCipherText = formattedCipherText.replace('[','',2)

    end = formattedCipherText.find('\n')
    cipherNumList = formattedCipherText [:end]
    charSequence = formattedCipherText[end+1:]

    cipherNumList = list(cipherNumList.split(','))
    cipherNumList = list(map(int,cipherNumList))

    charSequence = list(charSequence.split(','))
    charSequence = list(map(int,charSequence))
  
    decryptedAscii_list = []

    print('\n')
    j = 3
    for index,ascii in enumerate(cipherNumList):
      if index % 10 == 0:
        j-=1
      backSpace = '\b'
      if j < 0:
        j = 2
      completed = 100 * index/len(cipherNumList)
      print('\tDecrypting...'+backSpace*j,'   ','\tProgress ->',"{0:.2f}".format(completed),'%', end = '\r')
      decryptedAscii_list.append(pow(ascii,self.privateKey,self.modulus))

    #print('****************** Done!...Data Decrypted! *********************')
    actualText = ''
    for asciiValue in charSequence:
      actualText += chr(decryptedAscii_list[asciiValue])

    return actualText

  def fermat_primality_test(self,number):

    if number % 2 == 0:
      return False

    evenComponent=number-1
    a=random.randrange(1,number)
    if pow(a,evenComponent,number) == 1:
      return True
    return False
  
  
  def generatePrime(self):
    while True:
      primeCandidate = random.randrange(pow(2,Rsa.BIT_SIZE),pow(2,Rsa.BIT_SIZE+1))
      if self.fermat_primality_test(primeCandidate):
        return primeCandidate
  
  def gcd(self,a,b):
    if b == 0:
      return a
    else:
      return self.gcd(b,a%b)
