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

        # self.session = SessionHandler(server_ip, server_port)
        # self.events = Events(self.session, self.master)
        # self.videos = self.get_info_from_server()
        # self.path = tkinter.StringVar()
        # self.photo = tkinter.PhotoImage(file="../imgs/marci.png")
        # self.top_frame = tkinter.Frame(self, bg="#b3b3b6", width=200, height=200)
        # self.top_frame.pack_propagate(False)
        # self.top_frame.grid(column=0, row=0, pady=5, padx=10, sticky="n")
        # self.createWidget()

    def get_info_from_server(self):
        video_dirs = self.session.get_dirs()

        return self.session.get_videos(video_dirs).get("dirs")

    def createWidget(self):
        """创建组件"""
        top_frame = tkinter.Frame(self.master, bg="black", width=200, height=200)
        # top_frame.pack_propagate(False)
        top_frame.grid(column=0, row=0, pady=5, padx=10, sticky="n")

        # exit button
        # tkinter.Button(top_frame, text="またね", command=self.master.destroy).grid(row=0, column=0, sticky=tkinter.EW)
        tkinter.Button(top_frame, text="またね", command=self.master.destroy).pack(side="left")
        # download button
        # tkinter.Button(top_frame, text="ダウンロード").grid(row=0, column=1, sticky=tkinter.EW)
        tkinter.Button(top_frame, text="ダウンロード").pack(side="right")

        # use loaded server video data to create buttons which are named as videos title.
        for row, video in enumerate(self.videos.keys()):
            tkinter.Button(self, text=video, width=2).grid(row=row + 1)
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
