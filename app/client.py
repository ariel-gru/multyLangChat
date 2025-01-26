import socket
from chatappGUI import ChatApp
import app.encryption as encryption
from app.translator import translator
from app.nonce_manager import NonceManager
#I haven't started working on the server and the client yet.

NONCE = NonceManager.get_nonce()#for the AES encryption
class Client():
    def __init__(self):
        self.gui = ChatApp()
        self.client_socket=socket.socket()
        self.client_socket.connect(('127.0.0.1',2000))

        dh, pk = encryption.get_dh_public_key()
        self.client_socket.send(pk)
        reply = self.client_socket.recv(2048)
        shared_key =encryption.get_dh_shared_key(dh,reply)
        print("shared key:", shared_key)
        self.cipher = encryption(shared_key,NONCE)
