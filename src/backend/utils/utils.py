import os
import socket
import json
import sys
import winreg


def get_host_ip():
    extra_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    extra_conn.connect(('8.8.8.8', 80))
    ip = extra_conn.getsockname()[0]
    extra_conn.close()

    return ip


def to_bytes(**kwargs) -> bytes:
    if kwargs:
        return json.dumps(kwargs).encode("utf-8")


def get_desktop_path() -> str:
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    path = winreg.QueryValueEx(key, "Desktop")[0]
    return path


def video_size_str(size: int) -> str:
    unit = ["KB", "MB", "GB", "TB"]
    count = -1
    if size < 1024:
        return str(size) + "B"
    else:
        while size >= 1024:
            size /= 1024
            count += 1
    return str('%.2f' % size) + unit[count]


def load_ascii_art(path: str):
    with open(path, "r") as f:
        data = f.read()
    return data


def has_new_patch(new: str, now: str) -> bool:
    new = new.split(".")
    now = now.split(".")
    for i in range(len(now)):
        if int(new[i]) > int(now[i]):
            return True
    return False
