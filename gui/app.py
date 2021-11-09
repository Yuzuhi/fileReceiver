import os
import tkinter
from tkinter.filedialog import askdirectory

from backend.main.handler import SessionHandler
from gui.events import Events


class Application(tkinter.Frame):
    anime_path = "../anime"

    def __init__(self, master: tkinter.Tk = None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.events = Events(123, self.master)
        self.session = SessionHandler(1, 2, 3, 4)

        self.anime_dict = dict()
        self.dirs = self.session.get_dirs()
        for anime in self.dirs.keys():
            self.anime_dict[anime] = self.session.get_files(anime)
        # self.path = tkinter.StringVar()
        self._init_resources()

        self.photo = tkinter.PhotoImage(file="../imgs/marci.png")
        self.createWidget()

    # def _init_resources(self):
    #     dirs = {
    #         "dir1": {
    #             "dirName": "tessa",
    #             "dirImage": ""
    #         },
    #         "dir2": {
    #             "dirName": "karin",
    #             "dirImage": ""
    #         }
    #     }
    #
    #     self.list_dirs(dirs)

    def _init_resources(self):
        for anime, anime_files in self.anime_dict.items():
            tkinter.Button(self.master, text=anime).pack()
            for file, info in anime_files.items():
                tkinter.Label(self.master, text=file).pack()
                tkinter.Radiobutton(self, value=file).pack()

    def createWidget(self):
        """创建组件"""
        self.set_buttons(self.master, self, self.anime_path)
        # self.photo = tkinter.PhotoImage(file="../imgs/marci.png")
        label01 = tkinter.Label(self, image=self.photo)
        label01.pack()

    def set_buttons(self, root, frame, anime_path: str):
        # btn01 = tkinter.Button(root)
        # btn01["text"] = "ダウンロード"
        # btn01.pack()
        # btn01["command"] =

        # quit button
        tkinter.Button(frame, text="またね", command=root.destroy).pack()

        # anime button
        for _, animes, _ in os.walk(anime_path):
            for anime in animes:
                btn = tkinter.Button(frame)
                btn["text"] = anime
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
