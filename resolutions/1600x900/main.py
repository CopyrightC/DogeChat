from tkinter import *
import socket
import sys
import os
import speech_recognition as sr
from settings import Settings
from tkinter import ttk
from tkinter import scrolledtext
from functools import partial
from plyer import notification
from tkinter import font
from threading import Thread
from win32api import GetSystemMetrics
from tkinter import simpledialog
from tkinter import messagebox
from Connection import Connection
from webbrowser import open as opw

class ChatWin(Connection):
    '''
    Constructor
    '''
    def __init__(self,old_id,name,cht_nm,cht_psw):
        super().__init__(True)
        self.azure_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'azure-dark.tcl')
        self.name = name
        self.cht_nm = cht_nm
        self.cht_psw = cht_psw
        self.sock.send(f"replace {old_id}".encode())
        self.over = False
        self.shift_press = False
        self.setup= False
        self.letter_index = []
        self.metrics = [GetSystemMetrics(0),GetSystemMetrics(1)]#Getting the monitor resolution
        self.front_thread = Thread(target=self.Frontend) #GUI
        self.recv_thread = Thread(target=self.recv) #Receiving messages from the server

        self.front_thread.start()
        self.recv_thread.start()
    
    def Frontend(self):#User-interface
        theme_list = ['Dark theme', 'Light theme']
        self.root = Tk()
        self.called = False
        self.btnimg = PhotoImage(file = "data/images -win/send1.png",master=self.root)
        self.root.title("Pychat2.0")
        self.style = ttk.Style(self.root)
        self.root.protocol("WM_DELETE_WINDOW",self.handle_quit)
        self.root.tk.call('source',self.azure_path)
        self.style.theme_use('azure-dark')
        self.root.geometry("1600x900")
        cht_font = font.Font(family = "Trebuchet MS",size =17)
        self.cht_place = scrolledtext.ScrolledText(self.root,width=131,height = 27)
        self.cht_place.place(x=5,y=47)
        self.cht_place.configure(font = cht_font)
        sendbtn = Button(self.root,width = 57,height =68,bg="white",image = self.btnimg,command=self.sendmsg)
        sendbtn.place(x=1535,y=819)
        view_rc_psw = ttk.Button(text="View room ID and password",style= "AccentButton",command = self.showidpsw)
        view_rc_psw.place(x=1415,y=10)
        cht_lbl = Label(text="Chat room",font = ("Arial",13),bg = "gray78",fg= "black")
        cht_lbl.place(x=730,y=10)
        self.cht_place.config(state = "disabled")
        self.entry_area = Text(self.root,width = 253,height = 5)
        self.entry_area.place(x=5,y=819)
        self.entry_area.focus_force()
        
        #Binding the keys to some methods
        
        self.root.bind("<Shift_L>",self.checkkeyprs)
        self.root.bind("<KeyRelease>",self.onrel)
        self.root.bind("<Return>",self.sendmsg)
        self.root.mainloop()
    def feedback(self):
        opw(r"https://mail.google.com/mail/u/0/?fs=1&to=shouryasinha001@gmail.com&su=Feedback%20regarding%20PyChat&&tf=cm")
    
    def showidpsw(self):
        messagebox.showinfo("Info",f"Room ID : {self.cht_nm} \n Room password : {self.cht_psw}")

    #Receives messages; called in a thread
    def recv(self):
        
        while not self.over:
            try:
                message1 = self.sock.recv(1024)
                message1 = message1.decode()
                self.cht_place.config(state = 'normal')
                self.cht_place.insert('end',message1)
                self.cht_place.yview('end')
                self.cht_place.config(state = 'disabled')

                '''
                If the chat window isn't in focus then a notification pops up with a sound
                indicating that there's a new message
                '''

                #Remove this comment
                '''
                Notification.txt -> if message from settings(with help of txt) 
                [call it in a thread] -> execute if statement for noti
                '''
                '''
                if str(self.root.focus_get()) == "None":
                    notification.notify(
                        title = "New message!",
                        message = message1,
                        #app_icon = self.icon,
                        timeout = 8
                    )
                '''
            except ConnectionAbortedError:
                break
            
            except Exception as e:
                print(e)
                self.sock.close()
                break
    
    def handle_quit(self):
        self.sock.close()
        exit(0) #Exit code 0
    
    
    def sendmsg(self,*argv): 
      
        if not self.shift_press:
            entrytxt = self.entry_area.get('1.0','end')
            msg = f"{self.name} : {entrytxt}"
            lenx = len(msg)
            if msg[lenx-1] == "\n" : msg = msg.replace(msg[lenx-1],"")
            if len(msg) < 546: #Limiting the maximum character in a single message to 546 letters
                contents = self.entry_area.get('1.0','end').replace('\n',"")
                contents2 = str(contents).replace(' ',"")
                
                if len(contents) > 0 and len(contents2) > 0: #Sending the message to server if the length of message(excluding the line break and spaces) is greater than 0
                    try:
                        self.sock.send(msg.encode())
                        self.sock.send('\n'.encode())
                    except:
                        messagebox.showerror("Error!","You're not connected to the internet!")
                    self.entry_area.delete('1.0','end')
                else:
                    self.entry_area.delete('end','end')
            else:
                messagebox.showerror("Too many characters!","You can't send a message consisting of more than 546 letters! Your message currently has {} characters in it".format(len(msg)))
        
        
    def checkkeyprs(self,event):self.shift_press = True
      
    def onrel(self,event):
        #Checking if shift is released by the user
        if str(event).startswith("<KeyRelease event state=Shift"):self.shift_press = False  


