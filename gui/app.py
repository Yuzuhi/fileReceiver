import os
import tkinter
from tkinter import ttk
from tkinter.filedialog import askdirectory

from settings import *
from backend.main.handler import SessionHandler
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

        self.createWidget()

    # def load_listBox(self, e):

    def get_info_from_server(self):
        video_dirs = self.session.get_dirs()
        return self.session.get_videos(video_dirs).get("dirs")

    def load_video_info(self, e):
        for index in self.left_box.curselection():
            video = self.left_box.get(index)
            # 在右侧listbox显示剧集
            for each_episode in self.videos[video].keys():
                if each_episode == "videoNumber":
                    continue
                self.right_box.insert("end", each_episode)

    def createWidget(self):
        """创建组件"""
        # left

        # left = tkinter.Frame(self, bg="#0F61AF", width=2000, height=TOP_HEIGHT)
        # columns = ("name", "gender", "age")
        # tree = ttk.Treeview(left, show="headings", columns=columns, selectmode=tkinter.BROWSE)
        # tree.column("name", anchor="center")

        # tree.pack()

        self.left_box = tkinter.Listbox(self.master)
        self.left_box.place(x=10, y=20, width=200, height=200)
        self.left_box.bind("<Button-1>", func=self.load_video_info)

        # use loaded server video data to list videos.
        for video in self.videos.keys():
            self.left_box.insert("end", video)

        # right

        self.right_box = tkinter.Listbox(self.master)
        self.right_box.place(x=230, y=20, width=250, height=300)

        # left.pack()
        # top
        # top_frame = tkinter.Frame(self, bg="#0F61AF", width=2000, height=TOP_HEIGHT)
        # top_frame.pack_propagate(False)
        #
        # # exit button
        # # tkinter.Button(self.master, text="またね", command=self.master.destroy).grid(row=0, column=0, padx=30, sticky="NW")
        # tkinter.Button(top_frame, borderwidth=2, text="またね", command=self.master.destroy).pack(side="left", anchor="nw")
        # # download button
        # tkinter.Button(top_frame, borderwidth=2, text="ダウンロード").pack(side="right", anchor="ne")
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

    def set_buttons(self, root, frame, video_path: str):
        pass
        # btn01 = tkinter.Button(root)
        # btn01["text"] = "ダウンロード"
        # btn01.pack()
        # btn01["command"] =

        # quit button
        # tkinter.Button(frame, text="またね", command=root.destroy).pack()

        # video button
        # for _, videos, _ in os.walk(video_path):
        #     for video in videos:
        #         btn = tkinter.Button(frame)
        #         btn["text"] = video
        #         btn.pack()

        # path select button
        # tkinter.Button(frame, text="アニメをセーブするフォルダーを選択してください", command=self.events.select_path).pack()
        # print(self.events.path.get())

    # def select_path(self):
    #     path_ = askdirectory(initialdir=os.getcwd(), title="アニメをセーブするフォルダーを選択してください")
    #     print(path_)
    # self.path.set(path_)
    #
    # return self.path.get()

    def list_dirs(self, dirs: dict):
        for k, v in dirs.items():
            tkinter.Button(self.master, text=v["dirName"], ).pack()

    def list_files(self, files: dict):
        for _, v in files.items():
            value = v["name"]
            tkinter.Label(self.master, text=value).pack()
            tkinter.Radiobutton(self, value=value).pack()
