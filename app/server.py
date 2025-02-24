import socket
import threading
import chatappGUI as chatappGUI
from encryption import Cipher
from nonce import NONCE
import data_base
import json
#I haven't started working on the server and the client yet.

class server:
    def __init__(self):
        self.server_socket = socket.socket()
        self.server_socket.bind(("0.0.0.0", 7000))
        self.server_socket.listen(100)
        
        self.client_list=[]
        
        while True:
            client,address=self.server_socket.accept()
            threading.Thread(target=self.start_server,args=(client,address)).start()

        
    def start_server(self,client,address):
        
        dh, public_key = Cipher.get_dh_public_key()
        client.send(public_key)  # שליחת המפתח הפומבי ללקוח
        client_public_key = client.recv(1024)  # קבלת המפתח הפומבי של הלקוח
        shared_key = Cipher.get_dh_shared_key(dh,  client_public_key)
        print("shared key:", shared_key)
        cipher = Cipher(shared_key, NONCE)

        
        connected = False
        while not connected:
            encrypted_data = client.recv(1024)
            if encrypted_data:
                decrypted_data=cipher.aes_decrypt(encrypted_data)
                json_data = json.loads(decrypted_data)
                
                username = json_data.get("username")
                password = json_data.get("password")
                opertation = json_data.get("operation")
                
                DB=data_base.ChatAppDB()

                if opertation == "login":
                    if DB.check_user(username,password):
                        connected =True
                        print("logged in")
                        encrypted_answer=cipher.aes_encrypt(f'language:{DB.get_user_language(username)}'.encode())
                    else:
                        encrypted_answer=cipher.aes_encrypt('you are not connected'.encode())
                    client.send(encrypted_answer)
                
                
                if opertation == "register":
                        print(1)
                        if DB.save_user(username,password):
                            print(12)
                            connected =True
                            print("logged in")
                            encrypted_answer=cipher.aes_encrypt('you are connected'.encode())
                            client.send(encrypted_answer)
                            wating_for_lang = True
                            while wating_for_lang:
                                data = client.recv(1024)
                                data = cipher.aes_decrypt(data)
                                DB.change_language(username,data.split(":")[1])
                                wating_for_lang = False
                        else:
                            encrypted_answer=cipher.aes_encrypt('Username already exists'.encode())
                            client.send(encrypted_answer)
                        
                    


        self.client_list.append((client,address,username,shared_key))
        recv = True
        while recv:
            data = client.recv(1024)
            data = cipher.aes_decrypt(data)
            print(data)
            for i in self.client_list:
                if username != i[2]:
                    print("sending:"+data)
                    client_public_key = Cipher(i[3], NONCE)
                    encrypted_msg_by_specific_client_key=client_public_key.aes_encrypt(data.encode())
                    i[0].send(encrypted_msg_by_specific_client_key)

            
            


        client.close()
        self.server_socket.close()




if __name__ == "__main__":
    server=server()