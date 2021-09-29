
import Rsa

#Removes the tedious generation of new prime numbers/keys everytime the program runs and Enables the generation of new keys at the user's will

secret = Rsa.Rsa()
message = input("Enter the message you want to encrypt: ").lower()
command = input("Do you want to generate new keys(Y/N)?: ").lower()
if command == 'y':
  secret.generateKeys()
elif command == 'n':
  secret.initialize()
else:
  print("Invalid command!")
  
encrypted_message = secret.encrypt(message)
decrypted_message = secret.decrypt(encrypted_message)
print(decrypted_message)
