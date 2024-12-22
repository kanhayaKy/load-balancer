import sys

from socketserver import BaseRequestHandler, TCPServer
from socket import socket, AF_INET, SOCK_STREAM


class BackendServer(BaseRequestHandler):

    def __init__(self, *args, server_name, **kwargs):
        self.name = server_name
        super().__init__(*args, **kwargs)

    def handle(self):
        request = self.request.recv(8192)

        parsed_request = request.decode("utf-8")

        if not parsed_request:
            return

        print(f"Received request from {self.request.getpeername()}")
        print(parsed_request)

        response = f"Hello From Backend Server {self.name}\n"
        http_response = (
            f"HTTP/1.1 200 OK\r\nContent-Length: {len(response)}\r\n\r\n{response}"
        )

        self.request.send(http_response.encode())

        print(f"Replied with {response!r} message")


def create_server_handler(server_name):
    class CustomBackendServer(BackendServer):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, server_name=server_name, **kwargs)

    return CustomBackendServer


if __name__ == "__main__":

    PORT = 8000
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])

    server_name = f"server{PORT}"

    handler = create_server_handler(server_name)
    with TCPServer(("", PORT), handler) as serv:
        print(f"Server started on port {PORT}...")
        serv.serve_forever()
