import random



class Rsa:
  BIT_SIZE = 100
  
  def __init__(self):
    self.firstPrime = self.generatePrime()
    self.secondPrime = self.generatePrime()

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


  def encrypt(self,message):
    ascii_values = []
    print('\n')
    for character in message:
      ascii_values.append(ord(character))

    cipherNumList = []
    for index,ascii in enumerate(ascii_values):
      cipherNumList.append(pow(ascii,self.publicKey,self.modulus))
 
    return cipherNumList

  def decrypt(self,cipherNumList):
    decryptedAscii_list = []
    for index,ascii in enumerate(cipherNumList):
      decryptedAscii_list.append(pow(ascii,self.privateKey,self.modulus))
      

    actualText = ''
    for decrypted_ascii in decryptedAscii_list:
      actualText += chr(decrypted_ascii)
    
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