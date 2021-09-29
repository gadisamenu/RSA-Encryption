
import Rsa

#Added modular inverse function along with progress bar(percentage) for the encryption/decryption processes

message = input("Enter the message you want to encrypt: ")

secret = Rsa.Rsa()
encrypted_message = secret.encrypt(message)
decrypted_message = secret.decrypt(encrypted_message)
print(decrypted_message)
