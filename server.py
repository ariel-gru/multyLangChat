import socket
import chatappGUI

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