from socket import socket, AF_INET, SOCK_STREAM, gethostbyname, gethostname
from threading import Thread

running = True

def handle(conn, addr):
    while True:
        buf = conn.recv(64)
        print(f"Got [{addr}]: {buf}") 

def server_socket():
    serversocket = socket(AF_INET, SOCK_STREAM) 
    serversocket.bind(('0.0.0.0', 8089)) 
    serversocket.listen(5)

    while running: 
        connection, address = serversocket.accept() 
        
        Thread(target=handle, args=(connection, address)).start()

    serversocket.close()

server_thread = Thread(target=server_socket)
server_thread.start()

print("Server started. Type 'exit' to stop.")

while True:
    user_input = input("> ")
    if user_input.lower() == 'exit':
        running = False
        break

server_thread.join()