import socket
from threading import Event, Thread

def run(stop_event):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    serversocket.bind(('0.0.0.0', 8082)) 
    serversocket.listen(10)
    serversocket.settimeout(1.0)

    def handle(conn, addr):
        while True:
            buf = conn.recv(64)
            print(f"Got [{addr}]: {buf}") 

    try:
        while not stop_event.is_set(): 
            try:
                connection, address = serversocket.accept() 
                print(f"Accepted connection from {address}")
                Thread(target=handle, args=(connection, address)).start()
            except socket.timeout:
                continue  
    finally:
        print("Shutting down server...")
        serversocket.close()