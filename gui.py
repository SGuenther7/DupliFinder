from PyQt6.QtWidgets import (QMainWindow, QPushButton, QWidget, QLabel,
    QVBoxLayout, QHBoxLayout, QGroupBox, QSizePolicy, QSpinBox)

from os.path import getsize, exists, normpath
from os import remove, startfile
import send2trash

class MainWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()

        self.setCentralWidget(MainWidget(data))

class MainWidget(QWidget):
    def __init__(self, data):
        super().__init__()

        self.data = data

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.cur_idx = 0

        ## navigation
        top_row = QHBoxLayout()
        top_row_widget = QGroupBox()
        top_row_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        top_row_widget.setLayout(top_row)
        
        btn_prev = QPushButton("Prev")
        btn_prev.clicked.connect(self.btn_prev)
        top_row.addWidget(btn_prev)

        self.current_idx_box = QSpinBox()
        self.current_idx_box.setRange(1, len(self.data))
        self.current_idx_box.valueChanged.connect(self.changeIDX)
        top_row.addWidget(self.current_idx_box)

        self.label_idx = QLabel(f"{self.cur_idx + 1} / {len(self.data)}")
        top_row.addWidget(self.label_idx)

        btn_next = QPushButton("Next")
        btn_next.clicked.connect(self.btn_next)
        top_row.addWidget(btn_next)

        layout.addWidget(top_row_widget)

        ## info
        self.results = QGroupBox()
        result_layout = QVBoxLayout()
        self.results.setLayout(result_layout)
        layout.addWidget(self.results)

        self.results_size = QLabel("Size: ")
        result_layout.addWidget(self.results_size)

        self.results_deleted = QLabel("Moved To Bin: ")
        result_layout.addWidget(self.results_deleted)
        self.bytes_deleted = 0

        ## file info
        self.dupli_display = QVBoxLayout()
        dupli_display_widget = QGroupBox()
        dupli_display_widget.setLayout(self.dupli_display)
        self.file_container = []

        layout.addWidget(dupli_display_widget)

        self.validate()

    def btn_next(self):
        self.cur_idx = (self.cur_idx + 1) % len(self.data)
        self.validate()

    def btn_prev(self):
        self.cur_idx = (self.cur_idx - 1) % len(self.data)
        self.validate(-1)

    def changeIDX(self, newVal):
        self.cur_idx = newVal - 1
        self.validate()

    def deleteAllExcept(self, fileToKeep: "DupliDisplay"):
        deleted_size = 0
        for elem in self.file_container:
            if normpath(elem.file_path) == normpath(fileToKeep.file_path):
                continue
            deleted_size += elem.file_size
            send2trash.send2trash(normpath(elem.file_path))

        self.movedToBin(deleted_size)
        self.validate()

    def movedToBin(self, bytes: int):
        
        from main import formatBytes

        self.bytes_deleted += bytes
        self.results_deleted.setText(f"Moved To Bin: {formatBytes(self.bytes_deleted)}")

    def validate(self, direction = 1):

        for widget in self.file_container:
            self.dupli_display.removeWidget(widget)

        self.file_container.clear()

        retries = 0
        # while len([f for f in self.data[list(self.data)[self.cur_idx]] if exists(f)]) < 2:

        while True:
            if len(self.data[list(self.data)[self.cur_idx]]) > 1:
                if len([f for f in self.data[list(self.data)[self.cur_idx]] if exists(f)]) > 1:
                    break

            self.cur_idx = (self.cur_idx + direction) % len(self.data)
            retries += 1

            if retries > len(self.data):
                self.label_idx.setText(f"ALL DONE")
                return

        # self.current_idx_box.setValue(self.cur_idx + 1)
        self.label_idx.setText(f"{self.cur_idx + 1} / {len(self.data)}")
        
        for file in self.data[list(self.data)[self.cur_idx]]:
            if exists(file):
                self.file_container.append(
                    DupliDisplay(list(self.data)[self.cur_idx], file, getsize(file), self))
                self.dupli_display.addWidget(self.file_container[-1])

        equal = len(set([item.file_size for item in self.file_container])) == 1

        self.results_size.setText(f"Size: {"Same" if equal else "Different" }")
        self.results_size.setStyleSheet("QLabel { background-color : lightgreen; }" if equal
                                        else "QLabel { background-color : red; }");

class DupliDisplay(QWidget):
    def __init__(self, hash, file_path, size, parent):
        super().__init__()
        self.file_path = file_path
        self.parent = parent
        
        parts = file_path.replace("\\", "/").split("/")

        print(self.file_path)
        self.name = parts[-1]
        self.path = "/".join(parts[:-1])
        self.hash = hash
        self.file_size = size

        layout = QVBoxLayout()
        self.setLayout(layout)

        from main import formatBytes

        layout.addWidget(QLabel(f"File: {self.name}"))
        layout.addWidget(QLabel(f"Path: {self.path}"))
        layout.addWidget(QLabel(f"Hash: {self.hash}"))
        layout.addWidget(QLabel(f"Size: {formatBytes(self.file_size)}"))

        btns = QWidget()
        layout.addWidget(btns)
        btns_layout = QHBoxLayout()
        btns.setLayout(btns_layout)

        del_btn = QPushButton("Delete")
        del_btn.clicked.connect(self.btn_delete)
        btns_layout.addWidget(del_btn)

        open_btn = QPushButton("Open")
        open_btn.clicked.connect(self.btn_open)
        btns_layout.addWidget(open_btn)

        keep_btn = QPushButton("Keep only this File")
        keep_btn.clicked.connect(self.btn_keep_only_this)
        btns_layout.addWidget(keep_btn)


    def btn_delete(self):
        if exists(self.file_path):
            # remove(self.file_path)
            send2trash.send2trash(normpath(self.file_path))
            self.parent.movedToBin(self.file_size)
            self.parent: MainWidget
            self.parent.validate()

    def btn_open(self):
        if exists(self.file_path):
            # try:
            #     subprocess.run(['start', f"'{self.file_path}'"], check=True)
            # except:
            #     print(f"{self.file_path} -> {exists(self.file_path)}")
            startfile(self.file_path, 'open')

    def btn_keep_only_this(self):
        self.parent.deleteAllExcept(self)

    def __eq__(self, other):
        if hasattr(other, "hash") and hasattr(other, "size"):
            return self.hash == other.hash and self.size == other.hash
        return False

if __name__ == "__main__":
    from main import start
    start()
    