from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from typing import Set
from Connection import Connection
from functools import partial
import sys

#Main class
class Settings(Connection): 

    def __init__(self):
        super().__init__(True) #Parent's class constructor
        self.settings_win = Tk() 
        self.settings_win.geometry("800x600")
        self.settings_win.title("Settings")
        style = ttk.Style(self.settings_win)
        self.settings_win.tk.call('source','azure-dark.tcl')
        style.theme_use('azure-dark')
        self.main()
        self.settings_win.mainloop()
    
    #Get username
    def get_name(self):
        username_file = open(r'data/info/username.txt','r')
        self.username = username_file.read()
        username_file.close()
        return self.username

    #Resolution settings window
    def reso_settings(self):
        self.settings_win.destroy()
        self.resowin = Tk()
        self.resowin.title("Resolution settings")
        self.resowin.geometry("800x600")
        res_sty = ttk.Style(self.resowin)
        self.resowin.tk.call('source','azure-dark.tcl')
        res_sty.theme_use('azure-dark')
        lbl = Label(self.resowin,text= "Change my resolution to :",font = ("Arial",13))
        lbl.place(x=20,y=50)

        reso1 = ttk.Button(self.resowin,text = "800x600",style = "AccentButton",command = lambda : self.change_reso("800x600"))
        reso2 = ttk.Button(self.resowin,text = "1366x768",style = "AccentButton",command = lambda : self.change_reso("1366x768"))
        reso3 = ttk.Button(self.resowin,text = "1600x900",style = "AccentButton",command = lambda : self.change_reso("1600x900"))
        reso4 = ttk.Button(self.resowin,text = "1600x1200",style = "AccentButton",command = lambda : self.change_reso("1600x1200"))

        reso1.place(x=20,y=120)
        reso2.place(x=20,y=180)
        reso3.place(x=20,y=240)
        reso4.place(x=20,y=300)
        
        self.resowin.mainloop()
    
    def change_reso(self,s):
        with open(r'data/info/id.txt') as id:
            myid = str(id.read())

        self.sock.send(f";#';'%$&,,..--=reso_settings {myid}".encode())
        cmd = self.sock.recv(1024).decode()
        print("RECIVED")
        if cmd == "go":
            self.sock.send(s.encode())
            print("sent")
        messagebox.showinfo("Success","Changes saved successfully! \n Note : You need to restart the application in order for the changes to take place.")
    #Mainwindow ; frontend code
    def main(self):

        self.username = self.get_name()
        set_lbl = Label(self.settings_win,text="Settings",font = ("Arial",13),bg = "gray78",fg= "black")
        set_lbl.place(x=370,y=10)
        lbl = ttk.Label(self.settings_win,text = "Name",font = ("Helvetica",13))
        lbl.place(x=30,y=88)
        self.entry = ttk.Entry(self.settings_win,width=40)
        self.entry.place(x=130,y=80)
        self.entry.insert(0,self.username)
        self.change_pass = ttk.Button(self.settings_win,text = "Change password",style = "AccentButton",command =self.change_passw)
        self.change_pass.place(x=30,y=180)
        self.settings_win.resizable(0,0)
        btn = ttk.Button(self.settings_win,text="Save changes",style='AccentButton',command=self.save_changes)
        btn.place(x=670,y=535)
        log_out= ttk.Button(self.settings_win,text = "Log Out",command=self.log_out)
        log_out.place(x=30,y=535)
        change_reso = ttk.Button(self.settings_win,text = "Resolution settings",style = "AccentButton",command = self.reso_settings)
        change_reso.place(x=30,y=250)
    
    #Change username
    def change_name(self,name):
        _file = open('data/info/username.txt','w')
        _file.truncate()
        _file.write(name)
        _file.close()

    #Logout -> clear all txt files
    def log_out(self):

        with open(r'data\info\email.txt',"a+") as em:
            em.truncate(0)
        with open(r'data\info\id.txt',"a+") as em:
            em.truncate(0)
        with open(r'data\info\notification.txt',"a+") as em:
            em.truncate(0)
        with open(r'data\info\password.txt',"a+") as em:
            em.truncate(0)
        with open(r'data\info\registered.txt',"a+") as em:
            em.truncate(0)
        with open(r'data\info\username.txt',"a+") as em:
            em.truncate(0)

        self.sock.close()
        messagebox.showinfo("Loged out!","Successfully looged out!")
        sys.exit()

    #Commit changes
    def save_changes(self):
        try:
            if self.entry.get() != self.username:
                self.change_name(self.entry.get())
                messagebox.showinfo("Success","Changes saved successfully! \n Note : You need to restart the application in order for the changes to take place.")
                
        except Exception as e:
            print(e)

             
    def change_passw(self):
    
        with open(r'data\info\id.txt') as filex:
            _id = filex.read()
        window = Toplevel(width = 600,height = 400)
        window.resizable(0,0)

        lbl0 = Label(window,text= "Password settings",font = ("Arial",13),bg = "gray78",fg= "black")
        lbl0.place(x=240,y=10)
        lbl1 = Label(window,text= "Enter your old password",font = ("Arial",13))
        lbl1.place(x=10,y=80)
        lbl2 = Label(window,text= "Enter the new password",font = ("Arial",13))
        lbl2.place(x=10, y= 140)
        lbl3 = Label(window,text= "Confirm the new password",font = ("Arial",13))
        lbl3.place(x=10,y=200)
        
        self.old_psw = ttk.Entry(window,width=40)
        self.old_psw.place(x=220,y=80)
        self.new_psw = ttk.Entry(window,width=40,show = "*")
        self.new_psw.place(x=220,y=140)
        self.conf = ttk.Entry(window,width=40,show = "*")
        self.conf.place(x=220,y=200)
        self.btn = ttk.Button(window,text = "Show",style = "AccentButton",command = self.normal_text)
        self.btn.place(x=490,y=140)
        btn_sve = ttk.Button(window,text="Save changes",style='AccentButton',command= self.save_psw)
        btn_sve.place(x= 485,y=350)
        window.title("Change password")
        window.mainloop()
            
    # * -> text

    def normal_text(self):
        self.conf.config(show="")
        self.new_psw.config(show="")
        self.btn.config(text="Hide",command = self.hide_text)

    # text -> *

    def hide_text(self):
        self.conf.config(show="*")
        self.new_psw.config(show = "*")
        self.btn.config(text = "Show",command = self.normal_text)

    #Change psw
    # Client requests server to check the old psw
    # if it's valid then server changes the password(updates the json file)
    # View Server/Server.py for refernece
    def save_psw(self):
        with open(r'data\info\id.txt') as em:
            self.id = em.read()

        old_psw = self.old_psw.get()
        new_psw = self.new_psw.get()
        conf_psw = self.conf.get()

        if new_psw != conf_psw:
            messagebox.showerror("Error","Passwords don't match!")
        else:
            self.sock.send("psw_chck".encode())
            cmd = self.sock.recv(1024).decode()
            if cmd == "Send":
                data = f"{self.id} {str(old_psw)}"
                self.sock.send(data.encode())
                command = self.sock.recv(1024).decode()
                if command == "New":
                    self.sock.send(f"{str(new_psw)}".encode())
                    cmd = self.sock.recv(1024)
                    messagebox.showinfo("Success","Password changed successfully!")
                    self.sock.close()
                else:
                    messagebox.showinfo("Failed","Incorrect password!")

#Settings()