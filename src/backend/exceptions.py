class DisconnectionException(Exception):
    def __str__(self):
        return "connection has been closed."


class ReconnectSuccessException(Exception):
    pass


class ConnectionCloseException(Exception):
    def __str__(self):
        return "main thread has been closed."
