import socket
from time import sleep

def broadcast_thread(MY_IP, number):
    while True:    
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        msg = f"Hello from {MY_IP}, my number is {number}"

        # Broadcast address is 255.255.255.255
        sock.sendto(bytes(msg, 'utf-8'), ("255.255.255.255", 8082))
        sock.close()

        sleep(5)