import socket 
import time

CONNECT_IP='192.168.161.15'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((CONNECT_IP, 8089)) 

running = True
while running: 
   client_socket.send(b"Message")
   time.sleep(1)

client_socket.close()