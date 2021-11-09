import tkinter
from gui.app import Application


def main_loop():
    root = tkinter.Tk()

    root.title("アニメダウンローダー")
    root.geometry("500x300+100+200")

    Application(master=root)

    root.mainloop()


if __name__ == '__main__':
    main_loop()