class Main(Connection):
    
    def __init__(self):
        super().__init__(True) #Calling the parent class's Constructor
        self.info_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),r"data\info")
        self.azure_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'azure-dark.tcl')
        try:
            self.joined , self.created = False, False
            self.sock.send("id".encode())
            self.id = self.sock.recv(1024).decode()
            self.mainwin = Tk()
            self.mainwin.protocol("WM_DELETE_WINDOW",self.close_conn)
            self.mainwin.resizable(0,0)
            style = ttk.Style(self.mainwin)
            self.mainwin.tk.call('source',self.azure_path)
            style.theme_use('azure-dark')
            self.load_images()
            width,height = GetSystemMetrics(0),GetSystemMetrics(1)
            self.mainwin.geometry("1600x900")
            self.mainwin.title("Pychat 2.0")
            self.name = self.get_name()
            Thread(target=self.gui).start()   
            self.mainwin.mainloop()
        
        except OSError:
            sys.exit()

    def close_conn(self):
        self.sock.close()
        exit(0)
    
    def load_images(self):
        self.settings_file = PhotoImage(file = r"data/images/settings.png",master=self.mainwin)
        self.back = PhotoImage(file = r'data/images/default.png',master=self.mainwin)

    def gui(self):
        tab = Canvas(width=796,height=45)
        tab_label = Label(text = "Pychat 2.0",bg = "gray40",font = ("Arial",15),fg= "white")
        tab_label.place(x=760,y=12)
        tab.place(x=1,y=0)
        Chats = Canvas(width=300,height=900,bg='gray30')
        Chats.place(x=1,y=47)
        user_block = Canvas(width = 300,height = 61)
        user_block.place(x=1,y=835)
        username_label = Label(text = str(self.username) ,bg = "gray48",font = ("Arial",15),fg= "white")
        username_label.place(x=10,y=850)
        settings = Button(image=self.settings_file,width=40,height=40,command = self.open_settings)
        settings.place(x=250,y=845)
        add_chats = ttk.Button(text="Create Room",width=20,style="AccentButton",command=self.add_chats)
        add_chats.place(x=15,y=91)
        join_chat = ttk.Button(text="Join Room",width=20,style="AccentButton",command=self.join_chat)
        join_chat.place(x=15,y=141)
        self.chat_area = Canvas(width = 495,height=551,bg="gray20")
        lbl = Label(image=self.back)
        lbl.place(x=302,y=46)
        self.chat_area.place(x=302,y=46)

    def join_chat(self):
        try:

            self._join_id = simpledialog.askstring("Room ID","Enter the room ID")
            self._join_psw = simpledialog.askstring("Password","Enter the password")
            if self._join_id == None or self._join_psw == None:
                return
            if self._join_id == "" or self._join_psw == "": #Preventing Attribute error
                messagebox.showerror("Error","Room name or room pass can't be empty!")
                return

            self.sock.send("##%--$$join_room$$--##%".encode())
            msg = self.sock.recv(1024).decode()
            self.sock.send(self._join_id.encode())
            msg = self.sock.recv(1024).decode()
            self.sock.send(self._join_psw.encode())
            msg  = self.sock.recv(1024).decode()
            if msg == "true":
                self.joined = True
                self.mainwin.destroy()                  #Join room here

            else:
                messagebox.showerror("Error","Either of the meeting code or password is invaild.")

        except Exception as e: #Handling error
            print(e)
        
    def add_chats(self):
        self._room_name = simpledialog.askstring("Name","Enter a name for the group")
        self._room_pass = simpledialog.askstring("Password","Create a password")

        if self._room_name == None or self._room_pass == None:
            return
        if self._room_name == "" or self._room_pass == "": #Preventing Attribute error
            messagebox.showerror("Error","Room name or room pass can't be empty!")
            return

        self.sock.send("##%--$$room$$--##%".encode())
        data = self.sock.recv(1024).decode()
        
        if data =="Rins":
            self.sock.send(self._room_name.encode())
        data = self.sock.recv(1024).decode()
        if data == "Psw":
            self.sock.send(self._room_pass.encode())
        data = self.sock.recv(1024).decode()
        if data == "invalid!":
            messagebox.showerror("Error","Please enter a different name or password")
        elif data == "OK":  
            self.created =True
            self.mainwin.destroy()

    def open_settings(self):
        settings = Settings()

    def get_name(self):
        username_file = open(fr'{self.info_dir}/username.txt','r')
        self.username = username_file.read()
        username_file.close()
        return self.username
    
if __name__ == "__main__":
    main = Main() #Object creation
    #main.sock.close()
    if main.created:
        ChatWin(main.id,main.name,main._room_name,main._room_pass)
    elif main.joined:
        ChatWin(main.id,main.name,main._join_id,main._join_psw)