import socket
from _thread import *
from collections import defaultdict as df
import time


class Server:
    def __init__(self):
        '''
        Inisiasi pembuatan server
        '''
        self.rooms = df(list)
        #self.rooms = ['100', '101', '102']
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         #untuk membuat objek socket baru
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)       #mengatur konfigurasi dari socket

    def accept_connections(self, ip_address, port):
        '''
        Menerima koneksi baru
        '''
        self.ip_address = ip_address                            #meng-set nilai IP
        self.port = port                                        #meng-set nilai port
        self.server.bind((self.ip_address, int(self.port)))     #menggabungkan ip dan socket
        self.server.listen(100)                                 #membuat socket dalam posisi mendengarkan posisi yg ingin terhubung

        while True:
            connection, address = self.server.accept()          #menerima informasi dari koneksi yang terkait
            print(str(address[0]) + ":" + str(address[1]) + " Connected")

            start_new_thread(self.clientThread, (connection,))  #membuat thread untuk melakukan fungsi/ proses client thread

        self.server.close()

    def clientThread(self, connection):
        '''
        Fungsi untuk mendefinisikan client
        '''
        user_id = connection.recv(1024).decode().replace("User ", "")           #menyimpan nama user
        room_id = connection.recv(1024).decode().replace("Join ", "")           #menyimpan nomor room

        if room_id not in self.rooms:                                           #mengecek nomor room pada list room yang ada, jika tidak ditemukan akan dibuat room baru
            connection.send("Obrolan Baru Terbentuk".encode())
        else:
            connection.send("Anda Telah Bergabung Dengan Obrolan".encode())

        message_broad = str(user_id) + " telah bergabung dalam obrolan"
        self.broadcast(message_broad, connection, room_id)                      #mengembalikan pesan user berhasil terhubung

        self.rooms[room_id].append(connection)                                  #menyimpan informasi client terhubung pada room tersebut

        while True:                                                             #mengecek selama ada koneksi
            try:
                message = connection.recv(1024)
                print(str(message.decode()))
                if message:                                                     #mengecek jika pesan ditemukan
                    if str(message.decode()) == "FILE":                         #mengecek jika yang dikirimkan adalah file, maka broadcast file
                        self.broadcastFile(connection, room_id, user_id)
                    else:                                                       #mengecek jika yang dikirimkan selain file (pesan)
                        message_to_send = "" + \
                            str(user_id) + " : " + message.decode()
                        self.broadcast(message_to_send, connection, room_id)

                else:                                                           #mengecek jika pesan tidak ditemukan
                    self.remove(connection, room_id)
            except Exception as e:
                print(repr(e))
                print("Client Terputus")
                break

    def broadcastFile(self, connection, room_id, user_id):
        '''
        Mengirimkan notifikasi beserta file ketika ditemukan pesan 'FILE'
        '''
        file_name = connection.recv(1024).decode()      #menyimpan nama file
        lenOfFile = connection.recv(1024).decode()      #menyimpan detail file
        for client in self.rooms[room_id]:              #selama ada client dalam room
            if client != connection:                    #jika client tidak sama dengan dirinya sendiri (untuk menghindari duplikasi file)
                try:
                    client.send("FILE".encode())        #mengirimkan file dengan nama 'FILE' keseluruh user
                    time.sleep(0.1)
                    client.send(file_name.encode())
                    time.sleep(0.1)
                    client.send(lenOfFile.encode())
                    time.sleep(0.1)
                    client.send(user_id.encode())
                except:
                    client.close()
                    self.remove(client, room_id)

        total = 0
        print(file_name, lenOfFile)                     #menampilkan nama file dan ukuran file pada server
        while str(total) != lenOfFile:                  #mengirimkan notifikasi selama panjang/ ukuran file tidak 0
            data = connection.recv(1024)
            total = total + len(data)
            for client in self.rooms[room_id]:
                if client != connection:                #jika client tidak sama dengan dirinya sendiri (untuk menghindari duplikasi file)
                    try:
                        client.send(data)
                        # time.sleep(0.1)
                    except:
                        client.close()
                        self.remove(client, room_id)
        print("Sent")

    def broadcast(self, message_to_send, connection, room_id):
        '''
        Mengirimkan pesan teks
        '''
        for client in self.rooms[room_id]:
            if client != connection:                    #jika client tidak sama dengan dirinya sendiri (untuk menghindari duplikasi file)
                try:
                    client.send(message_to_send.encode())
                except:
                    client.close()
                    self.remove(client, room_id)        #menghapus client pada room tertentu

    def remove(self, connection, room_id):
        '''
        Menghapus client pada room tertentu
        '''
        if connection in self.rooms[room_id]:
            self.rooms[room_id].remove(connection)


if __name__ == "__main__":
    '''
    Membuat server dengan ip '127.0.0.1' dan port '12345'
    '''
    ip_address = "127.0.0.1"
    port = 12345

    s = Server()
    s.accept_connections(ip_address, port)
