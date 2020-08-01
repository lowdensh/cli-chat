import socket
import threading
from datetime import datetime as dt


def timestamp():
    return f'[{dt.now().strftime("%H:%M")}]'


nickname = input(f' {timestamp()} ::SERVER:: Enter nickname: ')

host = '127.0.0.1'
port = 7976

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICKNAME':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            # wrong host or port
            print(f' {timestamp()} ::SERVER:: Host and/or port was incorrect.')
            client.close()
            break


def write():
    while True:
        message = f' {timestamp()} {nickname}: {input("")}'
        client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
