import os
import tkinter
from tkinter.filedialog import askdirectory

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
        self._init_resources()

        self.photo = tkinter.PhotoImage(file="../imgs/marci.png")
        self.createWidget()

    def get_info_from_server(self):
        video_dirs = self.session.get_dirs()

        return self.session.get_videos(video_dirs).get("dirs")

    def _init_resources(self):
        for video, video_files in self.videos.items():
            tkinter.Button(self.master, text=video).pack()
            for file, info in video_files.items():
                tkinter.Label(self.master, text=file).pack()
                tkinter.Radiobutton(self, value=file).pack()

    def createWidget(self):
        """创建组件"""
        self.set_buttons(self.master, self, self.video_path)
        # self.photo = tkinter.PhotoImage(file="../imgs/marci.png")
        # tkinter.Label(self, image=self.photo).pack()

    def set_buttons(self, root, frame, video_path: str):
        # btn01 = tkinter.Button(root)
        # btn01["text"] = "ダウンロード"
        # btn01.pack()
        # btn01["command"] =

        # quit button
        tkinter.Button(frame, text="またね", command=root.destroy).pack()

        # video button
        for _, videos, _ in os.walk(video_path):
            for video in videos:
                btn = tkinter.Button(frame)
                btn["text"] = video
                btn.pack()

        # path select button
        tkinter.Button(frame, text="アニメをセーブするフォルダーを選択してください", command=self.events.select_path).pack()
        print(self.events.path.get())

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
