import tkinter
from pathlib import Path
from tkinter import ttk, messagebox
from tkinter.filedialog import askdirectory

from src.backend.utils.parser import Config
from src.backend.utils.utils import load_ascii_art, get_desktop_path, load_random_file
from src.gui.events import Events, executor
from src.settings import settings


class Application(tkinter.Frame):

    def __init__(self, server_ip: str, server_port: int, master: tkinter.Tk = None):
        super().__init__(master)
        self["height"] = settings.TOTAL_HEIGHT
        self["width"] = settings.TOTAL_WIDTH
        self.master = master
        # bind window close event
        self.master.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.events = Events(server_ip, server_port)
        # 欢迎界面，服务器加载资源完成后会自动摧毁此界面
        self.welcome_frame = tkinter.Frame(self.master, width=settings.TOTAL_WIDTH, height=settings.TOTAL_HEIGHT)
        self.welcome_frame.pack()
        self.welcome_gif_label = tkinter.Label(self.welcome_frame, width=300, height=300)
        self.welcome_gif_label.pack(side="top", pady=20)
        self.welcome_char_label = tkinter.Label(self.welcome_frame, text=settings.WELCOME_CHAR_LABEL_TEXT)
        self.welcome_char_label.pack(side="top")
        self.events.create_welcome_surface(self.welcome_gif_label, self.welcome_frame, self)
        # 创建其它组件
        self.__create_widget()
        # 开启一个线程去异步加载服务器资源
        future = executor.submit(self.events.get_videos)
        # 添加回调函数，根据加载的资源配置left tree 与 right box
        future.add_done_callback(self._callback)
        # 开启一个线程去检查服务器的ip地址与端口是否会改变，如果是，则修改本地文件config.ini保存的服务器ip与端口
        executor.submit(self._check_server)
        # 添加自动更新检查掉线的任务，掉线时会播放重连UI
        self.events.start_disconnection_check(self,
                                              self.disconnect_text_label,
                                              self.disconnect_gif_label,
                                              self.art_label)
        # 添加进度条监视任务
        self.events.add_downloading_update(self.downloading_label, self.progress_bar, self.progress_label)
        # 开启事件循环
        self.after(100, self.events.start_loop, self.master, 100)

    def _callback(self, future):
        self.videos = future.result()
        self.__configure_left_tree()

    def __create_widget(self):
        """创建组件"""
        # 初始化right_box
        self.right_box = None
        # left tree
        self.left_tree = tkinter.ttk.Treeview(self, columns="video", show="headings")
        self.left_tree.place(x=settings.LEFT_TREE_X,
                             y=settings.LEFT_TREE_Y,
                             width=settings.LEFT_TREE_WIDTH,
                             height=settings.LEFT_TREE_HEIGHT)

        # 右侧展示图片的label
        self.right_label = tkinter.Label(self,
                                         text=load_random_file(
                                             settings.RESOURCES_PATH.joinpath(settings.RIGHT_LABEL_DIR)),
                                         font=settings.RIGHT_LABEL_FONT)

        # use right_box size
        self.right_label.place(x=settings.RIGHT_BOX_X,
                               y=settings.RIGHT_BOX_Y,
                               width=settings.RIGHT_BOX_WIDTH,
                               height=settings.RIGHT_BOX_HEIGHT)

        # 左下角art
        self.art_label = tkinter.Label(self,
                                       text=load_ascii_art(
                                           settings.RESOURCES_PATH.joinpath(settings.ART_LABEL_PATH)
                                       ))

        self.art_label.place(x=settings.ART_LABEL_X, y=settings.ART_LABEL_Y)

        # 掉线时左下角的提示，会替换掉art
        self.disconnect_text_label = tkinter.Label(self, text=settings.RECONNECT_TEXT_LABEL_TEXT)
        self.disconnect_gif_label = tkinter.Label(self)

        # 显示当前下载中的任务与进度
        self.downloading_label = tkinter.Label(self,
                                               text=(settings.DOWNLOADING_LABEL_STR.format("", "")),
                                               font=settings.PENDING_DOWNLOAD_LABEL_FONT, anchor="nw")

        self.downloading_label.place(x=settings.DOWNLOADING_LABEL_X, y=settings.DOWNLOADING_LABEL_Y)

        # 显示当前任务数
        self.progress_label = tkinter.Label(self,
                                            text=(settings.PENDING_DOWNLOAD_LABEL_STR.format("")),
                                            font=settings.PENDING_DOWNLOAD_LABEL_FONT, anchor="nw")

        self.progress_label.place(x=settings.PENDING_DOWNLOAD_LABEL_X, y=settings.PENDING_DOWNLOAD_LABEL_Y)

        # 下载的进度条
        self.progress_bar = tkinter.ttk.Progressbar(self, value=0)
        self.progress_bar.place(x=settings.PROGRESS_BAR_X,
                                y=settings.PROGRESS_BAR_Y,
                                width=settings.PROGRESS_BAR_WIDTH,
                                height=settings.PROGRESS_BAR_HEIGHT)

        # 保存位置
        self.save_path = tkinter.StringVar()
        self.save_path.set(get_desktop_path())
        self.save_entry = tkinter.Entry(self,
                                        width=settings.SAVE_ENTRY_WIDTH,
                                        textvariable=self.save_path)

        self.save_entry.place(x=settings.SAVE_ENTRY_X, y=settings.SAVE_ENTRY_Y, width=settings.SAVE_ENTRY_WIDTH)
        self.save_btn = tkinter.Button(self, text="保存フォルダー", command=self._set_save_path)
        self.save_btn.place(x=settings.SAVE_BUTTON_X, y=settings.SAVE_BUTTON_Y)

        # download button
        self.download_btn = tkinter.Button(self, text="ダウンロード", command=self.start_download)
        self.download_btn.place(x=settings.DOWNLOAD_BTN_X,
                                y=settings.DOWNLOAD_BTN_Y,
                                width=settings.DOWNLOAD_BTN_WIDTH,
                                height=settings.DOWNLOAD_BTN_HEIGHT)

        # 添加全选按钮
        self.select_all_btn = tkinter.Button(self, text=settings.SELECT_ALL_BTN_TEXT, command=self.select_btn_click)
        self.select_all_btn.place(
            x=settings.SELECT_ALL_BTN_X,
            y=settings.SELECT_ALL_BTN_Y,
            width=settings.SELECT_ALL_BTN_WIDTH,
            height=settings.SELECT_ALL_BTN_HEIGHT
        )

        # 添加反选按钮
        self.invert_select_btn = tkinter.Button(self,
                                                text=settings.INVERT_SELECTION_BTN_TEXT,
                                                command=self.invert_btn_click)
        self.invert_select_btn.place(
            x=settings.INVERT_SELECTION_BTN_X,
            y=settings.INVERT_SELECTION_BTN_Y,
            width=settings.INVERT_SELECTION_BTN_WIDTH,
            height=settings.INVERT_SELECTION_BTN_HEIGHT
        )

    def __configure_left_tree(self):
        # 配置列标题
        self.left_tree.heading(column="video", text="タイトル")
        # 配置列布局
        self.left_tree.column("video", width=settings.LEFT_TREE_WIDTH - 10, anchor="center")
        # 插入数据
        for video in self.videos.keys():
            self.left_tree.insert(parent="", index="end", values=video)

        # 绑定事件
        self.left_tree.bind("<Button-1>", self._title_click, True)

    def __configure_right_box(self):
        self.right_box = tkinter.Listbox(self, selectmode="multiple")

        self.right_box.place(x=settings.RIGHT_BOX_X,
                             y=settings.RIGHT_BOX_Y,
                             width=settings.RIGHT_BOX_WIDTH,
                             height=settings.RIGHT_BOX_HEIGHT)

    # ----------------------------------------- Events ----------------------------------------------------------------

    def _set_save_path(self):
        save_path = tkinter.filedialog.askdirectory(title="保存フォルダー", initialdir=get_desktop_path())
        self.save_path.set(save_path.replace("/", "\\"))

    def _verify_save_path(self) -> bool:
        if not self.save_path.get():
            return False

        return Path(self.save_path.get()).is_dir()

    def _title_click(self, event):
        if not self.right_box:
            self.__configure_right_box()

        x, y, widget = event.x, event.y, event.widget
        index = widget.identify("item", x, y)
        item = self.left_tree.item(index)

        video = item["values"]
        if not video:
            return
        else:
            video = video[0]

        # delete right box info
        size = self.right_box.size()
        while size:
            self.right_box.delete(0)
            size -= 1

        # show video info in right box
        for each_episode in self.videos[video].keys():
            if each_episode == "videoNumber":
                continue
            self.right_box.insert("end", each_episode)

    # ------------------------------------------- button click -------------------------------------------------------

    def select_btn_click(self):
        """绑定right_box的点击事件"""
        if not self.right_box:
            return
        # 获取所有元素
        items_number = self.right_box.size()

        if items_number == 0:
            return

        self.right_box.selection_set(0, items_number)

    def invert_btn_click(self):
        if not self.right_box:
            return
        # 获取所有元素
        items_number = self.right_box.size()
        for i in range(items_number):
            if self.right_box.select_includes(i):
                self.right_box.selection_clear(i)
            else:
                self.right_box.selection_set(i)

    def start_download(self):
        # 验证保存地址
        if not self._verify_save_path():
            self._set_save_path()

        # 生成所有要下载的剧集信息

        selected_dir = self.left_tree.selection()

        # 获取用户所选择的剧集
        pending_download_index = list(self.right_box.curselection())

        if not pending_download_index:
            tkinter.messagebox.showinfo(title="ブブー", message="ダウンロードしたいアニメを選択してからダウンロードボタンを押すよ\n (๑´ㅂ`๑)")
            return

        selected_dir = self.left_tree.item(selected_dir).get("values")[0]

        download_request_list = list()

        for i in pending_download_index:
            download_request_list.append((selected_dir, self.right_box.get(i)))

            # 清除right_box的选择状态
            self.right_box.select_clear(i)

        # 开启下载线程

        self.events.start_download(download_request_list, self.save_path.get())

    # ------------------------------------------- application close ----------------------------------------------------

    def on_closing(self):
        self.events.session.close_flag = True
        self.master.destroy()

    # ------------------------------------------- update ----------------------------------------------------

    def _check_server(self):
        """检查服务器的ip与port"""
        ip, port = self.events.session.get_new_host()

        if not ip or not port:
            return

        if ip != Config.get("server").get("host"):
            temp = "; this project settings\n[project]version ="
            temp += Config.get("project").get("version")
            temp += "\n; server configs\nhost = "
            temp += ip + "\n"
            temp += f"port = {port}"

            with open(settings.CONFIG_FILE_PATH, "w") as f:
                f.write(temp)
