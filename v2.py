import ssl
import socket
import argparse
import time
import warnings

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("hostname", help="The hostname of the server to connect to")
parser.add_argument("port", type=int, help="The port number of the server to connect to")
args = parser.parse_args()

# Create a client-side SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

# Set the minimum and maximum version of SSL/TLS to use
context.minimum_version = ssl.TLSVersion.TLSv1
context.maximum_version = ssl.TLSVersion.TLSv1

# Use the SSL context when creating a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_sock = context.wrap_socket(sock, server_hostname=args.hostname)

# Establish the initial connection
s = ssl.wrap_socket(socket.socket())
print("Connecting to server...")
s.connect((args.hostname, args.port))
time.sleep(1)  # Delay for 1 second
print("Connected!")

# Send a request and receive the response
print("Sending request...")
s.send = b"GET /manage/account/login?redirect=%2Fmanage/ HTTP/1.1\r\nHost: " + args.hostname.encode() + b"\r\nUser-Agent: MyClient/1.0\r\nAccept: text/html\r\nConnection: close\r\n\r\n"
time.sleep(1)  # Delay for 1 second
print("Request sent!")


print("Receiving response...")
response = s.recv(4096)  # Receive up to 4096 bytes of data
print(response)  # Print the response
