import json
import socket
import struct
import sys

from backend.main.utils import to_bytes

tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_port = ("127.0.0.1", 8021)

tcp_server.connect(ip_port)

anime_path = "./haha"

body_info = to_bytes(dirPath=anime_path)
head_info = to_bytes(
    command="getFiles",
    code=0,
    msgSize=sys.getsizeof(body_info)
)

head_info_len = struct.pack("i", len(head_info))
print(len(head_info))

print(sys.getsizeof(head_info_len))

tcp_server.send(head_info_len)
tcp_server.send(head_info)

tcp_server.close()
