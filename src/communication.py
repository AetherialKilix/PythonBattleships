from __future__ import annotations

import socket
import utils
from enum import Enum

INSTANCE = None


class GuessResponse(Enum):
    MISS = 0
    HIT = 1
    SUNK = 2
    WIN = 3
    INVALID = 4

    @classmethod
    def from_string(cls, string: str):
        if string == "miss":
            return GuessResponse.MISS
        if string == "hit":
            return GuessResponse.HIT
        if string == "sunk":
            return GuessResponse.SUNK
        if string == "win":
            return GuessResponse.WIN
        if string == "invalid":
            return GuessResponse.INVALID

    def __str__(self) -> str:
        if self.value == 0:
            return "miss"
        if self.value == 1:
            return "hit"
        if self.value == 2:
            return "sunk"
        if self.value == 3:
            return "win"
        if self.value == 4:
            return "invalid"


def interpret_sunk_payload(payload: str):
    payload_arr = payload.split(",")
    return utils.get_cells_from_ends((payload_arr[0], payload_arr[1]), (payload_arr[2], payload_arr[3]))


class Connection(object):
    """Uses sockets to communicate with opponent. 'Packet'-format: 'type;data;' """

    def __init__(self, open_as="client", port: int = 5778, address: str = "127.0.0.1"):
        """Opens the communication either as a server or a client"""
        if not address:
            address = "127.0.0.1"
        mode = open_as
        if mode == "client":
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((address, port))
        elif mode == "server":
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((address, port))
            server.listen(1)
            self.connection, ignore = server.accept()  # no while true and separate thread needed, this is a 1 to 1 connection
        else:
            raise ValueError("only 'server' and 'client' as arguments allowed. found: " + str(open_as))

    def send_guess(self, x: int, y: int):
        self.connection.send(("guess;" + str(x) + "," + str(y) + ";").encode())

    def await_response(self) -> tuple[GuessResponse, list] | None:
        """this method blocks, until a FieldState was received (or an error occurred)"""
        data = self.connection.recv(512).decode()
        data = data.split(";")
        if len(data) != 3:  # [0] = type, [1] = payload, [2] = ""
            return None
        response = GuessResponse.from_string(data[0])
        payload = []
        if response == GuessResponse.SUNK:
            payload = interpret_sunk_payload(data[1])
        return response, payload

    def await_guess(self) -> tuple[int, int] | None:
        """this method blocks, until a guess was received (or an error occurred)"""
        data = self.connection.recv(512).decode()
        data = data.split(";")
        if len(data) != 3:  # [0] = type, [1] = payload, [2] = ""
            return None
        if not data[0] == "guess":
            return None
        position_strings = data[1].split(",")

        return int(position_strings[0]), int(position_strings[1])

    def send_response(self, response: GuessResponse, sunk_fields: str = ""):
        if response == GuessResponse.SUNK:
            self.connection.send((str(response) + ";" + sunk_fields + ";").encode())
        else:
            self.connection.send((str(response) + ";;").encode())

    def close(self):
        self.connection.close()

    def await_done(self):
        """this method blocks, until a "done" was received (or an error occurred)"""
        data = self.connection.recv(512).decode()
        data = data.split(";")
        if len(data) != 3:  # [0] = type, [1] = payload, [2] = ""
            return None
        if not data[0] == "done":
            return None

    def send_done(self):
        self.connection.send("done;;".encode())

    def await_both_done(self):
        self.send_done()
        self.await_done()
