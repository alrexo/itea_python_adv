import socket

s = socket.socket()
port = 12345
s.connect(('127.0.0.1', port))

string_to_send = input('Enter data to send: ')
s.send(string_to_send.encode())

s.close()
