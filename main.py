import random,Rsa


message = input("Enter the message you want to encrypt: ")

secret = Rsa.Rsa()
encrypted_message = secret.encrypt(message)
print(encrypted_message)
decrypted_message = secret.decrypt(encrypted_message)
print(decrypted_message)
