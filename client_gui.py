import socket
import tkinter as tk
from tkinter import font
from tkinter import ttk
from tkinter import filedialog
import time
import threading
import os
import re


class GUI:

    def __init__(self, ip_address, port):
        '''
        Inisiasi pembuatan GUI client
        '''
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((ip_address, port))

        self.Window = tk.Tk()                                           #pembuatan window/ gui client
        self.Window.withdraw()

        self.login = tk.Toplevel()                                      #pembuatan header untuk login

        self.login.title("Login")                                       #title window login
        self.login.resizable(width=False, height=False)                 #set ukuran window login
        self.login.configure(width=400, height=350)

        self.pls = tk.Label(self.login,
                            text="Silakan Login Untuk Masuk Chat Room",
                            justify=tk.CENTER,
                            font="Helvetica 12 bold")                   #membuat label pada window login

        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)             #set posisi label window login

        self.userLabelName = tk.Label(
            self.login, text="Username: ", font="Helvetica 11")
        self.userLabelName.place(relheight=0.2, relx=0.1, rely=0.25)

        self.userEntryName = tk.Entry(self.login, font="Helvetica 12")
        self.userEntryName.place(
            relwidth=0.4, relheight=0.1, relx=0.35, rely=0.30)
        self.userEntryName.focus()

        self.roomLabelName = tk.Label(
            self.login, text="Room Id: ", font="Helvetica 12")
        self.roomLabelName.place(relheight=0.2, relx=0.1, rely=0.40)

        self.roomEntryName = tk.Entry(
            self.login, font="Helvetica 11")
        self.roomEntryName.place(
            relwidth=0.4, relheight=0.1, relx=0.35, rely=0.45)

        self.go = tk.Button(self.login,
                            text="CONTINUE",
                            font="Helvetica 12 bold",
                            command=lambda: self.goAhead(self.userEntryName.get(), self.roomEntryName.get()))   #set button continue ke room

        self.go.place(relx=0.35, rely=0.62)

        self.Window.mainloop()

    def goAhead(self, username, room_id=0):
        '''
        Perpindahan window login ke group chat
        '''
        self.name = username
        self.room_id = room_id
        self.server.send(str.encode(username))          #mengirimkan nama ke server
        time.sleep(0.1)
        self.server.send(str.encode(room_id))           #mengirimkan room id ke server

        self.login.destroy()                            #menghilangkan window login
        self.layout()                                   #menampilkan window group chat

        rcv = threading.Thread(target=self.receive)     #membuat thread untuk client tertentu
        rcv.start()

    def layout(self):
        '''
        Tampilan GUI group chat
        '''
        self.Window.deiconify()
        self.Window.title("Room Chat")
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=470, height=600, bg="#17202A")
        self.chatBoxHead = tk.Label(self.Window,
                                    bg="#17202A",
                                    fg="#EAECEE",
                                    text=self.name +
                                    " [ " + self.room_id + " ]",
                                    font="Helvetica 11 bold",
                                    pady=5)

        self.chatBoxHead.place(relwidth=1)

        self.line = tk.Label(self.Window, width=450, bg="#ABB2B9")

        self.line.place(relwidth=1, rely=0.07, relheight=0.02)

        self.textCons = tk.Text(self.Window,
                                width=20,
                                height=3,
                                bg="#17202A",
                                fg="#EAECEE",
                                font="Helvetica 11",
                                padx=5,
                                pady=5)

        self.textCons.place(relheight=0.705, relwidth=1, rely=0.15)
        
        self.line = tk.Label(self.Window, width=450, bg="#ABB2B9")

        self.line.place(relwidth=1, rely=0.07, relheight=0.02)

        self.textTag = tk.Text(self.Window,
                                width=20,
                                height=2,
                                bg="#46617f",
                                fg="#EAECEE",
                                font="Helvetica 11",
                                padx=5,
                                pady=5)

        self.textTag.place(relheight=0.08, relwidth=1, rely=0.08)

        self.labelBottom = tk.Label(self.Window, bg="#ABB2B9", height=80)

        self.labelBottom.place(relwidth=1,
                               rely=0.8)

        self.entryMsg = tk.Entry(self.labelBottom,
                                 bg="#2C3E50",
                                 fg="#EAECEE",
                                 font="Helvetica 11")
        self.entryMsg.place(relwidth=0.74,
                            relheight=0.03,
                            rely=0.008,
                            relx=0.011)
        self.entryMsg.focus()

        self.buttonMsg = tk.Button(self.labelBottom,
                                   text="Send",
                                   font="Helvetica 10 bold",
                                   width=20,
                                   bg="#ABB2B9",
                                   command=lambda: self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.03,
                             relwidth=0.22)

        self.labelFile = tk.Label(self.Window, bg="#ABB2B9", height=70)

        self.labelFile.place(relwidth=1,
                             rely=0.9)

        self.fileLocation = tk.Label(self.labelFile,
                                     text="Choose file to send",
                                     bg="#2C3E50",
                                     fg="#EAECEE",
                                     font="Helvetica 11")
        self.fileLocation.place(relwidth=0.65,
                                relheight=0.03,
                                rely=0.008,
                                relx=0.011)

        self.browse = tk.Button(self.labelFile,
                                text="Browse",
                                font="Helvetica 10 bold",
                                width=13,
                                bg="#ABB2B9",
                                command=self.browseFile)
        self.browse.place(relx=0.67,
                          rely=0.008,
                          relheight=0.03,
                          relwidth=0.15)

        self.sengFileBtn = tk.Button(self.labelFile,
                                     text="Send",
                                     font="Helvetica 10 bold",
                                     width=13,
                                     bg="#ABB2B9",
                                     command=self.sendFile)
        self.sengFileBtn.place(relx=0.84,
                               rely=0.008,
                               relheight=0.03,
                               relwidth=0.15)

        self.textCons.config(cursor="arrow")
        scrollbar = tk.Scrollbar(self.textCons)
        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.textCons.yview)
        self.textCons.config(state=tk.DISABLED)


        self.textTag.config(cursor="arrow")
        scrollbar = tk.Scrollbar(self.textTag)
        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.textTag.yview)
        self.textTag.config(state=tk.DISABLED)

    def browseFile(self):
        '''
        Mencari file (txt) untuk dikirim ke server
        '''
        self.filename = filedialog.askopenfilename(initialdir="/",
                                                   title="Select a file",
                                                   filetypes=(("Text files",
                                                               "*.txt*"),
                                                              ("all files",
                                                               "*.*")))
        self.fileLocation.configure(
            text=self.filename)

    def sendFile(self):
        '''
        Mengirim file beserta ukurannya ke server
        '''
        self.server.send("FILE".encode())
        time.sleep(0.1)
        self.server.send(
            str(self.name + os.path.basename(self.filename)).encode())
        time.sleep(0.1)
        self.server.send(str(os.path.getsize(self.filename)).encode())
        time.sleep(0.1)

        file = open(self.filename, "rb")
        data = file.read(1024)
        while data:
            self.server.send(data)
            data = file.read(1024)
        self.textCons.config(state=tk.DISABLED)
        self.textCons.config(state=tk.NORMAL)
        self.textCons.insert(tk.END, "You sent a file :  "
                                     + str(os.path.basename(self.filename))
                                     + "\n\n")
        self.textCons.config(state=tk.DISABLED)
        self.textCons.see(tk.END)

    def sendButton(self, msg):
        '''
        Mengirimkan isi text field setelah button ditekan
        '''
        self.textCons.config(state=tk.DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, tk.END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()

    def receive(self):
        '''
        Menerima pesan dari server
        '''
        def checkTag(msg):
            '''
            Mengecek nama yang di tag oleh pengirim pesan dengan nama penerima
            '''
            arrmsg = msg.split(' ')
            for i in range(len(arrmsg)):
                # print('check arrmsg:',arrmsg[i])
                if(re.search('@',arrmsg[i])):
                    userMention = arrmsg[i].split('@')
                    if(userMention[1]== self.name):
                        return(True)

        def parseSender(msg):
            '''
            Parsing untuk mengetahui nama pengirim pesan
            '''
            if(msg!=''):
                arrmsg = msg.split(' : ')
                return(arrmsg[0])

        while True:
            try:
                message = self.server.recv(1024).decode()

                if str(message) == "FILE":                          #jika pesan berupa 'FILE'
                    file_name = self.server.recv(1024).decode()
                    lenOfFile = self.server.recv(1024).decode()
                    send_user = self.server.recv(1024).decode()

                    if os.path.exists(file_name):                   #jika ada file dengan path/ direktori yang sama maka hapus file
                        os.remove(file_name)

                    total = 0
                    with open(file_name, 'wb') as file:
                        while str(total) != lenOfFile:
                            data = self.server.recv(1024)
                            total = total + len(data)
                            file.write(data)

                    self.textCons.config(state=tk.DISABLED)
                    self.textCons.config(state=tk.NORMAL)
                    self.textCons.insert(
                        tk.END,str(send_user) + " send a file!\n\n")
                    self.textCons.config(state=tk.DISABLED)
                    self.textCons.see(tk.END)

                else:                                               #jika pesan selain 'FILE'
                    if(checkTag(message)):                          #jika status checkTag bernilai TRUE maka tampilkan hasil tag untuk user
                        self.textTag.config(state=tk.DISABLED)
                        self.textTag.config(state=tk.NORMAL)
                        self.textTag.insert(tk.END,
                                            message+"\n\n")
                        self.textTag.config(state=tk.DISABLED)

                        self.textCons.config(state=tk.DISABLED)
                        self.textCons.config(state=tk.NORMAL)
                        self.textCons.insert(tk.END,
                                            "dari "+parseSender(message)+"\n(*)"+message+"\n\n")

                        self.textCons.config(state=tk.DISABLED)
                        self.textCons.see(tk.END)
                    else:                                           #jika status FALSE maka tampilkan pesan
                        self.textCons.config(state=tk.DISABLED)
                        self.textCons.config(state=tk.NORMAL)
                        self.textCons.insert(tk.END,
                                            message+"\n\n")

                        self.textCons.config(state=tk.DISABLED)
                        self.textCons.see(tk.END)

            except:
                print("An error occured!")
                self.server.close()
                break

    def sendMessage(self):
        '''
        Mengirim pesan ke server
        '''
        self.textCons.config(state=tk.DISABLED)
        while True:
            if self.msg == "exit":                              #jika pesan ber-isi 'exit' maka tutup client/user
                self.server.close()
                self.Window.destroy()
            self.server.send(self.msg.encode())
            self.textCons.config(state=tk.NORMAL)
            self.textCons.insert(tk.END,
                                 "You : " + self.msg + "\n\n")

            self.textCons.config(state=tk.DISABLED)
            self.textCons.see(tk.END)
            break


if __name__ == "__main__":
    '''
    Membuat client dengan ip '127.0.0.1' dan port '12345'
    '''
    ip_address = "127.0.0.1"
    port = 12345
    g = GUI(ip_address, port)
