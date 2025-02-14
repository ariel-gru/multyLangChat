#pip install pycryptodome
from Crypto.Cipher import AES
#pip install py-diffie-hellman
from diffiehellman import DiffieHellman
from nonce_manager import NonceManager


class Cipher:
    def __init__(self, key, nonce):
        self.key = key
        self.nonce = nonce

    def aes_encrypt(self, txt):
        cipher = AES.new(self.key, AES.MODE_EAX,  nonce=self.nonce)
        ciphertext, tag = cipher.encrypt_and_digest(txt)
        return ciphertext

    def aes_decrypt(self, cipher_text):
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=self.nonce)
        msg = cipher.decrypt(cipher_text)
        return msg.decode('utf-8')

    @staticmethod
    def get_dh_public_key():
        dh = DiffieHellman(group=14, key_bits=540)
        pk = dh.get_public_key()
        return dh, pk

    @staticmethod
    def get_dh_shared_key(dh, pk, lngth=32):
        dh_shared = dh.generate_shared_key(pk)
        return dh_shared[:lngth]


if __name__ == "__main__":

    text = b"testing: hello world"
    PUBLIC_KEY = b"it is my secret password"
    NONCE =  NonceManager.get_nonce()
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
