import os
import threading
import tkinter
from tkinter import ttk, messagebox
from tkinter.filedialog import askdirectory
from typing import List

from settings import *
from backend.main.handler import SessionHandler
from backend.main.utils import get_desktop_path
from gui.events import Events


class Application(tkinter.Frame):
    video_path = "../video"

    def __init__(self, server_ip: str, server_port: int, master: tkinter.Tk = None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.session = SessionHandler(server_ip, server_port)
        self.events = Events(self.session, self.master)
        self.videos = self.get_info_from_server()
        # self.path = tkinter.StringVar()
        self.photo = tkinter.PhotoImage(file="../imgs/marci.png")
        # self.top_frame = tkinter.Frame(self, bg="#b3b3b6", width=200, height=200)
        # self.top_frame.pack_propagate(False)
        # self.top_frame.grid(column=0, row=0, pady=5, padx=10, sticky="n")
        self.right_box = tkinter.Listbox(self.master, selectmode="multiple")
        self.right_box.place(x=240, y=20, width=250, height=300)

        self.left_tree = tkinter.ttk.Treeview(self.master, columns="video", show="headings")
        self.left_tree.place(x=10, y=20, width=200, height=200)

        # 保存位置
        self.save_path = tkinter.StringVar()
        self.save_path.set(get_desktop_path())
        self.save_entry = tkinter.Entry(self.master, width=20, textvariable=self.save_path)
        self.save_entry.place(x=100, y=230)
        self.save_btn = tkinter.Button(self.master, text="フォルダーを選択してね", command=self.set_save_path)
        self.save_btn.place(x=120, y=230)

        # 存放下载任务的列表
        self.pending_download_tasks = list()

        # 用于下载的线程
        self.download_thread = False

        self.configure_left_tree()
        self.createWidget()

    def configure_left_tree(self):
        # 配置列标题
        self.left_tree.heading(column="video", text="タイトル")
        # 配置列布局
        self.left_tree.column("video", width=190, anchor="center")
        # 插入数据
        for video in self.videos.keys():
            self.left_tree.insert(parent="", index="end", values=video)

        # 绑定事件
        self.left_tree.bind("<Button-1>", self.title_click, True)

    def title_click(self, event):
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

        # print(self.left_tree.identify_element(x, y))

        # print(self.left_tree.)

    def get_info_from_server(self):
        video_dirs = self.session.get_dirs()
        return self.session.get_videos(video_dirs).get("dirs")

    def set_save_path(self):
        save_path = tkinter.filedialog.askdirectory(title="フォルダーを選択してね", initialdir=get_desktop_path())
        self.save_path.set(save_path)

        print(self.save_path.get())

    def _verify_save_path(self) -> bool:
        return os.path.exists(self.save_path.get())

    def start_download(self):
        # 验证保存地址
        if not self._verify_save_path():
            self.set_save_path()

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

        self.pending_download_tasks.extend(download_request_list)

        if self.download_thread is False:
            self.download_thread = threading.Thread(target=self._start_download)
            self.download_thread.start()
        elif not self.download_thread.is_alive():
            self.download_thread = threading.Thread(target=self._start_download)
            self.download_thread.start()
        else:
            self.pending_download_tasks.extend(download_request_list)

        # self._start_download(download_request_list)

        # dir_name = self.left_tree.ge

    def _start_download(self):
        for video_info in self.pending_download_tasks:
            video_dir, video = video_info
            self.session.single_download(video_dir, video, self.save_path.get())

    def createWidget(self):
        """创建组件"""

        # left.pack()
        # top
        # top_frame = tkinter.Frame(self, bg="#0F61AF", width=2000, height=TOP_HEIGHT)
        # top_frame.pack_propagate(False)
        #
        # # exit button
        # # tkinter.Button(self.master, text="またね", command=self.master.destroy).grid(row=0, column=0, padx=30, sticky="NW")
        # tkinter.Button(top_frame, borderwidth=2, text="またね", command=self.master.destroy).pack(side="left", anchor="nw")

        # download button
        download_btn = tkinter.Button(self.master, text="ダウンロード", command=self.start_download)
        download_btn.place(x=10, y=230)

        #
        # top_frame.pack()
        #
        # # mid
        #
        # mid_frame = tkinter.Frame(self, width=2000, height=200)
        # # mid = tkinter.Frame(mid_frame, width=2000, height=200).pack()
        # tkinter.Button(mid_frame, text="111", width=100, borderwidth=2).grid(row=0)
        #
        # mid_frame.pack()

        # for file, info in video_files.items():
        #     tkinter.Label(self.master, text=file).pack()
        #     tkinter.Radiobutton(self, value=file).pack()

        # self.set_buttons(self.master, self, self.video_path)
        # self.photo = tkinter.PhotoImage(file="../imgs/marci.png")
        # tkinter.Label(self, image=self.photo).pack()

    def list_dirs(self, dirs: dict):
        for k, v in dirs.items():
            tkinter.Button(self.master, text=v["dirName"], ).pack()

    def list_files(self, files: dict):
        for _, v in files.items():
            value = v["name"]
            tkinter.Label(self.master, text=value).pack()
            tkinter.Radiobutton(self, value=value).pack()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.session.close()
