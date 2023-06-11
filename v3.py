import ssl
import socket
import time
import logging
import argparse

# Setting up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("hostname", help="The hostname of the server to connect to")
parser.add_argument("port", type=int, help="The port number of the server to connect to")
args = parser.parse_args()

# Create a client-side SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

# Use the SSL context when creating a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_sock = context.wrap_socket(sock, server_hostname=args.hostname)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE


# Establish the initial connection
logging.info("Connecting to server...")
try:
    ssl_sock.connect((args.hostname, args.port))
    time.sleep(1)  # Delay for 1 second
    logging.info("Connected!")
except Exception as e:
    logging.error(f"Error connecting to server: {str(e)}")
    exit(1)

# Continuously capture traffic
while True:
    # Send a request
    logging.info("Sending request...")
    try:
        request = b"GET /manage/account/login?redirect=%2Fmanage/ HTTP/1.1\r\nHost: " + args.hostname.encode() + b"\r\nUser-Agent: MyClient/1.0\r\nAccept: text/html\r\nConnection: close\r\n\r\n"
        ssl_sock.sendall(request)
        time.sleep(1)  # Delay for 1 second
        logging.info("Request sent!")
    except Exception as e:
        logging.error(f"Error sending request: {str(e)}")
        ssl_sock.close()
        exit(1)

    # Receive and print the response
    logging.info("Receiving response...")
    try:
        while True:
            response = ssl_sock.recv(4096)  # Receive up to 4096 bytes of data
            if not response:
                # If response is empty, the connection is closed
                break
            logging.info(response)  # Print the response
    except Exception as e:
        logging.error(f"Error receiving response: {str(e)}")
        ssl_sock.close()
        exit(1)

ssl_sock.close()
