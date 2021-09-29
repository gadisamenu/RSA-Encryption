import random,enum

def gcd(a,b):
  if b == 0:
    return a
  else:
    return gcd(b,a%b)

            
class rsaState(enum.Enum):
  READY = 0
  INVALID_STATE = 1

class Rsa:
  state = rsaState.INVALID_STATE
  BIT_SIZE = 1024
  firstPrime = 0
  secondPrime = 0
  publicLock = 0
  privateKey = 0
  modulus = 0

  @staticmethod
  def initialize():
    try:
      file = open('encryptionInfo.rsa','r')
    except FileNotFoundError as fnot:
      print("Initialization Failed!",fnot)
      return False

    if file.read() == '':
      Rsa.generateNewKey()
    file.seek(0)

    try:
      Rsa.firstPrime = int(file.readline())
      Rsa.secondPrime = int(file.readline())
    except:
      print('Invalid Encryption Resource!'+file.name)
      return False

    modulus = Rsa.firstPrime * Rsa.secondPrime

    phi = (Rsa.firstPrime-1) * (Rsa.secondPrime-1)

    key = 0
    for i in range(modulus,1,-1):
      if gcd(i, phi)==1:
        key = i
        break
        
    testLock = Rsa.modularInverse(phi, key)
    lock = testLock + phi if testLock < 0 else testLock

    Rsa.publicLock = key 
    Rsa.privateKey = lock
    Rsa.modulus = modulus

    Rsa.state = rsaState.READY
    return True


  @staticmethod
  def generateNewKey():
    Rsa.firstPrime = Rsa._generatePrime()
    Rsa.secondPrime = Rsa._generatePrime()
    try:
      file = open('encryptionInfo.rsa','w')
      file.write(str(Rsa.firstPrime)+'\n')
      file.write(str(Rsa.secondPrime)+'\n')
    except FileNotFoundError:
      pass
    except ValueError:
      raise InvalidPrimeNumberFormat
    file.close()

    Rsa.initialize()


  @staticmethod
  def _isPrime(number):
    if number % 2 == 0:
      return False

    a=random.randrange(1,number)
    if pow(a,number,number) == pow(a,1,number):
      return True
    return False
  
  @staticmethod
  def _generatePrime():
    while True:
      primeCandidate = random.randrange(pow(2,Rsa.BIT_SIZE),pow(2,Rsa.BIT_SIZE+1))
      if Rsa._isPrime(primeCandidate):
        return primeCandidate

  @staticmethod
  def modularInverse(phi,e,s0=1,s1=0,t0=0,t1=1):
    if phi % e == 0:
      return t1
    else:
      q=phi//e
      s=s0 - q*s1
      t=t0 - q*t1
      return Rsa.modularInverse(e,phi%e,s1,s,t1,t)

  @staticmethod
  def encrypt(message):
    if Rsa.state == rsaState.INVALID_STATE:
      print("RSA is not initialized!")
      return
     
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
      cipherNumList.append(pow(ascii,Rsa.publicLock,Rsa.modulus))
      
    print('****************** Done!...Data Encrypted! *********************')
    return str(cipherNumList)+'\n'+str(char_sequence)
  
  @staticmethod
  def decrypt(formattedCipherText):
    if Rsa.state == rsaState.INVALID_STATE:
      print("RSA is not initialized!")
      return
  
    formattedCipherText = formattedCipherText.replace(']','',2)
    formattedCipherText = formattedCipherText.replace('[','',2)

    end = formattedCipherText.find('\n')
    cipherNumList = formattedCipherText [:end]
    charSequence = formattedCipherText[end+1:]
    try:

      cipherNumList = list(cipherNumList.split(','))
      cipherNumList = list(map(int,cipherNumList))

      charSequence = list(charSequence.split(','))
      charSequence = list(map(int,charSequence))
    except ValueError:
      raise InvalidEncryptionFormat

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
      decryptedAscii_list.append(pow(ascii,Rsa.privateKey,Rsa.modulus))

    print('****************** Done!...Data Decrypted! *********************')
    try:
      actualText = ''
      for asciiValue in charSequence:
        actualText += chr(decryptedAscii_list[asciiValue])
    except ValueError:
      raise KeyMisMatch
    except OverflowError as e:
      print('Overflow',e)
    return actualText
  
  
  

class EmptyFile(Exception):
  pass

class InvalidEncryptionFormat(Exception):
  pass

class KeyMisMatch(Exception):
  pass

class InvalidPrimeNumberFormat(Exception):
  pass
