import socket
import threading
from datetime import datetime as dt


host = '127.0.0.1'
port = 7976

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def timestamp():
    return f'[{dt.now().strftime("%H:%M")}]'


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            # remove client
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            print(f' {timestamp()} ::SERVER:: {nickname} disconnected.')
            broadcast(f' {timestamp()} ::SERVER:: {nickname} disconnected from cli-chat.'.encode('ascii'))
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f' {timestamp()} ::SERVER:: {str(address)} new client connected.')

        client.send('NICKNAME'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        print(f' {timestamp()} ::SERVER:: {str(address)} set nickname to {nickname}.')
        client.send(f' {timestamp()} ::SERVER:: You are connected to cli-chat.'.encode('ascii'))
        broadcast(f' {timestamp()} ::SERVER:: {nickname} connected to cli-chat.'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()
