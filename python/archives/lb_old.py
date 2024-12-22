import sys
from socket import socket, AF_INET, SOCK_STREAM

# CONSTANTS
HOST = "localhost"
PORT = 5001

if len(sys.argv) > 1:
    PORT = int(sys.argv[1])


def start_server(address, backlog=5):
    with socket(AF_INET, SOCK_STREAM) as server_socket:
        try:
            server_socket.bind(address)
            server_socket.listen(backlog)
            print(f"Server listening on port {PORT}...")

            while True:
                connection, address = server_socket.accept()
                handle_connection(connection, address)
        except Exception as e:
            print(f"Error handling connection: {e}")
        finally:
            server_socket.close()


def handle_connection(connection, address):
    with connection:
        # print(f"Connected by {address}...")
        try:
            request = connection.recv(1024)
            parsed_request = request.decode("utf-8")

            if not parsed_request:
                return

            print(f"Received request from {connection.getpeername()}")
            print(parsed_request)

            be_socket = socket(AF_INET, SOCK_STREAM)
            be_socket.connect(("localhost", 7000))
            be_socket.send(request)

            http_response = be_socket.recv(8192)
            parsed_response = http_response.decode("utf-8")
            print(f"Received response from server")
            print(parsed_response)

            connection.send(http_response)

        except Exception as e:
            print(f"Error handling connection: {e}")


if __name__ == "__main__":
    start_server(
        address=(HOST, PORT),
    )
