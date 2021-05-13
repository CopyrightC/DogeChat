from tkinter import *
from tkinter import messagebox
import socket
import smtplib
import sys
from os import system
from random import randint
from Connection import Connection

class Register(Connection):
    def __init__(self):

        x = self.if_Registered()
        if x:
            system('main.py')
            quit()
        super().__init__(True)
        self.conn = True

        if self.conn:
            self.parent = Tk()
            self.parent.withdraw()
            self.window = Toplevel()
            self.window.protocol("WM_DELETE_WINDOW",self.close)
            self.window.config()
            self.window.geometry("800x600")
            self.window.configure(bg='gray20')
            self.window.title("Pychat 2.0")
            self.gui()
            self.window.mainloop()
            self.parent.mainloop()

    def gui(self):
        label = Label(self.window,text = "Register",bg= "gray20",fg = "white",font=("Arial",15))
        label.place(x=360,y=20)
        email_lbl = Label(self.window,text = "Email address",bg="gray20",fg= "white",font = ("Arial",15))
        email_lbl.place(x= 20,y= 90)
        self.email_entry = Text(self.window,height= 2,width=20)
        self.email_entry.place(x=190,y=90)
        self.email_entry.insert(INSERT,'shouryasinha001@gmail.com')
        user_lbl = Label(self.window,text = "Username",bg="gray20",fg= "white",font = ("Arial",15))
        user_lbl.place(x=20,y=150)
        self.username_entry = Text(self.window,height = 2,width=20)
        self.username_entry.place(x=190,y=150)
        pass_lbl = Label(self.window,text = "Password",bg="gray20",fg= "white",font = ("Arial",15))
        pass_lbl.place(x=20,y=210)
        self.pass_entry = Text(self.window,height = 2,width=20)
        self.pass_entry.place(x=190,y=210)
        register_btn = Button(self.window,text="Register!",bg="blue",fg="white",width= 10,height=2,command=self.send_mail)
        register_btn.place(x=20,y=290)

        label2 = Label(self.window,text = "Already a member?",bg="gray20",fg= "white",font = ("Arial",15))
        label2.place(x=20,y=420)
        log_inlbl = Label(self.window,text= "Log in",bg="gray20",fg= "purple1",font = ("Arial",15))
        log_inlbl.place(x=199,y=420)

    def close(self):
        sys.exit()

    def send_mail(self):
        self.email = self.email_entry.get('1.0','end-1c')
        self.username = self.username_entry.get('1.0','end-1c')
        self.password = self.pass_entry.get('1.0','end-1c')
        self.sock.send("##%--$$regis$$--##%".encode())
        cmd = self.sock.recv(1024).decode()
        if cmd == "recv":
            self.sock.send(self.email.encode())
            cmd  = self.sock.recv(1024).decode()
            if cmd == "user":
                self.sock.send(self.username.encode())
                cmd  = self.sock.recv(1024).decode()
                if cmd == "pass":
                    self.sock.send(self.password.encode())
                    cmd  = self.sock.recv(1024).decode()
                    if cmd == "valid":
                        idx = self.sock.recv(1024).decode()
                        print(idx)
                        self.store(idx)
                        self.load_win2()
                    elif cmd == "incorrect!":
                        messagebox.showerror("Invalid!",self.email + "is not a valid email id")

    def store(self,id):
        with open(r'data\info\id.txt','r+') as ids:
            ids.write(id)
            print("done done")

    def load_win2(self):
        username_file = open(r'data/info/username.txt','w')
        username_file.write(self.username)
        username_file.close()
        password_file = open(r'data\info\password.txt','w')
        password_file.write(self.password)
        password_file.close()
        self.registered()
        messagebox.showinfo("Success!","Registered successfully!")
        self.window.destroy()
        system("main.py")
        quit()
    
    def registered(self):
        file = open(r'data/info/registered.txt','w')
        file.write('registered')
        file.close()
    
    def if_Registered(self):
        file1 = open(r'data/info/registered.txt')
        x = file1.read()
        if x == "registered":
            return True
        else:
            return False
    
register = Register() 