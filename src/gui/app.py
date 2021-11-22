import os
import random
import threading
import tkinter
from tkinter import ttk, messagebox
from tkinter.filedialog import askdirectory
from typing import Generator, Tuple, List

from PIL import Image, ImageSequence, ImageTk

from src.backend.handler import SessionHandler
from src.backend.utils.utils import load_ascii_art, get_desktop_path
from src.settings import settings


class Application(tkinter.Frame):

    def __init__(self, server_ip: str, server_port: int, master: tkinter.Tk = None):
        super().__init__(master)
        self.master = master
        # bind window close event
        self.master.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.server_ip = server_ip
        self.server_port = server_port
        self.pack()
        # 存放下载任务的列表
        self.pending_download_tasks = list()
        # 存放当前下载中的进度信息
        self.downloading_info: dict = {
            "value": 0,  # 下载进度条value
            "maximum": 0,  # 下载进度条最大值
            "video_dir": "",  # 下载中的video所属的文件夹
            "video": "",  # 下载中的video
            "tasks": 0  # 当前剩余的待下载任务数
        }
        # 用于下载的线程
        self.download_thread = False
        # 用于定时函数的事件列表
        self.events: List[Tuple] = []
        # 开启一个线程去异步加载服务器资源
        self.load_server_thread = threading.Thread(target=self.__load_from_server)
        self.load_server_thread.start()
        self.load_server_stopped = False
        # 欢迎界面，服务器加载资源完成后摧毁此界面
        self.welcome_frame = tkinter.Frame(self.master, width=settings.TOTAL_WIDTH, height=settings.TOTAL_HEIGHT)
        self.welcome_frame.pack()
        self.welcome_gif_label = tkinter.Label(self.welcome_frame, width=300, height=300)
        self.welcome_gif_label.pack(side="top", pady=20)
        self.welcome_char_label = tkinter.Label(self.welcome_frame, text=settings.WELCOME_CHAR_LABEL_TEXT)
        self.welcome_char_label.pack(side="top")
        # 设置一个欢迎界面是否被摧毁的flag
        self.welcome_frame_been_destroyed = False
        # 设置一个查看欢迎界面是否停止的flag
        self.welcome_thread_stopped = False
        self.__welcome__()
        self.master.after(100, self._event_loop)

    def __welcome__(self):
        """创建欢迎界面，等待从服务器获取资源"""
        # 随机启用一个gif
        gifs = [gif for gif in os.listdir(settings.RESOURCES_PATH) if gif.endswith(".gif")]
        gif_path = os.path.join(settings.RESOURCES_PATH, random.choice(gifs))
        if not os.path.exists(gif_path):
            return
        # 创建生成器
        frame_generator = self.gen_frame(gif_path)
        self._submit(self._show_gif, frame_generator)

    def _event_loop(self):
        """
        用来指派任务给定时函数，如果任务完成则关闭定时函数
        当前的任务仅有加载界面与定时从服务器获取资源的任务
        当从服务器获取到资源后，会更改self.welcome_thread_stopped = False的值
        然后停止下一次定时任务并加载其它组件
        """
        self.master.after(100, self._event_loop)
        # 更新下载进度条
        if self.welcome_frame_been_destroyed:
            self._update_downloading_info()

        # 结束欢迎画面
        elif self.welcome_thread_stopped:
            self.welcome_frame.destroy()
            self.welcome_frame_been_destroyed = True
            self.__create_widget()

        # 更新欢迎画面
        else:
            for func, *args in self.events:
                func(*args)

    def _submit(self, func, *args):
        self.events.append((func, *args))

    def _show_gif(self, frame_generator: Generator):
        width, height, pic = next(frame_generator)
        self.welcome_gif_label.configure(
            width=min(width, settings.WELCOME_MAX_WIDTH),
            height=min(height, settings.WELCOME_MAX_HEIGHT)
            , image=pic)

    @staticmethod
    def gen_frame(gif_path: str) -> Generator:
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

    def __load_from_server(self):
        self.session = SessionHandler(self.server_ip, self.server_port)
        self.videos = self.session.get_videos(self.session.get_dirs()).get("dirs")
        # 异步加载完成后发送信号让主线程继续进行
        self.welcome_thread_stopped = True

    def __create_widget(self):
        """创建组件"""
        # left tree
        self.left_tree = tkinter.ttk.Treeview(self.master, columns="video", show="headings")
        self.left_tree.place(x=settings.LEFT_TREE_X,
                             y=settings.LEFT_TREE_Y,
                             width=settings.LEFT_TREE_WIDTH,
                             height=settings.LEFT_TREE_HEIGHT)

        self.__configure_left_tree()

        self.right_box = None

        # 右侧展示图片的label
        self.right_label = tkinter.Label(self.master,
                                         text=load_ascii_art(
                                             os.path.join(settings.RESOURCES_PATH, settings.RIGHT_LABEL_PATH)),
                                         font=settings.RIGHT_LABEL_FONT)

        # use right_box size
        self.right_label.place(x=settings.RIGHT_BOX_X,
                               y=settings.RIGHT_BOX_Y,
                               width=settings.RIGHT_BOX_WIDTH,
                               height=settings.RIGHT_BOX_HEIGHT)

        # 显示当前下载中的任务与进度
        self.downloading_label = tkinter.Label(self.master,
                                               text=(settings.DOWNLOADING_LABEL_STR.format("", "")),
                                               font=settings.PENDING_DOWNLOAD_LABEL_FONT, anchor="nw")

        self.downloading_label.place(x=settings.DOWNLOADING_LABEL_X, y=settings.DOWNLOADING_LABEL_Y)

        # 显示当前任务数
        self.progress_label = tkinter.Label(self.master,
                                            text=(settings.PENDING_DOWNLOAD_LABEL_STR.format("")),
                                            font=settings.PENDING_DOWNLOAD_LABEL_FONT, anchor="nw")

        self.progress_label.place(x=settings.PENDING_DOWNLOAD_LABEL_X, y=settings.PENDING_DOWNLOAD_LABEL_Y)

        # 下载的进度条
        self.progress_bar = tkinter.ttk.Progressbar(self.master, value=0)
        self.progress_bar.place(x=settings.PROGRESS_BAR_X,
                                y=settings.PROGRESS_BAR_Y,
                                width=settings.PROGRESS_BAR_WIDTH,
                                height=settings.PROGRESS_BAR_HEIGHT)

        # 保存位置
        self.save_path = tkinter.StringVar()
        self.save_path.set(get_desktop_path())
        self.save_entry = tkinter.Entry(self.master,
                                        width=settings.SAVE_ENTRY_WIDTH,
                                        textvariable=self.save_path)

        self.save_entry.place(x=settings.SAVE_ENTRY_X, y=settings.SAVE_ENTRY_Y, width=settings.SAVE_ENTRY_WIDTH)
        self.save_btn = tkinter.Button(self.master, text="保存フォルダー", command=self._set_save_path)
        self.save_btn.place(x=settings.SAVE_BUTTON_X, y=settings.SAVE_BUTTON_Y)

        # download button
        download_btn = tkinter.Button(self.master, text="ダウンロード", command=self.start_download)
        download_btn.place(x=settings.DOWNLOAD_BTN_X,
                           y=settings.DOWNLOAD_BTN_Y,
                           width=settings.DOWNLOAD_BTN_WIDTH,
                           height=settings.DOWNLOAD_BTN_HEIGHT)

    def __configure_left_tree(self):
        # 配置列标题
        self.left_tree.heading(column="video", text="タイトル")
        # 配置列布局
        self.left_tree.column("video", width=settings.LEFT_TREE_WIDTH - 10, anchor="center")
        # 插入数据
        for video in self.videos.keys():
            self.left_tree.insert(parent="", index="end", values=video)

        # 绑定事件
        self.left_tree.bind("<Button-1>", self._title_click, True)

    def _create_right_box(self):
        self.right_box = tkinter.Listbox(self.master, selectmode="multiple")

        self.right_box.place(x=settings.RIGHT_BOX_X,
                             y=settings.RIGHT_BOX_Y,
                             width=settings.RIGHT_BOX_WIDTH,
                             height=settings.RIGHT_BOX_HEIGHT)

    # ----------------------------------------- Events ----------------------------------------------------------------

    def _set_save_path(self):
        save_path = tkinter.filedialog.askdirectory(title="保存フォルダー", initialdir=get_desktop_path())
        self.save_path.set(save_path)

    def _title_click(self, event):
        if not self.right_box:
            self._create_right_box()

        x, y, widget = event.x, event.y, event.widget
        index = widget.identify("item", x, y)
        item = self.left_tree.item(index)

        video = item["values"]
        if not video:
            return
        else:
            video = video[0]

        # delete right box info
        size = self.right_box.size()
        while size:
            self.right_box.delete(0)
            size -= 1

        # show video info in right box
        for each_episode in self.videos[video].keys():
            if each_episode == "videoNumber":
                continue
            self.right_box.insert("end", each_episode)

    def start_download(self):
        # 验证保存地址
        if not self._verify_save_path():
            self._set_save_path()

        # 生成所有要下载的剧集信息

        selected_dir = self.left_tree.selection()

        # 获取用户所选择的剧集
        pending_download_index = list(self.right_box.curselection())

        if not pending_download_index:
            tkinter.messagebox.showinfo(title="ブブー", message="ダウンロードしたいアニメを選択してからダウンロードボタンを押すよ\n (๑´ㅂ`๑)")
            return

        selected_dir = self.left_tree.item(selected_dir).get("values")[0]

        download_request_list = list()

        for i in pending_download_index:
            download_request_list.append((selected_dir, self.right_box.get(i)))

            # 清除right_box的选择状态
            self.right_box.select_clear(i)

        # 开启下载线程

        self.pending_download_tasks.extend(download_request_list)

        if self.download_thread is False:
            self.download_thread = threading.Thread(target=self._start_download)
            self.download_thread.start()
        elif not self.download_thread.is_alive():
            self.download_thread = threading.Thread(target=self._start_download)
            self.download_thread.start()

        # 将当前任务数添加到待更新的 self.downloading_info 这一列表中

        self.downloading_info["tasks"] = len(self.pending_download_tasks)

    def _verify_save_path(self) -> bool:
        return os.path.exists(self.save_path.get())

    def _start_download(self):
        # show pending videos number
        self.downloading_info["tasks"] = len(self.pending_download_tasks)

        while self.pending_download_tasks:
            video_dir, video = self.pending_download_tasks.pop(0)
            # show pending videos number
            self.downloading_info["tasks"] = len(self.pending_download_tasks)

            # show downloading video title
            self.downloading_info["video_dir"] = video_dir
            self.downloading_info["video"] = video

            self.session.start_download(video_dir, video, self.save_path.get(), self.downloading_info)

        # clear downloading video title
        self.downloading_info["value"] = -1

    def _update_downloading_info(self):

        if self.downloading_info["maximum"] == 0:
            return

        # 进度条更新

        # 当前没有下载任务
        if self.downloading_info["value"] == -1:
            self.downloading_label.configure(text=settings.DOWNLOADING_LABEL_STR.format("", ""))
        else:
            self.progress_bar["value"] = self.downloading_info["value"]
            self.progress_bar["maximum"] = self.downloading_info["maximum"]
            percentage = float("%.2f" % (self.downloading_info["value"] * 100 / self.downloading_info["maximum"]))
            temp_text = self.downloading_info['video_dir'] + "--" + self.downloading_info['video']
            self.downloading_label.configure(
                text=settings.DOWNLOADING_LABEL_STR.format(str(percentage) + "%", temp_text)
            )

        # 剩余任务数更新
        self.progress_label.configure(
            text=(settings.PENDING_DOWNLOAD_LABEL_STR.format(self.downloading_info["tasks"])))

    def on_closing(self):
        self.session.close_flag = True
        self.master.destroy()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.session.close()
