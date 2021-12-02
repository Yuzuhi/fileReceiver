import json
import socket
import struct

import time
from pathlib import Path
from typing import Optional, List

from src.backend.constant import FAIL_CODE, SUCCESS_CODE
from src.backend.exceptions import DisconnectionException
from src.backend.utils.utils import to_bytes
from src.settings import settings


def reconnect(func):
    """自动重连模块"""

    def wrapper(self, *args, **kwargs):
        """
        :param self: SessionHandler
        :param args:
        :param kwargs:
        :return:
        """
        if self.close_flag:
            raise DisconnectionException
        try:
            return func(self, *args, **kwargs)
        except socket.timeout as e:
            self.disconnect = True
            if not self.auto_reconnect:
                raise e
            else:
                self._reconnect()
                self.disconnect = False
                return func(self, *args, **kwargs)
        except socket.error as e:
            self.disconnect = True
            if not self.auto_reconnect:
                raise e
            else:
                self._reconnect()
                self.disconnect = False
                return func(self, *args, **kwargs)

    return wrapper


class SessionHandler:
    get_dirs_command = 0
    get_videos_command = 1
    download_command = 2
    get_new_version = 3

    def __init__(self, server_ip: str, server_port: int, auto_reconnect: bool = True):
        self.server_ip = server_ip
        self.server_port = server_port
        self.auto_reconnect = auto_reconnect
        self.close_flag = False
        # 表示当前链接是否断开的标志
        self.disconnect = True

        try:
            self.session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self.session.setblocking(False)
            self.session.connect((self.server_ip, self.server_port))
            self.disconnect = False

        except socket.error as e:
            if self.auto_reconnect:
                self._reconnect()
            else:
                raise e

    def _reconnect(self) -> bool:
        server = '{} {}'.format(self.server_ip, self.server_port)
        while True:
            # 睡眠以防止持续请求
            time.sleep(2.0)
            try:
                if self.close_flag:
                    return False
                self.session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.session.connect((self.server_ip, self.server_port))
            except ConnectionRefusedError:
                print('Connection to server {} failed!'.format(server))
            except TimeoutError:
                print('Connection to server {} timed out!'.format(server))
            except DisconnectionException:
                print(DisconnectionException())
            except socket.error as e:
                print('Connection to server {} failed! deal to {}'.format(server, e))
            else:
                self.disconnect = False
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
            msgSize=len(body_info)
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

        header_info = to_bytes(
            command="getDirs",
            code=self.get_dirs_command,
            msgSize=len(body_info)
        )

        self._send_header_info(header_info)

        print(f"send body message,msg:{body_info}")
        self.session.send(body_info)
        print(f"body_info {body_info} has been sent")

        dirs = self._receive_response()
        if not dirs or dirs["code"] == FAIL_CODE:
            raise socket.error

        return list(dirs["dirs"].keys())

    @reconnect
    def start_download(self, video_path: str, video_name: str, save_path: str, downloading_info: dict):

        download_path = Path.home().joinpath(save_path, video_name)

        # 有此文件说明已经下载完成
        if Path(download_path).is_file():
            return

        download_path = str(download_path) + settings.INCOMPLETE_SUFFIX

        if Path(download_path).is_file():
            # 读取大小
            received = Path(download_path).stat().st_size
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
            msgSize=len(body_info)
        )

        self._send_header_info(header_info)
        self.session.send(body_info)

        video_info = self._receive_header_info()
        # 更新下载信息
        downloading_info["video_dir"] = video_path
        downloading_info["video"] = video_name

        self._write(download_path, video_info["videoSize"], downloading_info, received)

    @reconnect
    def get_new_patch_version(self):

        body_info = to_bytes(
            command="version",
            code=self.get_new_version,
        )

        header_info = to_bytes(
            command="version",
            code=self.get_new_version,
            msgSize=len(body_info)
        )

        self._send_header_info(header_info)
        self.session.send(body_info)

        return self._receive_response().get("version")

    def _send_header_info(self, header_info: bytes):

        header_info_len = struct.pack("i", len(header_info))
        print(f"send header message length,length:{header_info_len}")
        self.session.send(header_info_len)
        print(f"send header message,message:{header_info}")
        self.session.send(header_info)
        print(f"header_info {header_info} has been sent")

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

    def _write(self, download_path: str, size: int, downloading_info: dict, received: int = 0):

        # 设置进度条
        downloading_info["value"] = received
        downloading_info["maximum"] = size

        # 设置session超时时间，防止服务器断开链接后客户端阻塞
        self.session.settimeout(10)

        t1 = time.time()

        with open(download_path, "ab") as f:

            f.seek(received)

            while received < size:
                if self.close_flag:
                    return
                value = size - received
                if value > 4096:
                    block = self.session.recv(4096)
                    # 断开连接,收到0长度的数据
                    if len(block) == 0:
                        raise DisconnectionException
                else:
                    block = self.session.recv(value)
                    if len(block) == 0:
                        raise DisconnectionException

                f.write(block)
                received += len(block)
                downloading_info["value"] = received

        t2 = time.time()
        print(f"費やした時間：{t2 - t1}秒")
        # 取消session超时时间
        self.session.settimeout(None)
        # 取消文件正在下载的后缀
        old_name = Path(download_path)
        new_name = download_path.split(settings.INCOMPLETE_SUFFIX)[0]
        old_name.replace(new_name)
        print("ダウンロード完成")
