from cryptography.fernet import Fernet

message = "hello geeks"
fernet = Fernet("hej")
encMessage = fernet.encrypt(message.encode())
print("original string: ", message)
print("encrypted string: ", encMessage)
decMessage = fernet.decrypt(encMessage).decode()
print("decrypted string: ", decMessage)

