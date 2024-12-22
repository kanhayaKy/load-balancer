from socketserver import BaseRequestHandler, TCPServer
from socket import socket, AF_INET, SOCK_STREAM

from threading import Thread, Lock, Timer, Event

from strategy import RoundRobinStrategy
from health import start_health_check

from constants import NoValidServerURLError
from config import SELECTION_STRATEGY


class LoadBalancerHandler(BaseRequestHandler):

    def handle(self):
        request = self.request.recv(8192)

        parsed_request = request.decode("utf-8")

        if not parsed_request:
            return

        print(f"Received request from {self.request.getpeername()}")
        print(parsed_request)

        try:
            server_address = self.get_server_address()
        except NoValidServerURLError as e:
            print(f"Error: {e}")
            response = "No valid server URL found"
            http_response = (
                f"HTTP/1.1 503 Service Unavailable\r\n"
                f"Content-Length: {len(response)}\r\n"
                f"Content-Type: text/plain\r\n\r\n"
                f"{response}"
            )
            self.request.send(http_response.encode())
            return

        server_response = self.forward_request(request, server_address)

        parsed_response = server_response.decode("utf-8")
        print(f"Received response from server")
        print(parsed_response)

        self.request.send(server_response)

    def get_server_address(self):
        return self.server.strategy.get_server_address(self.server)

    def forward_request(self, request, address):
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.connect(address)
        server_socket.send(request)

        server_response = server_socket.recv(8192)
        return server_response


def start_loadbalancer_workers(n_workers=2):
    with TCPServer(("", 5001), LoadBalancerHandler) as serv:
        serv.strategy = SELECTION_STRATEGY()

        serv.be_servers = []
        serv.current = 0
        serv.lock = Lock()

        start_health_check(serv)

        for n in range(n_workers):
            t = Thread(target=serv.serve_forever)
            t.daemon = True
            t.start()

        print("Server started on port 5001...")
        serv.serve_forever()


if __name__ == "__main__":
    start_loadbalancer_workers()
