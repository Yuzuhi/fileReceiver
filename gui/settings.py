class Settings:
    # project
    Version = "0.1.0"
    ip = "101.228.159.55"
    port = 8021
    # path
    resources = "resources"
    icon_path = "catherine.ico"
    right_label_path = "catherine.txt"
    # total size
    TOTAL_WIDTH: int = 700
    TOTAL_HEIGHT: int = 425
    # left tree size
    LEFT_TREE_HEIGHT = 200
    LEFT_TREE_WIDTH = 230
    LEFT_TREE_X = 10
    LEFT_TREE_Y = 30
    # right_label
    RIGHT_LABEL_FONT: tuple = ("Arial", 2)
    # right box size
    RIGHT_BOX_HEIGHT = 300
    RIGHT_BOX_WIDTH = 430
    RIGHT_BOX_X = 260
    RIGHT_BOX_Y = 30
    # save entry size
    SAVE_ENTRY_X = 10
    SAVE_ENTRY_Y = 235
    SAVE_ENTRY_WIDTH = 200
    SAVE_ENTRY_HEIGHT = 10
    # save button
    SAVE_BUTTON_X = 10
    SAVE_BUTTON_Y = 260
    SAVE_BUTTON_WIDTH = 30
    SAVE_BUTTON_HEIGHT = 30
    # progress bar
    PROGRESS_BAR_WIDTH = 250
    PROGRESS_BAR_HEIGHT = 30
    PROGRESS_BAR_X = 260
    PROGRESS_BAR_Y = 365
    # download button
    DOWNLOAD_BTN_X = 590
    DOWNLOAD_BTN_Y = 365
    DOWNLOAD_BTN_WIDTH = 100
    DOWNLOAD_BTN_HEIGHT = 30
    # surprise label
    SURPRISE_LABEL_X = 10
    SURPRISE_LABEL_Y = 5
    # downloading label
    DOWNLOADING_LABEL_X = 260
    DOWNLOADING_LABEL_Y = 330
    DOWNLOADING_LABEL_FONT: tuple = ("Arial", 7)
    DOWNLOADING_LABEL_STR: str = "ダウンロード中：{}"
    # progress label
    PENDING_DOWNLOAD_LABEL_X = 260
    PENDING_DOWNLOAD_LABEL_Y = 345
    PENDING_DOWNLOAD_LABEL_FONT = ("Arial", 7)
    PENDING_DOWNLOAD_LABEL_STR: str = "残りダウンロード数：{}"



settings = Settings()
