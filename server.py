import socket
import os
import pickle
import time
import threading

HOST = ""
PORT = 9090

TYPE = socket.AF_INET
PROTOCOL = socket.SOCK_STREAM

folder = "f_main"
directory = os.path.join(os.getcwd(), folder)


def clientprocessing(sock, addr):
    try:
        packageLen = int(sock.recv(1024))

        print('получена длина', packageLen)
        bytesReceive = 0
        received_data = b''

        while bytesReceive < packageLen:
            chunk = sock.recv(min(packageLen - bytesReceive, 2048))
            bytesReceive = bytesReceive + len(chunk)
            received_data += chunk
            print('gcvb')


        #received_data = sock.recv(packageLen)
        print(f"Получено от {addr}")
        received_data = pickle.loads(received_data)
        msg = check_directory(directory, received_data)
        msg = pickle.dumps(msg)

        sock.send(pickle.dumps(len(msg)))
        sock.send(msg)
        print(f"Запрос отправлен клиенту {addr}")
    except Exception as e:
        print(f"Error processing client {addr}: {e}")
        sock.close()


def create_directories(folder):
    if not os.path.isdir(os.path.join(os.getcwd(), folder)):
        os.mkdir(os.path.join(os.getcwd(), folder))


def check_directory(directory, dir_client):
    dir_server = os.listdir(directory)
    for f in dir_client:
        if f not in dir_server:
            print("Отправлен запрос на remove")
            return f"remove {f}"

    for f in dir_server:
        if f not in dir_client:
            print("Отправлен запрос на create")
            return File(f, directory)
    print("Отправлен запрос на OK")
    return "OK"


class File:
    def __init__(self, name, directory):
        self.name = name
        self.directory = directory
        self.data = self.read_data()

    def read_data(self):
        with open(os.path.join(self.directory, self.name)) as f:
            return f.readlines()


srv = socket.socket(TYPE, PROTOCOL)
srv.bind((HOST, PORT))

create_directories(folder)
srv.listen(3)
while True:
    print("Слушаю порт 9090")
    sock, addr = srv.accept()
    print("Подключен клиент", addr)
    try:

        thread = threading.Thread(target=clientprocessing,
                                  args=(sock, addr))  # Создание нового потока для обработки клиента
        thread.start()  # Запускаем поток для обработки клиента


    except Exception as e:
        print("Error creating thread:", e)
