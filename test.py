from pathlib import Path

a = Path.home().joinpath("save_path", "video_name")

print(str(a))
print(type(str(a)))