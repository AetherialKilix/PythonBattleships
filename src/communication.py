import socket

sock = None
server = None
mode = "client"


def open(open_as="client", port: int=5778, address: str="localhost"):
    """Opens the communication either as a server or a client"""
    global mode, sock, server
    mode = open_as
    if mode == "client":
        # sock = socket.socket
        pass
    elif mode == "server":
        pass
    else:
        raise ValueError("only 'server' and 'client' as arguments allowed. found: " + str(open_as))

