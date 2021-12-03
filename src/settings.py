import sys
from pathlib import Path
from typing import List

RootPath = Path.cwd()


def get_root_path():
    return sys._MEIPASS if getattr(sys, "frozen", False) else RootPath


class Settings:

    def __init__(self):
        # project
        self.Debug = True
        self.VIDEO_FORMAT: List[str] = ["mp4", "mkv", "rmvb", "flv"]
        self.INCOMPLETE_SUFFIX = ".yuzuhi"
        self.Home = Path(__file__)
        # path
        self.RESOURCES_PATH = Path(get_root_path()).joinpath("resources")
        self.ICON_PATH = "catherine.ico"
        self.RIGHT_LABEL_DIR = "right_label"
        self.LOADING_DIR = "loading"
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
        # art label
        self.ART_LABEL_PATH = "art.txt"
        # self.ART_LABEL_HEIGHT
        # self.ART_LABEL_WIDTH
        self.ART_LABEL_X = 40
        self.ART_LABEL_Y = 300
        # reconnect text label
        self.RECONNECT_TEXT_LABEL_X = 20
        self.RECONNECT_TEXT_LABEL_Y = 300
        self.RECONNECT_TEXT_LABEL_TEXT = "只今接続が切れた∑(O_O；)\nでも大丈夫よかりんちゃん、\n再接続していますよ"
        # reconnect gif label
        self.RECONNECT_GIF_LABEL_X = 80
        self.RECONNECT_GIF_LABEL_Y = 370
        self.RECONNECT_GIF_LABEL_PATH = "reconnecting.gif"
        # right_label
        self.RIGHT_LABEL_FONT: tuple = ("Lucida Grande", 8)
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
        self.SAVE_BUTTON_X = 115
        self.SAVE_BUTTON_Y = 270
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
        self.DOWNLOADING_LABEL_COMPLETE_STR: str = "ダウンロード完了"
        # progress label
        self.PENDING_DOWNLOAD_LABEL_X = 260
        self.PENDING_DOWNLOAD_LABEL_Y = 345
        self.PENDING_DOWNLOAD_LABEL_FONT = ("Arial", 7)
        self.PENDING_DOWNLOAD_LABEL_STR: str = "残りダウンロード数：{}"
        # select all button
        self.SELECT_ALL_BTN_TEXT = "すべて選択"
        self.SELECT_ALL_BTN_X = 260
        self.SELECT_ALL_BTN_Y = 8
        self.SELECT_ALL_BTN_WIDTH = 100
        self.SELECT_ALL_BTN_HEIGHT = 20
        # invert selection button
        self.INVERT_SELECTION_BTN_TEXT = "反転選択"
        self.INVERT_SELECTION_BTN_X = 370
        self.INVERT_SELECTION_BTN_Y = 8
        self.INVERT_SELECTION_BTN_WIDTH = 100
        self.INVERT_SELECTION_BTN_HEIGHT = 20

    @property
    def GIF_NUMBER(self) -> int:
        return len([file for file in Path(self.RESOURCES_PATH).iterdir() if file.suffix == ".gif"])


settings = Settings()
