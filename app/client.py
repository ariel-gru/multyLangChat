import socket
import threading
import chatappGUI
from encryption import Cipher
from translator import Translator
from nonce_manager import NonceManager
#I haven't started working on the server and the client yet.

NONCE = NonceManager.get_nonce()#for the AES encryption

class client:
    def __init__(self):
        self.client_socket = socket.socket()
        self.client_socket.connect(("10.42.57.33", 7000))
        
        
        dh, public_key = Cipher.get_dh_public_key()
        self.client_socket.send(public_key)  # שליחת המפתח הפומבי לשרת
        public_key_server = self.client_socket.recv(1024)  # קבלת המפתח הפומבי של השרת
        shared_key = Cipher.get_dh_shared_key(dh, public_key_server)
        print("shared key:", shared_key)
        self.cipher = Cipher(shared_key, NONCE)
        print("Secure channel established.")
    
    def login(self,data):
        answer =''
        while answer !='you are connected':

            encrypted_message = self.cipher.aes_encrypt(data.encode())

            self.client_socket.send(encrypted_message)
            encryptd_answer = self.client_socket.recv(1024)
            answer = self.cipher.aes_decrypt(encryptd_answer)
            if answer != 'you are connected':
                return False
        return True



if __name__ == "__main__":
    pass
