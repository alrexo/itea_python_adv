import socket
import threading
from datetime import datetime


class ThreadedServer:
    def __init__(self, port, host='', buffer_size=1024, max_threads=5):
        self.port = port
        self.host = host
        self.buffer_size = buffer_size
        self.max_threads = max_threads
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket successfully created.')
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        print('Socket bound to port {}.'.format(self.port))

    def listen(self):
        self.sock.listen(self.max_threads)
        print('Socket is listening. {} connections max.'.format(self.max_threads))
        while True:
            client, address = self.sock.accept()
            print('Got connection from {}.'.format(address))
            threading.Thread(target=self.listen_to_client, args=(client, address)).start()

    def listen_to_client(self, client, address):
        while True:
            received_data = str(client.recv(self.buffer_size).decode('utf8'))
            output = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') + ', ' + str(address) + ': ' + received_data + '\n'
            if not received_data:
                break
            print(output)
            with open('data.txt', 'a+') as f:
                f.write(output)
        client.close()


if __name__ == '__main__':
    while True:
        port = input('Please enter port number: ')
        try:
            port = int(port)
            break
        except ValueError:
            pass

    ThreadedServer(port).listen()
