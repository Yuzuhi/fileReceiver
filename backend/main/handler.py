import json
import os
import socket
import struct
import sys
from typing import Optional, List

from backend.main.conn import connect_server
from backend.main.constant import FAIL_CODE, SUCCESS_CODE
from backend.main.utils import to_bytes


class SessionHandler:
    get_dirs_command = 0
    get_videos_command = 1
    single_download_command = 2
    multi_download_command = 3

    def __init__(self, server_ip: str, server_port: int):
        # self.ip = self.get_hostname()
        self.session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.session.connect((server_ip, server_port))

    @staticmethod
    def get_hostname():
        hostname = socket.gethostname()
        sys_info = socket.gethostbyname_ex(hostname)
        return sys_info[2]

    def get_videos(self, video_dirs: List[str]) -> Optional[dict]:
        """
        发送获取文件列表的请求
        :return:
        """

        body_info = to_bytes(
            command="getVideos",
            code=self.get_videos_command,
            dirNumber=len(video_dirs),
            dirName=video_dirs
        )

        head_info = to_bytes(
            command="getVideos",
            code=self.get_videos_command,
            msgSize=sys.getsizeof(body_info)
        )

        self._send_head_info(head_info)
        self.session.send(body_info)

        videos = self.receive_response()

        if not videos or videos["code"] == FAIL_CODE:
            raise socket.error

        return videos

    def get_dirs(self) -> List[str]:

        body_info = to_bytes(command="getDirs",
                             code=self.get_dirs_command)

        head_info = to_bytes(
            command="getDirs",
            code=self.get_dirs_command,
            msgSize=sys.getsizeof(body_info)
        )

        self._send_head_info(head_info)
        self.session.send(body_info)

        dirs = self.receive_response()
        if not dirs or dirs["code"] == FAIL_CODE:
            raise socket.error

        return dirs["dirs"].keys()

    def download_request(self):
        pass

    def _single_download(self, video_path: str, video_name: str):

        body_info = to_bytes(videoPath=video_path, videoName=video_name)
        head_info = to_bytes(
            command="singleDownload",
            code=self.single_download_command,
            msgSize=sys.getsizeof(body_info)
        )

        self._send_head_info(head_info)
        self.session.send(body_info)

        video_info = self.receive_response()
        if not video_info:
            return

        self.write(video_info["name"], video_info["size"])

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

    def _send_head_info(self, head_info: bytes):

        head_info_len = struct.pack("i", len(head_info))
        self.session.send(head_info_len)
        self.session.send(head_info)

    def receive_response(self) -> Optional[dict]:
        response = self.session.recv(4)
        header_len = struct.unpack('i', response)[0]
        header_info = self.session.recv(header_len)
        header_info = json.loads(header_info.decode('utf-8'))

        if header_info:
            response_body = self.session.recv(header_info["msgSize"])
            response_body = json.loads(response_body.decode("utf-8"))

            if response_body["code"] == SUCCESS_CODE:
                return response_body
