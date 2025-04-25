import sys
import socket
import re
from threading import Event, Thread
import netifaces as ni
import redis
import broadcast
import server

# Connect to Redis
R = redis.StrictRedis()
try:
    R.ping()
except:
    print("REDIS: Not Running -- No Streams Available")
    R = None

R.lpush("connections", "temp")
R.lpop("connections")

# Check first if the argument exists, if not, offer a helpful error message
if len(sys.argv) < 2:
    print("Usage: python server.py <integer> [-b]")
    sys.exit(1)

# Grab the number and validate it
number = sys.argv[1]
if not number.isdigit():
    print("Please provide a valid positive integer.")
    sys.exit(1)

MY_IP = ni.ifaddresses('en0')[ni.AF_INET][0]['addr']

if len(sys.argv) > 2:
    flags = sys.argv[2:]
    for f in flags:
        if f == "-b":
            # This thread can just be terminated, so I added daemon=True
            Thread(target=broadcast.broadcast_thread, args=(MY_IP, number, ), daemon=True)

# Compile the pattern here to validate the IPv4 address
ipv4_pat = re.compile(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$")

# This is a list of threads that must be joined
stop_event = Event()
threads = []
server_thread = Thread(target=server.run, args=(stop_event,))
server_thread.start()
threads.append(server_thread)

print(f"Connect on LAN IP: {MY_IP}")
print("Server started. Type 'exit' to stop.")
while True:
    user_input = input("> ")
    if user_input.lower() == 'exit':
        stop_event.set()
        for t in threads:
            t.join()
        break

    # Check if the full string conforms to the regex pattern
    # If it does, then we know its a valid IPv4 address
    if re.fullmatch(ipv4_pat, user_input):
        print(f"Sending message to valid IPv4 address: {user_input}")
        msg = f"Hello from {MY_IP}, my number is {number}"
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((user_input, 8082)) 
            
            # Send the message to the server
            client_socket.send(bytes(msg, 'utf-8'))
            print(f"Sent to {user_input}: {msg}")
        except Exception as err:
            print(f"Exception: {err}")
    else:
        print(f"Please enter a valid IPv4 address.")