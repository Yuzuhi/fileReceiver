import os
import re
from typing import List, Dict

# ini配置文件解析器
from src.settings import settings, RootPath


class IniParser:

    def __init__(self, file: str):
        self.file = file
        self.sectionList: List[str] = []
        self.paramList: List[List[str]] = []
        self.resDict: Dict[str, Dict[str, str]] = dict()

    def load(self) -> Dict[str, Dict[str, str]]:
        # 读取文件
        with open(self.file, 'r') as f:
            data = f.read()
        line_slice = data.split("\n")

        for idx, line in enumerate(line_slice):
            idx += 1
            # 遍历每一行，首先查找section:[sectionName]
            line = line.strip()
            if len(line) == 0 or line.startswith(";") or line.startswith("#"):
                continue

            if line.startswith("[") and line.endswith("]"):
                # 将已经读取到sectionList与paramList的节点与属性保存到resDict中
                if len(self.sectionList) != 0:
                    section_name = self.sectionList.pop()
                    self.resDict[section_name] = self._new_config_dict()
                    self._clean()

                section_name = line[1:len(line) - 1].strip()

                # 校验section_name
                section_name_compile = "^[_a-zA-Z]\w*$"
                if re.match(section_name_compile, section_name) is None:
                    # 不符合变量名规范
                    raise Exception(f"line:{idx},syntax error.")
                else:
                    # 将section_name加至list中用于
                    self.sectionList.append(section_name)

            else:
                line_list: List[str] = line.split("=")
                if len(self.sectionList) == 0 or len(line_list) != 2 or line.startswith("="):
                    raise Exception(f"line:{idx},syntax error.")
                self.paramList.append(line_list)

        section_name = self.sectionList.pop()
        self.resDict[section_name] = self._new_config_dict()

        return self.resDict

    def _new_config_dict(self) -> Dict[str, str]:
        new_dict: Dict[str, str] = dict()
        for i in range(len(self.paramList)):
            new_dict[self.paramList[i][0].strip()] = self.paramList[i][1].strip()
        return new_dict

    def _clean(self):
        # 清除已保存的sectionName与param
        self.sectionList = []
        self.paramList = []


if settings.Debug:
    ini_file_path = os.path.join(RootPath, "config.ini")
else:
    ini_file = os.getcwd()
    ini_file_path = os.path.join(ini_file, "config.ini")

parser = IniParser(ini_file_path)
Config = parser.load()
