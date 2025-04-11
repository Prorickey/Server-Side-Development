import socket
from threading import Thread

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
serversocket.bind(('0.0.0.0', 8089)) 
serversocket.listen(5)

def handle(conn, addr):
    while True:
        buf = conn.recv(64)
        print(f"Got [{addr}]: {buf}") 

running = True
while running: 
    connection, address = serversocket.accept() 
    
    Thread(target=handle, args=(connection, address)).start()

serversocket.close()