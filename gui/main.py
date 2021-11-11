import tkinter
from gui.app import Application
from settings import *


def main_loop():
    windows = tkinter.Tk()

    windows.title("アニメダウンローダー")
    windows.geometry(f"{TOTAL_WIDTH}x{TOTAL_HEIGHT}+200+300")

    server_ip = "47.110.232.162"
    server_port = 8021
    Application(server_ip, server_port, master=windows)

    windows.mainloop()


if __name__ == '__main__':
    main_loop()
