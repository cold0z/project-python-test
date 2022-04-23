import base64
from cryptography.fernet import Fernet

def generate_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    """
    Load the previously generated key
    """
    keyF = open("secret.key", "rb")
    return keyF

def encrypt_message(message):
    """
    Encrypts a message
    """
    key1 = load_key()
    key = key1.read()
    key1.close()
    
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    new_message = base64.b64encode(encrypted_message)

    return str(new_message)

def decrypt_message(encrypted_message):
    """
    Decrypts an encrypted message
    """
    key1 = load_key()
    key = key1.read()
    key1.close()
    f = Fernet(key)
    decode64_message = base64.b64decode(encrypted_message)
    decrypted_message = f.decrypt(decode64_message)

    return str(decrypted_message.decode())


if __name__ == "__main__":
    encrypt_message("encrypt this message")