import os
import tkinter

from backend.main.handler import SessionHandler
from tkinter.filedialog import askdirectory


class Events:

    def __init__(self, session: SessionHandler, frame: tkinter.Tk):
        self.session = session
        self.frame = frame
        self.path = tkinter.StringVar()

    def start_download(self, e):
        pass

    def get_dir_list(self, e):
        pass

    def select_path(self):
        path_ = askdirectory(initialdir=os.getcwd(), title="アニメをセーブするフォルダーを選択してください")

        # self.path.set(path_)
        # print(self.path)
        if path_:
            return path_

    def load_video_info(self, e):
        """点击左侧listbox中的剧集名来在右侧显示详细的剧集信息"""










