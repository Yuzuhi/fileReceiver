import json
import os
import socket
import struct
import sys
from json import JSONEncoder
from typing import Optional

from backend.main.conn import connect_server
from backend.main.utils import to_bytes


class SessionHandler:
    get_dirs_command = 0
    get_files_command = 1
    single_download_command = 2
    multi_download_command = 3

    def __init__(self, server_ip: str, server_port: int, anime_base_path: str, save_path: str):
        self.anime_base_path = anime_base_path
        self.save_path = save_path
        self.ip = self.get_hostname()
        self.session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.session.bind((self.ip, 8021))
        self.session.connect((server_ip, server_port))
        self.animes = self.get_dirs()
        self.all_anime = list()
        for anime in self.animes:
            self.all_anime.append(self.get_files(anime))

    @staticmethod
    def get_hostname():
        hostname = socket.gethostname()
        sys_info = socket.gethostbyname_ex(hostname)
        return sys_info[2]

    def get_files(self, anime_path: str) -> Optional[dict]:
        """
        发送获取文件列表的请求
        :return:
        """

        body_info = to_bytes(dirPath=anime_path)
        head_info = to_bytes(
            command="getFiles",
            code=self.get_files_command,
            msgSize=sys.getsizeof(body_info)
        )

        self._send_head_info(head_info)
        self.session.send(body_info)

        animes = self.receive_response(self.get_files_command)

        if not animes:
            return

        return animes["files"]

    def get_dirs(self) -> Optional[dict]:

        body_info = to_bytes(basePath=self.anime_base_path)
        head_info = to_bytes(
            command="getDirs",
            code=self.get_dirs_command,
            msgSize=sys.getsizeof(body_info)
        )

        self._send_head_info(head_info)
        self.session.send(body_info)

        dirs = self.receive_response(self.get_dirs_command)
        if not dirs:
            return
        return dirs["dirs"]

    def single_download(self, anime_path: str, anime_name: str):

        body_info = to_bytes(animePath=anime_path, animeName=anime_name)
        head_info = to_bytes(
            command="singleDownload",
            code=self.single_download_command,
            msgSize=sys.getsizeof(body_info)
        )

        self._send_head_info(head_info)
        self.session.send(body_info)

        anime_info = self.receive_response(self.single_download_command)
        if not anime_info:
            return

        self.write(anime_info["name"], anime_info["size"])

    def multi_download(self, animes: tuple):

        for _, v in animes.items():
            self.single_download()

    def write(self, name: str, size: int):
        save_path = os.path.join(self.save_path, name)
        with open(save_path, "wb") as f:
            while size > 1024:
                block = self.session.recv(1024)
                # 接收到数据
                if block:
                    f.write(block)
                    size -= 1024
                else:
                    block = self.session.recv(size)
                    if block:
                        f.write(block)

    def test(self):
        with connect_server(self.ip, self.port) as socket:
            data = socket.recv(4)
            print(data)
            head_len = struct.unpack('i', data)[0]
            data = socket.recv(head_len)
            print(head_len)
            head_info = json.loads(data.decode('utf-8'))
            print("head_info:", head_info)

    def _send_head_info(self, head_info: bytes):

        head_info_len = struct.pack("i", len(head_info))
        self.session.send(head_info_len)
        self.session.send(head_info)

    def receive_response(self, command: int) -> Optional[dict]:
        response = self.session.recv(4)
        head_len = struct.unpack('i', response)[0]
        response = self.session.recv(head_len)
        head_info = json.loads(response.decode('utf-8'))
        if head_info["code"] == command:
            body_data = self.session.recv(head_info)
            return json.loads(body_data.decode("utf-8"))
