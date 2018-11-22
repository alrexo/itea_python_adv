import socket
from datetime import datetime

s = socket.socket()
print('Socket successfully created.')

port = 12345
s.bind(('', port))
print('Socket bound to port {}.'.format(port))

s.listen(5)
print('Socket is listening.')

while True:
    client, address = s.accept()
    print('Got connection from {}.'.format(address))

    size = 1024
    received_data = str(client.recv(size).decode('utf8'))
    output = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') + ', ' + str(address) + ': ' + received_data + '\n'
    print(output)

    with open('data.txt', 'a+') as f:
        f.write(output)

    client.close()
