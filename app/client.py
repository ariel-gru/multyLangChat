import socket
import app.encryption as encryption
from app.translator import translator
from app.nonce_manager import NonceManager
#I haven't started working on the server and the client yet.

NONCE = NonceManager.get_nonce()#for the AES encryption

my_socket=socket.socket()
my_socket.connect(('127.0.0.1',8820))
while True:
    message = input(' Enter message:')
    if message == "exit" :
        my_socket.close()
        break
    my_socket.send(message.encode())
