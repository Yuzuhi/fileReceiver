import os
import threading
import tkinter
from tkinter import ttk, messagebox
from tkinter.filedialog import askdirectory

from backend.main.exceptions import ReconnectSuccessException
from backend.main.handler import SessionHandler
from backend.main.utils import get_desktop_path, get_resource_path, load_ascii_art
from gui.events import Events
from gui.settings import settings

RIGHT_LABEL_PATH = get_resource_path(os.path.join(settings.resources, settings.right_label_path))


class Application(tkinter.Frame):

    def __init__(self, server_ip: str, server_port: int, master: tkinter.Tk = None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.session = SessionHandler(server_ip, server_port, True)

        self.videos = self.get_info_from_server()

        # 存放下载任务的列表
        self.pending_download_tasks = list()

        # 用于下载的线程
        self.download_thread = False
        self.__create_widget()

    def __create_widget(self):
        """创建组件"""

        self.right_box = None
        # left tree
        self.left_tree = tkinter.ttk.Treeview(self.master, columns="video", show="headings")
        self.left_tree.place(x=settings.LEFT_TREE_X,
                             y=settings.LEFT_TREE_Y,
                             width=settings.LEFT_TREE_WIDTH,
                             height=settings.LEFT_TREE_HEIGHT)

        self.__configure_left_tree()

        # 右侧展示图片的label
        self.right_label = tkinter.Label(self.master,
                                         text=load_ascii_art(RIGHT_LABEL_PATH),
                                         font=settings.RIGHT_LABEL_FONT)

        # use right_box size
        self.right_label.place(x=settings.RIGHT_BOX_X,
                               y=settings.RIGHT_BOX_Y,
                               width=settings.RIGHT_BOX_WIDTH,
                               height=settings.RIGHT_BOX_HEIGHT)

        # 显示当前下载中的任务
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

    def get_info_from_server(self):
        try:
            video_dirs = self.session.get_dirs()
            return self.session.get_videos(video_dirs).get("dirs")
        except ReconnectSuccessException:
            # 发生错误但是重连成功
            self.get_info_from_server()

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

        self.progress_label.configure(
            text=(settings.PENDING_DOWNLOAD_LABEL_STR.format(len(self.pending_download_tasks))))

    def _verify_save_path(self) -> bool:
        return os.path.exists(self.save_path.get())

    def _start_download(self):

        # show pending videos number
        self.progress_label.configure(
            text=(settings.PENDING_DOWNLOAD_LABEL_STR.format(len(self.pending_download_tasks)))
        )

        while self.pending_download_tasks:
            video_dir, video = self.pending_download_tasks.pop(0)
            # show pending videos number
            self.progress_label.configure(
                text=(settings.PENDING_DOWNLOAD_LABEL_STR.format(len(self.pending_download_tasks)))
            )

            # show downloading video title
            self.downloading_label.configure(
                text=(settings.DOWNLOADING_LABEL_STR.format(f"{video_dir}---{video}"))
            )

            self.session.start_download(video_dir, video, self.save_path.get(), self.progress_bar)

        # clear downloading video title
        self.downloading_label.configure(
            text=(settings.DOWNLOADING_LABEL_STR.format("", ""))
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.session.close()
