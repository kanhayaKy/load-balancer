from .base import ServerSelectionStrategy


class RoundRobinStrategy(ServerSelectionStrategy):
    def get_server_address(self, server):
        try:
            selected_server = server.be_servers[server.current]
        except IndexError:
            raise NoValidServerURLError("Valid server URL not found")

        # Update the current server index in a thread-safe manner
        with server.lock:
            server.current = (server.current + 1) % len(server.be_servers)

        return selected_server
