import os

from backend.main.constant import MINSIZE



class FileReader:

    def __init__(self, file_path: str):
        self.file_path = file_path
        pass

    def get_size(self):
        return os.path.getsize(self.file_path)

    def read_file(self):
        with open(self.file_path, "rb") as f:
            while True:
                block = f.read(MINSIZE)
                if block:
                    yield block
                else:
                    return

    def write_file(self, output_path: str):
        with open(output_path, "wb") as f:
            for file_bytes in self.read_file():
                if file_bytes:
                    f.write(file_bytes)
                else:
                    return


if __name__ == '__main__':
    path = r"C:\Users\86173"
    filename = "Redbone by Childish Gambino (Looper cover).mp4"
    file_path = os.path.join(path, filename)
    output_path = os.path.join(".", filename)
    f = FileReader(file_path)
    # f.write_file(output_path)
    print(f.get_size())

