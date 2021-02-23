import urllib3
import socket

HOST = '192.168.0.178'  # The server's hostname or IP address
PORT = 8889      # The port used by the server
link = '192.168.0.178:8889'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)

print('Received', repr(data))

