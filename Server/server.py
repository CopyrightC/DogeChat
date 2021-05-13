import socket
import json
from sys import winver
from threading import Thread
from random import randint
from validate_email import validate_email #pip install validate_email
print("""

Copyright (C) 2021 SATAN01 <shouryasinha001@gmail.com>


                                  ,----,                                                   
                                ,/   .`|                      ,--.                         
  .--.--.      ,---,          ,`   .'  : ,---,              ,--.'|    ,----..        ,---, 
 /  /    '.   '  .' \       ;    ;     /'  .' \         ,--,:  : |   /   /   \    ,`--.' | 
|  :  /`. /  /  ;    '.   .'___,/    ,'/  ;    '.    ,`--.'`|  ' :  /   .     :  /    /  : 
;  |  |--`  :  :       \  |    :     |:  :       \   |   :  :  | | .   /   ;.  \:    |.' ' 
|  :  ;_    :  |   /\   \ ;    |.';  ;:  |   /\   \  :   |   \ | :.   ;   /  ` ;`----':  | 
 \  \    `. |  :  ' ;.   :`----'  |  ||  :  ' ;.   : |   : '  '; |;   |  ; \ ; |   '   ' ; 
  `----.   \|  |  ;/  \   \   '   :  ;|  |  ;/  \   \'   ' ;.    ;|   :  | ; | '   |   | | 
  __ \  \  |'  :  | \  \ ,'   |   |  ''  :  | \  \ ,'|   | | \   |.   |  ' ' ' :   '   : ; 
 /  /`--'  /|  |  '  '--'     '   :  ||  |  '  '--'  '   : |  ; .''   ;  \; /  |   |   | ' 
'--'.     / |  :  :           ;   |.' |  :  :        |   | '`--'   \   \  ',  /    '   : | 
  `--'---'  |  | ,'           '---'   |  | ,'        '   : |        ;   :    /     ;   |.' 
            `--''                     `--''          ;   |.'         \   \ .'      '---'   
                                                     '---'            `---`                
                                                                                           
""")
class Connection:

    #Constructor

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.bind(('0.0.0.0',65432))
        self.sock.listen()
        self.details = {}
        self.arr_clients = []
        print("Server is listening...")
        
        while True:
            self._conn,addr = self.sock.accept() #Aceept incoming connections
            
            print(f"Connected to {addr}")
            Thread(target=self._recv,args=(self._conn,)).start() #args need to be a tuple

    #recv method; separate for each client (called in a thread)

    def _recv(self,client):
        result = False
        while True:
            try:
                self.data = client.recv(1024).decode()

                if self.data == "##%--$$regis$$--##%":
                    client.send("recv".encode())
                    email = client.recv(1024).decode()
                    client.send("user".encode())
                    self.username = client.recv(1024).decode()

                    client.send("pass".encode())
                    self.password = client.recv(1024).decode()
                    
                    self._email_validation(email,client)
                
                if self.data == "##%--$$room$$--##%":
                    client.send("Rins".encode())
                    name = client.recv(1024).decode()
                    client.send("Psw".encode())
                    passw = client.recv(1024).decode()

                    try:
                        if self.details[name] == passw:
                            client.send("invalid!".encode())
                    except:
                        client.send("OK".encode())
                        self._store_psw_id(name,passw,client)

                if self.data == "##%--$$join_room$$--##%":
                    client.send("jroom".encode())
                    id = client.recv(1024).decode()
                    client.send('jpsw'.encode())
                    jpsw = client.recv(1024).decode()
                    
                    for jrooms in self.arr_clients:
                        if jrooms[0] == [id,jpsw]:
                            jrooms[1].append(client)
                            _recv_thr = Thread(target=self._recv_thread,args=client)
                            _recv_thr.start()
                            result = True
                            client.send("true".encode())

                    if not result:
                        client.send('false'.encode())

                if self.data == "psw_chck":
                    client.send("Send".encode())
                    id_psw = client.recv(1024).decode().split()
                    boolx = self.check_id_psw(id_psw)
                    if boolx:
                        client.send("New".encode())
                        new_psw = client.recv(1024).decode()
                        self.change_psw(id_psw[0],new_psw)
                        client.send("Changed".encode())
                    else:
                        client.send("Failed".encode())

                if self.data == "id":
                    self._conn.send(str(self._conn).encode())

                if self.data.startswith("replace"):
                    listx = self.data.split()
                    listx.pop(0)
                    old_id = "".join(listx)

                    for rooms in self.arr_clients:
                        for clients in rooms[1]:
                            clx = str(clients).replace(" ","")
                            if clx == old_id:
                                rooms[1].remove(clients)
                                rooms[1].append(client)
                                self._recv_thread(client)

                if self.data.startswith(";#';'%$&,,..--=reso_settings "):
                    id = self.data.split()[1]
                    client.send("go".encode())
                    new_reso = client.recv(1024).decode()
                    self.update_client_reso(id,new_reso)

                if self.data.startswith("^^&&/./,.,reso--MYID"):
                    client.send("send".encode())
                    idx = client.recv(1024).decode()
                    reso = self.check_id_reso(idx)
                    client.send(reso.encode())

