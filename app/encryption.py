#pip install pycryptodome
from Crypto.Cipher import AES
#pip install py-diffie-hellman
from diffiehellman import DiffieHellman
from nonce import NONCE


class Cipher:
    def __init__(self, key, nonce):
        """
        Initializes the Cipher object with an encryption key and a nonce.
        """
        self.key = key # AES encryption key
        self.nonce = nonce # Nonce value for AES (must match between encryption and decryption)

    def aes_encrypt(self, txt):
        """
        Encrypts the given text using AES encryption.
        """
        cipher = AES.new(self.key, AES.MODE_EAX,  nonce=self.nonce) # Initialize AES cipher in EAX mode
        ciphertext, tag = cipher.encrypt_and_digest(txt) # Encrypt the plaintext and generate authentication tag
        return ciphertext # Return the ciphertext

    def aes_decrypt(self, cipher_text):
        """
        Decrypts the given ciphertext using AES decryption.
        """
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=self.nonce)  # Initialize AES cipher with same nonce
        msg = cipher.decrypt(cipher_text) # Decrypt the ciphertext
        return msg.decode('utf-8') # Return the decoded plaintext

    @staticmethod
    def get_dh_public_key():
        """
        Generates a Diffie-Hellman public key.
        """
        dh = DiffieHellman(group=14, key_bits=540) # Create a Diffie-Hellman object with group 14 and 540-bit key
        pk = dh.get_public_key()  # Generate the public key
        return dh, pk # Return the DH object and its public key

    @staticmethod
    def get_dh_shared_key(dh, pk, lngth=32): 
        """
        Generates a shared secret key using Diffie-Hellman key exchange.
        """
        dh_shared = dh.generate_shared_key(pk) # Generate shared key using the other party's public key
        return dh_shared[:lngth] # Return the first 'lngth' bytes of the shared key


if __name__ == "__main__":

    text = b"testing: hello world"
    PUBLIC_KEY = b"it is my secret password"
    print("text before:", text)

    c1 = Cipher(PUBLIC_KEY, NONCE)
    encrypted_text = c1.aes_encrypt(text)
    c2 = Cipher(PUBLIC_KEY, NONCE)
    message = c2.aes_decrypt(encrypted_text)
    print("text after: ", message)

    dh1, dh1_public = Cipher.get_dh_public_key()
    dh2, dh2_public = Cipher.get_dh_public_key()

    sk1 = Cipher.get_dh_shared_key(dh1, dh2_public)
    sk2 = Cipher.get_dh_shared_key(dh2, dh1_public)
    print("shared key 1: ", sk1)
    print("shared key 2: ", sk2)
