import socket
import app.chatappGUI as chatappGUI
import app.encryption as encryption
from app.nonce_manager import NonceManager
#I haven't started working on the server and the client yet.

NONCE = NonceManager.get_nonce()#for the AES encryption

server_socket= socket.socket()

server_socket.bind(('0.0.0.0',8820))
server_socket.listen()
(client_socket, client_address) = server_socket.accept()
print("Client connected")

while True:
    data=server_socket.recv(2048).decode()
    if data == "exit":
        server_socket.close()
        
        break