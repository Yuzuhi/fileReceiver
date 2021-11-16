class DisconnectionException(Exception):
    def __str__(self):
        print("connection has been closed.")


class ReconnectSuccessException(Exception):
    pass