#Handle quit event here
#and remove the client for arr
#and his room from self.details

            except ConnectionResetError:
                client.close()

            except OSError:
                client.close()

    def check_id_reso(self,id):
        json_data = json.load(open(r'resolutions.json'))
        try:
            reso = json_data[id]
            return reso

        except:
            return "None"
    #Check if the email is valid or not 
    
    def _email_validation(self,email,client):
        is_valid = validate_email(email)

        if is_valid:
            client.send("valid".encode())
            id = self.generate_id()
            client.send(str(id).encode())
            self._save_users(self.username,self.password,id)
            self.save_mail(email)

        else:
            client.send("incorrect!".encode())

    #Save the email in a text file

    def save_mail(self,email):
        file = open(r'server files/email.txt','w')
        file.write(email)
        file.close()

    #Save the username in a text file

    def _save_users(self,name,psw,id):
        boolx = False
        with open(r'server files/users.txt','w') as u:
            u.write(name)

        try:
            json_data = json.load(open(r'serverdata.json'))
            json_data[id] = psw

        except json.decoder.JSONDecodeError:
            boolx = True

        with open(r'serverdata.json','w') as js:

            if not boolx:
                json.dump(json_data,js)
            else:
                wr = json.dumps({id:psw})
                js.write(wr)

    def update_client_reso(self,id,new_reso):
        json_data = json.load(open(r'resolutions.json'))
        json_data[id] = new_reso
        
        data = json.dumps(json_data)
        with open("resolutions.json","w") as js:
            js.write(data)

    #Store the id and password of the room in a dict
    def generate_id(self):

        id = randint(10000,100000)
        ids = self.check_ids()
        if not ids == "Empty":
            while id in ids:
                id = randint(10000, 100000)

        with open(r'server files\used_ids.txt','a+') as fp:
            fp.write(str(id) + "\n")

        return id

    def change_psw(self,id,psw):
        json_data = json.load(open(r'serverdata.json'))
        json_data[id] = psw
        wr = json.dumps(json_data)
        with open(r'serverdata.json','w') as js:
            js.write(wr) 

    def _store_psw_id(self, id, passw,client):
        self.details[id] = passw
        self.arr_clients.append([[id,passw],[client]])  #    [[[id,passw],[client]]] format list
        self._recv_thread(client)
    
    def check_ids(self):
        with open(r'server files\used_ids.txt',"r+") as ud:
            data = ud.read().split("\n")
            try:
                data = [int(x) for x in data] #Converting str -> int
            except Exception:
                return "Empty"

        return data

    def check_id_psw(self,listx):
        json_data = json.load(open(r'serverdata.json'))
    
        if json_data[listx[0]] == listx[1]:
            return True
        return False

class Threading(Connection):

    def __init__(self):
        super().__init__() #Parent's class constructor
        print(self.arr_clients) 

    def _recv_thread(self,client):
        while True:
            try:
                msg = client.recv(1024)
                for rooms in self.arr_clients:
                    for clients in rooms[1]:
                        if clients == client:
                            arr = rooms[1].copy()
                            self.broadcast(arr,msg)
                            break

            except Exception as e:
                client.close()

    def broadcast(self,arr,msg):
        for client in arr:
            client.send(msg)
            
threads = Threading()