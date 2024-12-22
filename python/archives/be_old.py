import sys
import socket


# CONSTANTS
HOST = "localhost"
PORT = 7000

if len(sys.argv) > 1:
    PORT = int(sys.argv[1])


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        try:
            server_socket.bind((HOST, PORT))
            server_socket.listen(5)
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
            request = connection.recv(1024).decode("utf-8")

            if request:
                print(f"Received request from {connection.getpeername()}")
                print(request)

            response = "Hello From Backend Server"
            http_response = (
                f"HTTP/1.1 200 OK\r\nContent-Length: {len(response)}\r\n\r\n{response}"
            )

            connection.send(http_response.encode())
            print(f"Replied with {response!r} message")

        except Exception as e:
            print(f"Error handling connection: {e}")


if __name__ == "__main__":
    start_server()
