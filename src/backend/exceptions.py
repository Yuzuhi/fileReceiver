class DisconnectionException(Exception):
    def __str__(self):
        return "connection has been closed."


class ReconnectSuccessException(Exception):
    pass


