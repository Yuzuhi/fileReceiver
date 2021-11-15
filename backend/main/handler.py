import json
import os
import socket
import struct
import sys
import time
from tkinter.ttk import Progressbar
from typing import Optional, List

from backend.main.conn import connect_server
from backend.main.constant import FAIL_CODE, SUCCESS_CODE
from backend.main.exceptions import DisconnectionException, ReconnectSuccessException
from backend.main.utils import to_bytes


class SessionHandler:
    get_dirs_command = 0
    get_videos_command = 1
    download_command = 2

    def __init__(self, server_ip: str, server_port: int, auto_reconnect: bool = True):
        # self.ip = self.get_hostname()
        self.server_ip = server_ip
        self.server_port = server_port
        self.auto_reconnect = auto_reconnect

        try:
            self.session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.session.connect((self.server_ip, self.server_port))
        except socket.error as e:
            if self.auto_reconnect:
                self.re_connect()
            else:
                raise e

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

        self._send_header_info(head_info)
        self.session.send(body_info)

        videos = self._receive_response()

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

        self._send_header_info(head_info)
        self.session.send(body_info)

        dirs = self._receive_response()
        if not dirs or dirs["code"] == FAIL_CODE:
            raise socket.error

        return list(dirs["dirs"].keys())

    def start_download(self, video_path: str, video_name: str, save_path: str, progress_bar: Progressbar):

        body_info = to_bytes(
            command="download",
            code=self.download_command,
            videoDir=video_path,
            videoName=video_name
        )

        head_info = to_bytes(
            command="download",
            code=self.download_command,
            msgSize=sys.getsizeof(body_info)
        )

        self._send_header_info(head_info)
        self.session.send(body_info)

        video_info = self._receive_header_info()
        if not video_info:
            return

        self._write(video_name, video_info["videoSize"], save_path, progress_bar)

    def _write(self, name: str, size: int, save_path: str, progress_bar: Progressbar):

        download_path = os.path.join(save_path, name)
        received = 0
        # 设置进度条
        progress_bar["value"] = 0
        progress_bar["maximum"] = size

        with open(download_path, "wb") as f:

            while received < size:
                value = size - received
                if value > 1024:
                    block = self.session.recv(1024)

                else:
                    block = self.session.recv(value)
                f.write(block)
                received += len(block)
                progress_bar["value"] = received

        print("下载完成")

    def _send_header_info(self, head_info: bytes):

        head_info_len = struct.pack("i", len(head_info))
        self.session.send(head_info_len)
        self.session.send(head_info)

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
            if self.auto_reconnect:
                self.re_connect()
                # 告知调用本次函数的程序重连成功
                raise ReconnectSuccessException
            else:
                raise DisconnectionException

        response_body = json.loads(response_body.decode("utf-8"))

        if response_body["code"] == SUCCESS_CODE:
            return response_body

    def _receive_header_info(self) -> dict:
        response = self.session.recv(4)
        if not response:
            if self.auto_reconnect:
                self.re_connect()
                # 告知调用本次函数的程序重连成功
                raise ReconnectSuccessException
            else:
                raise DisconnectionException

        header_len = struct.unpack('i', response)[0]
        header_info = self.session.recv(header_len)
        if not header_info:
            if self.auto_reconnect:
                self.re_connect()
                # 告知调用本次函数的程序重连成功
                raise ReconnectSuccessException
            else:
                raise DisconnectionException

        header_info = json.loads(header_info.decode('utf-8'))

        return header_info

    def re_connect(self):
        """自动重连模块"""
        server = '{} {}'.format(self.server_ip, self.server_port)
        while True:
            print('Connecting to server {} ...'.format(server))
            try:
                self.session = self.__connect()
            except ConnectionRefusedError:
                print('Connection to server {} failed!'.format(server))
            except TimeoutError:
                print('Connection to server {} timed out!'.format(server))
            except socket.error as e:
                print('Connection to server {} failed! deal to {}'.format(server, e))
            else:
                return

            time.sleep(2.0)

    def __connect(self):
        session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        session.connect((self.server_ip, self.server_port))
        return session
