import sys
import socket
import re

# Check first if the argument exists, if not, offer a helpful error message
if len(sys.argv) != 2:
    print("Usage: python server.py <integer>")
    sys.exit(1)

# Grab the number and validate it
number = sys.argv[1]
if not number.isdigit():
    print("Please provide a valid positive integer.")
    sys.exit(1)

MY_IP = "192.168.1.1"

# Compile the pattern here to validate the IPv4 address
ipv4_pat = re.compile(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$")

print("Server started. Type 'exit' to stop.")
while True:
    user_input = input("> ")
    if user_input.lower() == 'exit':
        break

    # Check if the full string conforms to the regex pattern
    # If it does, then we know its a valid IPv4 address
    if re.fullmatch(ipv4_pat, user_input):
        print(f"Valid IPv4 address: {user_input}")

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((user_input, 8082)) 
        
        # Send the message to the server
        msg = f"Hello from {MY_IP}, my number is {number}"
        client_socket.send(bytes(msg, 'utf-8'))
    else:
        print(f"Please enter a valid IPv4 address.")