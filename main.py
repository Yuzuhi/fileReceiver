import os
import tkinter

from src.backend.utils.parser import Config
from src.gui.app import Application
from src.settings import settings



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
