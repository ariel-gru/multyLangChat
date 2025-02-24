import socket
import threading
import chatappGUI
from encryption import Cipher
from nonce import NONCE
#I haven't started working on the server and the client yet.



class client:
    def __init__(self):
        self.client_socket = socket.socket()
        self.client_socket.connect(("127.0.0.1", 7000))
        
        
        dh, public_key = Cipher.get_dh_public_key()
        self.client_socket.send(public_key)  # שליחת המפתח הפומבי לשרת
        public_key_server = self.client_socket.recv(1024)  # קבלת המפתח הפומבי של השרת
        shared_key = Cipher.get_dh_shared_key(dh, public_key_server)
        print("shared key:", shared_key)
        self.cipher = Cipher(shared_key, NONCE)
        print("Secure channel established.")
    
    def login(self,data):
        answer =''
        while 'language:' not in answer:

            encrypted_message = self.cipher.aes_encrypt(data.encode())

            self.client_socket.send(encrypted_message)
            encryptd_answer = self.client_socket.recv(1024)
            answer = self.cipher.aes_decrypt(encryptd_answer)
            if 'language:' not in answer:
                return False , ""
        print(answer.split(':')[1])
        print(answer)
        return True,answer.split(':')[1]
    
    def register(self,data):
        answer =''
        while answer !='you are connected':

            encrypted_message = self.cipher.aes_encrypt(data.encode())

            self.client_socket.send(encrypted_message)
            encryptd_answer = self.client_socket.recv(1024)
            answer = self.cipher.aes_decrypt(encryptd_answer)
            if answer != 'you are connected':
                return False
        print(3)
        return True
    def get_msg(self, message_callback):
        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                msg = self.cipher.aes_decrypt(data)
                if msg:
                    message_callback(msg)
        except Exception as e:
            print(f"Connection lost: {e}")
        
    def change_lang(self,language):
        msg = "change language:"+language
        encrypted_msg = self.cipher.aes_encrypt(msg.encode())
        self.client_socket.send(encrypted_msg)

    
    def snd_msg(self,message,username):
            msg=message
            print(msg)
            msg=username+":"+chr(0)+msg
            encrypted_msg = self.cipher.aes_encrypt(msg.encode())
            self.client_socket.send(encrypted_msg)



if __name__ == "__main__":
    pass
