from abc import ABC, abstractmethod


class ServerSelectionStrategy(ABC):
    @abstractmethod
    def get_server_address(self, server):
        pass
