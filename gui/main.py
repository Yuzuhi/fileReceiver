import tkinter
from gui.app import Application


def main_loop():
    root = tkinter.Tk()

    root.title("アニメダウンローダー")
    root.geometry("500x300+100+200")

    server_ip = "47.110.232.162"
    server_port = 8021
    Application(server_ip, server_port, master=root)

    root.mainloop()


if __name__ == '__main__':
    main_loop()
