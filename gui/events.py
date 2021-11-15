import os
import tkinter
from tkinter import ttk
from typing import Optional

from backend.main.handler import SessionHandler
from tkinter.filedialog import askdirectory

from gui.settings import settings


class Events:

    def __init__(self, session: SessionHandler, master: tkinter.Tk):
        self.session = session
        self.master = master
        self.path = tkinter.StringVar()

    def start_download(self, e):
        pass

    def get_dir_list(self, e):
        pass

    def title_click(self, event, right_box: Optional[tkinter.Listbox], left_tree: tkinter.ttk.Treeview, videos: dict):

        if not right_box:
            right_box = self.create_right_box()

        x, y, widget = event.x, event.y, event.widget
        index = widget.identify("item", x, y)
        item = left_tree.item(index)

        video = item["values"]
        if not video:
            return
        else:
            video = video[0]

        # delete right box info
        size = right_box.size()
        while size:
            right_box.delete(0)
            size -= 1

        # show video info in right box
        for each_episode in videos[video].keys():
            if each_episode == "videoNumber":
                continue
            right_box.insert("end", each_episode)

    def create_right_box(self) -> tkinter.Listbox:

        right_box = tkinter.Listbox(self.master, selectmode="multiple")

        right_box.place(x=settings.RIGHT_BOX_X,
                        y=settings.RIGHT_BOX_Y,
                        width=settings.RIGHT_BOX_WIDTH,
                        height=settings.RIGHT_BOX_HEIGHT)

        return right_box

    def load_video_info(self, e):
        """点击左侧listbox中的剧集名来在右侧显示详细的剧集信息"""
