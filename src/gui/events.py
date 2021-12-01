import os
import random
import tkinter
from tkinter import ttk
from typing import Generator
from PIL import Image, ImageSequence, ImageTk
from concurrent.futures import ThreadPoolExecutor

from src.backend.handler import SessionHandler
from src.backend.utils.parser import Config
from src.backend.utils.utils import has_new_patch
from src.settings import settings

executor = ThreadPoolExecutor(max_workers=5)


class Events:

    def __init__(self, server_ip: str, server_port: int):
        # 事件列表
        self.events_list = []
        self.server_ip = server_ip
        self.server_port = server_port
        self.session = None
        self.pending_download_tasks = []
        # 存放当前下载中的进度信息
        self.downloading_info: dict = {
            "value": 0,  # 下载进度条value
            "maximum": 0,  # 下载进度条最大值
            "video_dir": "",  # 下载中的video所属的文件夹
            "video": "",  # 下载中的video
            "tasks": 0  # 当前剩余的待下载任务数
        }
        # flag
        # 播放欢迎界面的flag
        self.welcome_thread_stopped = False
        # 掉线状态的flag
        self.disconnecting = False
        # 下载线程的flag
        self.download_thread = None

    def start_loop(self, master: tkinter.Tk, interval: int):
        master.after(interval, self.start_loop, master, interval)
        for func, *args in self.events_list:
            func(*args)

    def _submit(self, func, *args):
        self.events_list.append((func, *args))

    @staticmethod
    def _gen_frame(gif_path: str) -> Generator:
        """
        每次都会返回1帧gif frame的生成器
        :param gif_path:
        :return:
        """
        img = Image.open(gif_path)
        width, height = img.size

        while True:
            # gif图片流的迭代器
            frames = ImageSequence.Iterator(img)
            for frame in frames:
                pic = ImageTk.PhotoImage(frame)
                yield (
                    min(width, settings.WELCOME_MAX_WIDTH),
                    min(height, settings.WELCOME_MAX_HEIGHT),
                    pic
                )

    # --------------------------------------------- welcome surface --------------------------------------------------

    def create_welcome_surface(self,
                               welcome_label: tkinter.Label,
                               wait_to_destroy: tkinter.Frame,
                               wait_to_pack: tkinter.Frame
                               ):

        gifs = [gif for gif in os.listdir(settings.RESOURCES_PATH) if
                gif.endswith(".gif") and gif.startswith("loading")]

        gif_path = os.path.join(settings.RESOURCES_PATH, random.choice(gifs))
        if not os.path.exists(gif_path):
            return

        # 创建生成器
        frame_generator = self._gen_frame(gif_path)
        self._submit(self._display_welcome_gif, frame_generator, welcome_label, wait_to_destroy, wait_to_pack)

    def _display_welcome_gif(self,
                             frame_generator: Generator,
                             label: tkinter.Label,
                             wait_to_destroy: tkinter.Frame,
                             wait_to_pack: tkinter.Frame
                             ):

        if self.welcome_thread_stopped and label.winfo_exists():
            wait_to_destroy.destroy()
            wait_to_pack.pack()
        if not label.winfo_exists():
            return
        if not self.welcome_thread_stopped:
            width, height, pic = next(frame_generator)
            label.configure(
                width=min(width, settings.WELCOME_MAX_WIDTH),
                height=min(height, settings.WELCOME_MAX_HEIGHT),
                image=pic)

    # --------------------------------------------- disconnection check ------------------------------------------------
    def start_disconnection_check(self,
                                  master_frame: tkinter.Frame,
                                  disconnect_text_label: tkinter.Label,
                                  disconnect_gif_label: tkinter.Label,
                                  connecting_label: tkinter.Label
                                  ):
        """开启app的掉线检测，掉线时播放掉线gif"""
        gif_path = os.path.join(settings.RESOURCES_PATH, settings.RECONNECT_GIF_LABEL_PATH)
        frame_generator = self._gen_frame(gif_path)

        self._submit(self._display_reconnecting_label_gif,
                     frame_generator,
                     master_frame,
                     disconnect_text_label,
                     disconnect_gif_label,
                     connecting_label)

    def _display_reconnecting_label_gif(self,
                                        frame_generator: Generator,
                                        master_frame: tkinter.Frame,
                                        disconnect_text_label: tkinter.Label,
                                        disconnect_gif_label: tkinter.Label,
                                        connecting_label: tkinter.Label
                                        ):
        if not self.session:
            # 此时还没有连接到服务器上
            return
        if not self.session.disconnect:
            disconnect_text_label.place_forget()
            disconnect_gif_label.place_forget()
            connecting_label.place(x=settings.ART_LABEL_X, y=settings.ART_LABEL_Y)

        else:
            connecting_label.place_forget()

            width, height, pic = next(frame_generator)
            disconnect_gif_label.configure(
                width=min(width, settings.WELCOME_MAX_WIDTH),
                height=min(height, settings.WELCOME_MAX_HEIGHT),
                image=pic)

            disconnect_gif_label.place(x=settings.RECONNECT_GIF_LABEL_X, y=settings.RECONNECT_GIF_LABEL_Y)
            disconnect_text_label.place(x=settings.RECONNECT_TEXT_LABEL_X, y=settings.RECONNECT_TEXT_LABEL_Y)

    # ------------------------------------------- network -------------------------------------------------------------

    def _create_session(self):
        """
        network communications init
        """
        if not self.session:
            self.session = SessionHandler(self.server_ip, self.server_port)

    # ------------------------------------------- network communications -----------------------------------------------
    def get_videos(self):
        self._create_session()
        videos = self.session.get_videos(self.session.get_dirs()).get("dirs")
        self.welcome_thread_stopped = True
        return videos

    def start_download(self, download_request_list: list, save_path: str):

        self.pending_download_tasks.extend(download_request_list)

        if self.download_thread is None:
            self.download_thread = executor.submit(self._start_download, save_path)
        elif self.download_thread.done():
            self.download_thread = executor.submit(self._start_download, save_path)

        # 将当前任务数添加到待更新的 self.downloading_info 这一列表中

        self.downloading_info["tasks"] = len(self.pending_download_tasks)

    def check_update(self):
        """检查更新"""
        now_version = Config.get("project").get("version")
        # todo
        new_version = self.session.get_new_patch_version()
        # 如果没有找到新版本的config.ini或是其它原因，就会返回空值
        if new_version == "":
            return False

        return has_new_patch(new_version, now_version)

    # ------------------------------------------- downloading -------------------------------------------------------

    def add_downloading_update(self,
                               downloading_label: tkinter.Label,
                               progress_bar: tkinter.ttk.Progressbar,
                               progress_label: tkinter.Label
                               ):

        self._submit(self._update_downloading_info_task, downloading_label, progress_bar, progress_label)

    def _start_download(self, save_path: str):
        # show pending videos number
        self.downloading_info["tasks"] = len(self.pending_download_tasks)

        while self.pending_download_tasks:
            video_dir, video = self.pending_download_tasks.pop(0)
            # show pending videos number
            self.downloading_info["tasks"] = len(self.pending_download_tasks)

            # show downloading video title
            self.downloading_info["video_dir"] = video_dir
            self.downloading_info["video"] = video

            self.session.start_download(video_dir, video, save_path, self.downloading_info)

        # clear downloading video title
        self.downloading_info["value"] = -1

    def _update_downloading_info_task(self,
                                      downloading_label: tkinter.Tk,
                                      progress_bar: tkinter.ttk.Progressbar,
                                      progress_label: tkinter.Label):

        if self.downloading_info["maximum"] == 0:
            return

        # 进度条更新

        # 当前没有下载任务
        if self.downloading_info["value"] == -1:
            downloading_label.configure(text=settings.DOWNLOADING_LABEL_STR.format("", ""))
        else:
            progress_bar["value"] = self.downloading_info["value"]
            progress_bar["maximum"] = self.downloading_info["maximum"]
            percentage = float("%.2f" % (self.downloading_info["value"] * 100 / self.downloading_info["maximum"]))
            temp_text = self.downloading_info['video_dir'] + "--" + self.downloading_info['video']
            downloading_label.configure(
                text=settings.DOWNLOADING_LABEL_STR.format(str(percentage) + "%", temp_text)
            )

        # 剩余任务数更新
        progress_label.configure(
            text=(settings.PENDING_DOWNLOAD_LABEL_STR.format(self.downloading_info["tasks"])))

    # ------------------------------------------- updating -------------------------------------------------------

    def _update(self):
        """更新软件"""
        pass


