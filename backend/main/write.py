from backend.main.conn import connect_server


class FileWriter:

    def __init__(self, file_path: str):
        self.file_path = file_path
        # 获取文件列表

    def write(self):
        with connect_server() as socket:
            with open(self.file_path, "wb") as f:
                pass
