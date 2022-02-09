import socket
import getpass
import zipfile
import os
import shutil

username = getpass.getuser()

HOST = ''
PORT = 3653

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))
server_socket.listen()

client_socket, addr = server_socket.accept()
print('connected by {}'.format(addr))

while True:
    try:
        while True:
            data = client_socket.recv(1024)

            divided = data.decode().split('/')
            location = divided[3]
            data_transferred = 0
            info = client_socket.recv(1024)
            with open('C:\\Users\\{}\\Desktop\\server_folder\\'.format(username) + location,
                      'wb') as f:
                try:
                    while info:
                        f.write(info)
                        data_transferred += len(info)
                        info = client_socket.recv(1024)
                except Exception as ex:
                    print(ex)
            f.close()
            client_socket.close()
            client_socket, addr = server_socket.accept()
            with zipfile.ZipFile('C:\\Users\\{}\\Desktop\\server_folder\\zips\\torecv.zip'.format(username), 'r') as zip_ref:
                zip_ref.extractall('C:\\Users\\{}\\Desktop\\extraction_folder'.format(username))
            os.remove('C:\\Users\\{}\\Desktop\\server_folder\\zips\\torecv.zip'.format(username))
            whatsin = os.listdir('C:\\Users\\{}\\Desktop\\extraction_folder'.format(username))
            for i in whatsin:
                whatsin2 = os.listdir('C:\\Users\\{}\\Desktop\\extraction_folder\\{}'.format(username, i))
                for a in whatsin2:
                    shutil.move('C:\\Users\\{}\\Desktop\\extraction_folder\\{}\\{}'.format(username, i, a), 'C:\\Users\\{}\\Desktop\\saving_dataset\\{}\\{}'.format(username, i, a))
            shutil.rmtree('C:\\Users\\{}\\Desktop\\extraction_folder\\target'.format(username))
            shutil.rmtree('C:\\Users\\{}\\Desktop\\extraction_folder\\not_target'.format(username))
    except Exception as e:
        print(e)
        client_socket, addr = server_socket.accept()
        print('connected by {}'.format(addr))