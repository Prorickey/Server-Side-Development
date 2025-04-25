import re
import socket
from threading import Thread

def run_udp(R, stop_event):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serversocket.bind(('0.0.0.0', 8082))

    # Set the timeout so we can check the stop event
    serversocket.settimeout(1.0)

    while not stop_event.is_set(): 
        try:
            # Receive data and address from client
            data, addr = serversocket.recvfrom(1024) 

            # Check if the address is in the redis database
            # if not, we can add it
            try:
                R.lrange("connections", 0, -1).index(addr[0].encode()) 
            except ValueError:
                R.lpush("connections", addr[0])
            
            # This regex helps extract the number from the format
            # I am expecting
            match = re.search(r'my number is (\d+)', data.decode("utf-8"))
            if match:
                number = int(match.group(1))
                print(f"UDP RECVD: {addr[0]} {number}")
        except socket.timeout:
            continue  

def run_tcp(R, stop_event):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    serversocket.bind(('0.0.0.0', 8082)) 
    serversocket.listen(10)

    # Set the timeout so we can check the stop event
    serversocket.settimeout(1.0)

    def handle(conn, addr):
        try:
            R.lrange("connections", 0, -1).index(addr[0].encode()) 
        except ValueError:
            R.lpush("connections", addr[0])

        try:
            while True:
                buf = conn.recv(64)
                match = re.search(r'my number is (\d+)', buf.decode("utf-8"))
                if match:
                    number = int(match.group(1))
                    print(f"TCP RECVD: {addr[0]} {number}")
        finally:
            conn.close()
            R.lrem("connections", 1, addr[0])

    try:
        while not stop_event.is_set(): 
            try:
                connection, address = serversocket.accept() 
                print(f"Accepted connection from {address[0]}")

                # Handle the connection on a seperate thread because it's blocking
                # daemon=True because it doesn't say that I need to handle these
                # threads gracefully
                Thread(target=handle, args=(connection, address), daemon=True).start()
            except socket.timeout:
                continue  
    finally:
        print("Shutting down server...")
        serversocket.close()