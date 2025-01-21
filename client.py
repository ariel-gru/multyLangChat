import socket
#fs
my_socket=socket.socket()
my_socket.connect(('127.0.0.1',8820))
while True:
    message = input(' Enter message:')
    if message == "exit" :
        my_socket.close()
        break
    my_socket.send(message.encode())
