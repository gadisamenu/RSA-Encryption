import random
publicKey = 0
privateKey = 0
modulus = 0
firstPrime = 0
secondPrime = 0

def gcd(a,b):
  if b == 0:
    return a
  else:
    return gcd(b,a%b)

def encrypt(message):
    ascii_values = []
    print('\n')
    for character in message:
      ascii_values.append(ord(character))

    cipherNumList = []
    j = 3
    for index,ascii in enumerate(ascii_values):
      cipherNumList.append(pow(ascii,publicKey,modulus))
 
    return cipherNumList

def decrypt(cipherNumList):
    decryptedAscii_list = []
    for index,ascii in enumerate(cipherNumList):
      decryptedAscii_list.append(pow(ascii,privateKey,modulus))
      

    actualText = ''
    for decrypted_ascii in decryptedAscii_list:
      actualText += chr(decrypted_ascii)
    
    return actualText

def fermat_primality_test(number):

  if number % 2 == 0:
    return False

  evenComponent=number-1
  a=random.randrange(1,number)
  if pow(a,evenComponent,number) == 1:
    return True
  return False
  
  
def generatePrime():
  while True:
    primeCandidate = random.randrange(pow(2,100),pow(2,101))
    if fermat_primality_test(primeCandidate):
      return primeCandidate
    

firstPrime = generatePrime()
secondPrime = generatePrime()



modulus = firstPrime * secondPrime

phi = (firstPrime-1) * (secondPrime-1)

for number in range(phi,1,-1):
  if gcd(phi,number) == 1:
    publicKey = number
    break
  
for number in range(phi,1,-1):
  if (publicKey * number) % phi == 1:
    privateKey = number
    print('hello')
    break
  print("he")

message = input("Enter a string to encrypt: ")
encrypted = encrypt(message)
decrypted = decrypt(encrypted)
print(decrypted)