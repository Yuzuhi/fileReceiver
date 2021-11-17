import json
import os
import socket
import struct
import sys
import time
from tkinter.ttk import Progressbar
from typing import Optional, List

from src.backend.constant import FAIL_CODE, SUCCESS_CODE
from src.backend.exceptions import DisconnectionException
from src.backend.utils.utils import to_bytes


def reconnect(func):
    """自动重连模块"""

    def wrapper(self, *args, **kwargs):
        """
        :param self: SessionHandler
        :param args:
        :param kwargs:
        :return:
        """

        try:
            return func(self, *args, **kwargs)
        except socket.error as e:
            if not self.auto_reconnect:
                raise e
            else:
                self._reconnect()
                return func(self, *args, **kwargs)

    return wrapper


class SessionHandler:
    get_dirs_command = 0
    get_videos_command = 1
    download_command = 2

    def __init__(self, server_ip: str, server_port: int, auto_reconnect: bool = True):
        self.server_ip = server_ip
        self.server_port = server_port
        self.auto_reconnect = auto_reconnect

        try:
            self.session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.session.connect((self.server_ip, self.server_port))
        except socket.error as e:
            if self.auto_reconnect:
                self._reconnect()
            else:
                raise e

    def _reconnect(self) -> bool:
        server = '{} {}'.format(self.server_ip, self.server_port)
        while True:
            try:
                self.session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.session = self.session.connect((self.server_ip, self.server_port))
                # 睡眠以防止持续请求
                time.sleep(2.0)
            except ConnectionRefusedError:
                print('Connection to server {} failed!'.format(server))
            except TimeoutError:
                print('Connection to server {} timed out!'.format(server))
            except DisconnectionException:
                print(DisconnectionException())
            except socket.error as e:
                print('Connection to server {} failed! deal to {}'.format(server, e))
            else:
                return True

    @reconnect
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

        self._send_header_info(head_info)
        self.session.send(body_info)

        videos = self._receive_response()

        if not videos or videos["code"] == FAIL_CODE:
            raise socket.error

        return videos

    @reconnect
    def get_dirs(self) -> List[str]:

        body_info = to_bytes(command="getDirs",
                             code=self.get_dirs_command)

        head_info = to_bytes(
            command="getDirs",
            code=self.get_dirs_command,
            msgSize=sys.getsizeof(body_info)
        )

        self._send_header_info(head_info)
        self.session.send(body_info)

        dirs = self._receive_response()
        if not dirs or dirs["code"] == FAIL_CODE:
            raise socket.error

        return list(dirs["dirs"].keys())

    @reconnect
    def start_download(self, video_path: str, video_name: str, save_path: str, progress_bar: Progressbar):

        download_path = os.path.join(save_path, video_name)

        if os.path.exists(download_path):
            # 读取
            received = os.stat(download_path).st_size
        else:
            received = 0

        body_info = to_bytes(
            command="download",
            code=self.download_command,
            videoDir=video_path,
            videoName=video_name,
            received=received
        )

        header_info = to_bytes(
            command="download",
            code=self.download_command,
            msgSize=sys.getsizeof(body_info)
        )

        self._send_header_info(header_info)
        self.session.send(body_info)

        video_info = self._receive_header_info()
        self._write(download_path, video_info["videoSize"], progress_bar, received)

    def _send_header_info(self, header_info: bytes):

        header_info_len = struct.pack("i", len(header_info))
        self.session.send(header_info_len)
        self.session.send(header_info)

    def _receive_response(self) -> Optional[dict]:
        """
        接受服务器端发来的响应
        :return:
        """

        header_info = self._receive_header_info()
        # 本次请求的response_body会比较长，有可能会出错,因此使用while循环保证接收完整
        received = 0
        size = header_info["msgSize"]
        response_body = b""

        while received < size:
            response_body += self.session.recv(size - received)
            received += len(response_body)

        if not response_body:
            raise DisconnectionException

        response_body = json.loads(response_body.decode("utf-8"))

        if response_body["code"] == SUCCESS_CODE:
            return response_body

    def _receive_header_info(self) -> dict:
        """接收server发来的头部信息"""
        response = self.session.recv(4)
        if not response:
            raise DisconnectionException

        header_len = struct.unpack('i', response)[0]
        header_info = self.session.recv(header_len)
        if not header_info:
            raise DisconnectionException

        header_info = json.loads(header_info.decode('utf-8'))

        return header_info

    def _write(self, download_path: str, size: int, progress_bar: Progressbar, received: int = 0):

        # 设置进度条
        progress_bar["value"] = received
        progress_bar["maximum"] = size

        with open(download_path, "ab") as f:

            f.seek(received)

            while received < size:
                value = size - received
                if value > 1024:
                    block = self.session.recv(1024)
                    # 断开连接,收到0长度的数据
                    if len(block) == 0:
                        raise DisconnectionException
                else:
                    block = self.session.recv(value)
                    if len(block) == 0:
                        raise DisconnectionException

                f.write(block)
                received += len(block)
                progress_bar["value"] = received

        print("下载完成")
