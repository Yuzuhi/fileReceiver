# This is a sample Python script.

# Press Alt+Shift+X to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
import os

from backend.main.handler import SessionHandler

if __name__ == '__main__':
    ip = "127.0.0.1"
    # ip = "47.110.232.162"
    port = 8021
    downloader = SessionHandler(ip, port)
    # path = os.path.abspath(".")
    # path = os.path.join(path, "video/file.mp4")
    # downloader.write(path)
    downloader.test()
