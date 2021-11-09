import socket


class connect_server:

    def __init__(self, ip: str, port: int):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((ip, port))

    def __enter__(self):
        return self.client_socket

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client_socket.close()


