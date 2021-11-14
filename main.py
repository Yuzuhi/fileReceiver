import tkinter
from gui.app import Application
from gui.settings import settings


def main_loop():
    windows = tkinter.Tk()
    windows.title("アニメダウンローダー")
    windows.geometry(f"{settings.TOTAL_WIDTH}x{settings.TOTAL_HEIGHT}+200+300")
    windows.iconbitmap("imgs/catherine.ico")
    windows.resizable(0, 0)
    server_ip = settings.ip
    server_port = settings.port
    Application(server_ip, server_port, master=windows)

    windows.mainloop()


if __name__ == '__main__':
    main_loop()
