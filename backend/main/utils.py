import socket
import json


def get_host_ip():
    extra_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    extra_conn.connect(('8.8.8.8', 80))
    ip = extra_conn.getsockname()[0]
    extra_conn.close()

    return ip


def to_bytes(**kwargs) -> bytes:
    if kwargs:
        return json.dumps(kwargs).encode("utf-8")


if __name__ == '__main__':
    a = to_bytes(haha="hehe", hehe="pupu")
    print(a)
