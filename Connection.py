import socket
from tkinter import Tk
from tkinter import messagebox

class Connection:
    def __init__(self,bool=False):
        try:
            self.conn = True
            self.ip,self.port = "3.142.167.54",12203
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            if bool:
                self.sock.connect((self.ip,self.port))
        except Exception as e:
            print(e)
            msg_win = Tk()
            msg_win.withdraw()
            messagebox.showerror("Socket error!","You're not connected to the internet or the server is offline!")
            self.conn = False
            msg_win.destroy()
            quit()