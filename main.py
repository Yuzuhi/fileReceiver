import tkinter
from src.backend.utils.parser import Config
from src.gui.app import Application
from src.settings import settings

window = tkinter.Tk()
window.title("アニメダウンローダー")
window.geometry(f"{settings.TOTAL_WIDTH}x{settings.TOTAL_HEIGHT}+200+300")
window.iconbitmap(settings.RESOURCES_PATH.joinpath(settings.ICON_PATH))
window.resizable(0, 0)
server_ip = Config.get("server").get("host")
server_port = int(Config.get("server").get("port"))

if __name__ == '__main__':
    Application(server_ip, server_port, master=window)
    window.mainloop()
