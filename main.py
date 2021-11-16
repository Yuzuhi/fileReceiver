import os
import tkinter

from src.backend.utils.parser import Config
from src.backend.utils.utils import get_resource_path
from src.gui.app import Application
from src.settings import settings


# def get_resource_path(relative_path: str):
#     if getattr(sys, "frozen", False):
#         base_path = sys._MEIPASS  # 获取临时资源
#     else:
#         base_path = os.path.abspath(".")  # 获取当前路径
#     return os.path.join(base_path, relative_path)  # 绝对路径

ICON_PATH = get_resource_path(os.path.join(settings.resources, settings.icon_path))


def main_loop():
    window = tkinter.Tk()
    window.title("アニメダウンローダー")
    window.geometry(f"{settings.TOTAL_WIDTH}x{settings.TOTAL_HEIGHT}+200+300")
    # window.iconbitmap(ICON_PATH)
    window.resizable(0, 0)
    server_ip = Config.get("server").get("host")
    server_port = int(Config.get("server").get("port"))

    Application(server_ip, server_port, master=window)
    window.mainloop()


if __name__ == '__main__':
    main_loop()
