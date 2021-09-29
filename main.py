from Rsa import *

print('************** 1024 bit RSA Encryption for Text files only **************\n')

command = input("Enter: \n 'e'-to encrypt a file\n 'd'-to decrypt a file\n 'n' -to generate new keys\n 'q'-to quit\n").lower()

if not Rsa.initialize():
    exit(1)
    
if command == 'e':
  
  file_path =  input("Please Enter the filename or directory of the file: ")
  try:
    file = open(file_path,'r')
    message = file.read()
    if message == '':
      raise EmptyFile
    cipherText = Rsa.encrypt(message)
    file.close()
    secure_file = open('Encrypted_Files/'+file_path,'w')
    secure_file.write(cipherText)
    secure_file.close()
  except FileNotFoundError as fnot:
    print("Could not find the file specified! ",fnot)
  except TypeError as wrongtype:
    print("Only character streams are allowed! ",wrongtype)
  except EmptyFile:
    print("The file '"+file.name+"' is empty")
    
elif command == 'd':
  Rsa.initialize()
  file_path =  input("Please Enter the full directory of the file: ")
  try:
    file = open(file_path,'r')
    cipherText = file.read()
    file.close()
    message = Rsa.decrypt(cipherText)
    index = file_path.rfind('/')
    file_name = file_path[index+1:]

    new_file = open('Decrypted_Files/'+file_name,'w')
    new_file.write(message)
    new_file.close()
  except FileNotFoundError as fnot:
    print(fnot)
  except TypeError as wrongtype:
    print(wrongtype)
  except InvalidEncryptionFormat:
    print('This file is not Encrypted by this application!')
  except KeyMisMatch:
    print("Wrong public and private key pairs!")

elif command == 'n':
  Rsa.generateNewKey()
elif command == 'q':
  exit(0)
else:
  print('Invalid command!\n')
