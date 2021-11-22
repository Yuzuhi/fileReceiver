import os
import sys

RootPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_root_path():
    return sys._MEIPASS if getattr(sys, "frozen", False) else RootPath


class Settings:

    def __init__(self):
        # project
        self.Debug = True
        # path
        self.RESOURCES_PATH = os.path.join(get_root_path(), "resources")
        self.ICON_PATH = "catherine.ico"
        self.RIGHT_LABEL_PATH = "catherine.txt"
        self.GIF_PATH = "loading{}"
        # total size
        self.TOTAL_WIDTH: int = 700
        self.TOTAL_HEIGHT: int = 425
        # welcome label
        self.WELCOME_MAX_HEIGHT = 425
        self.WELCOME_MAX_WIDTH = 600
        # welcome gif label
        self.WELCOME_GIF_LABEL_HEIGHT = 300
        self.WELCOME_GIF_LABEL_WIDTH = 300
        # welcome char label
        self.WELCOME_CHAR_LABEL_TEXT = "ローディング中..."
        # left tree size
        self.LEFT_TREE_HEIGHT = 200
        self.LEFT_TREE_WIDTH = 230
        self.LEFT_TREE_X = 10
        self.LEFT_TREE_Y = 30
        # right_label
        self.RIGHT_LABEL_FONT: tuple = ("Arial", 2)
        # right box size
        self.RIGHT_BOX_HEIGHT = 300
        self.RIGHT_BOX_WIDTH = 430
        self.RIGHT_BOX_X = 260
        self.RIGHT_BOX_Y = 30
        # save entry size
        self.SAVE_ENTRY_X = 10
        self.SAVE_ENTRY_Y = 235
        self.SAVE_ENTRY_WIDTH = 200
        self.SAVE_ENTRY_HEIGHT = 10
        # save button
        self.SAVE_BUTTON_X = 10
        self.SAVE_BUTTON_Y = 260
        self.SAVE_BUTTON_WIDTH = 30
        self.SAVE_BUTTON_HEIGHT = 30
        # progress bar
        self.PROGRESS_BAR_WIDTH = 250
        self.PROGRESS_BAR_HEIGHT = 30
        self.PROGRESS_BAR_X = 260
        self.PROGRESS_BAR_Y = 365
        # download button
        self.DOWNLOAD_BTN_X = 590
        self.DOWNLOAD_BTN_Y = 365
        self.DOWNLOAD_BTN_WIDTH = 100
        self.DOWNLOAD_BTN_HEIGHT = 30
        # surprise label
        self.SURPRISE_LABEL_X = 10
        self.SURPRISE_LABEL_Y = 5
        # downloading label
        self.DOWNLOADING_LABEL_X = 260
        self.DOWNLOADING_LABEL_Y = 330
        self.DOWNLOADING_LABEL_FONT: tuple = ("Arial", 7)
        self.DOWNLOADING_LABEL_STR: str = "ダウンロード中 {}：{}"
        # progress label
        self.PENDING_DOWNLOAD_LABEL_X = 260
        self.PENDING_DOWNLOAD_LABEL_Y = 345
        self.PENDING_DOWNLOAD_LABEL_FONT = ("Arial", 7)
        self.PENDING_DOWNLOAD_LABEL_STR: str = "残りダウンロード数：{}"

    @property
    def GIF_NUMBER(self) -> int:
        return len([file for file in os.listdir(self.RESOURCES_PATH) if file.split(".")[-1] == "gif"])


settings = Settings()
