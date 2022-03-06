
import socket

s = socket.socket()
host = socket.gethostname()
print(host)
port = 8000
s.bind((host, port))

s.listen(5)
while True:
   c, addr = s.accept()
   print('Got connection from', addr)
   print(c.recv(1024))
   c.send('Thank you for connecting'.encode('utf-8'))
   c.close()
