import socket
import fleet

class Packet(object):
    def __init__(self, packetType: str, data: str):
        self.type = packetType
        self.data = data

    def __str__(self):
        return self.type + ";" + self.data + ";"


class Connection(object):

    def __init__(self, open_as="client", port: int = 5778, address: str = socket.gethostname()):
        """Opens the communication either as a server or a client"""
        mode = open_as
        if mode == "client":
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((address, port))
        elif mode == "server":
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((address, port))
            server.listen()
            self.connection = server.accept()  # no while true and separate thread needed, this is a 1 to 1 connection
        else:
            raise ValueError("only 'server' and 'client' as arguments allowed. found: " + str(open_as))

    def send_guess(self, x: int, y: int) -> bool:
        pass

    def await_response(self) -> fleet.FieldState:
        pass

    def await_guess(self) -> tuple[int, int]:
        pass

    def send_response(self, response: fleet.FieldState) -> None:
        pass
