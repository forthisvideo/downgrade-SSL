import ssl
import socket
import argparse
import time

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

# Establish a connection with the server
while True:
    try:
        print("Connecting to server...")
        ssl_sock.connect((args.hostname, args.port))
        print("Connected to server!")
        break
    except socket.error as err:
        print("Error:", err)
    except ssl.SSLError as err:
        print("Error:", err)
    except Exception as err:
        print("Error:", err)

    # Wait before retrying
    print("Retrying in 5 seconds...")
    time.sleep(5)

# Send a request to the server
request = (
    "GET / HTTP/1.1\r\n"
    "Host: {}\r\n"
    "Connection: close\r\n"
    "\r\n"
).format(args.hostname).encode()
ssl_sock.send(request)

# Receive the response
response = ssl_sock.recv(4096)
print("Response:", response.decode())

# Close the connection
ssl_sock.close()
