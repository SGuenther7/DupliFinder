from PyQt6.QtWidgets import (QMainWindow, QPushButton, QWidget, QLabel,
    QVBoxLayout, QHBoxLayout, QGroupBox, QSizePolicy, QSpinBox, QCheckBox, QFileDialog,
    QScrollArea, QLineEdit)

from PyQt6.QtCore import Qt

from os.path import getsize, exists, normpath
from os import remove, startfile
import send2trash

from util import util


class ListContainer(QScrollArea):

    def __init__(self):
        super().__init__()
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.setWidgetResizable(True)

        self.list=[]
        
        container=QWidget()
        self.setWidget(container)
        self.layout = QVBoxLayout(container)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # self.layout.setSpacing(-10)
        # QVBoxLayout().setSpacing(0)
        # self.layout.

    def addItem(self, item: QWidget):
        self.list.append(item)
        self.layout.addWidget(item)

    def removeItem(self, item):
        self.layout.removeWidget(item)
        self.list.remove(item)

    def getList(self) -> list[str]:
        return [item.getPath() for item in self.list if item.isChecked()]

class DirectoryToCheck(QWidget):
    def __init__(self, directory_path, parent):
        super().__init__()

        self.path = directory_path
        self.parent = parent

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.check = QCheckBox()
        layout.addWidget(self.check)

        self.label = QLabel(self.path)
        layout.addWidget(self.label)

        self.btn_pick_directory = QPushButton("Change Directory")
        self.btn_pick_directory.clicked.connect(self._pickDirectory)
        layout.addWidget(self.btn_pick_directory)

        self.btn_remove = QPushButton("remove")
        self.btn_remove.clicked.connect(self._remove)
        layout.addWidget(self.btn_remove)

    def _pickDirectory(self):
        directory = QFileDialog.getExistingDirectory()
        self.label.setText(directory)

    def _remove(self):
        self.parent: StartUpWidget
        self.parent.removeItem(self)

    def isChecked(self):
        return self.check.isChecked()

    def getPath(self):
        return self.label.text()

class StartUpWidget(QWidget):
    def __init__(self, config):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.list = ListContainer()
        layout.addWidget(self.list)

        inserter = QWidget()
        inserter_layout = QHBoxLayout()
        inserter.setLayout(inserter_layout)
        layout.addWidget(inserter)
        
        self.inserter_input = QLineEdit("Test")
        inserter_layout.addWidget(self.inserter_input)

        inserter_btn_pick = QPushButton("Pick Directory")
        inserter_btn_pick.clicked.connect(self._pickDirectory)
        inserter_layout.addWidget(inserter_btn_pick)

        inserter_btn_add = QPushButton("Add")
        inserter_btn_add.clicked.connect(self._addDirectory)
        inserter_layout.addWidget(inserter_btn_add)

        targets = config.get("targets", [])
        for target in targets:
            self.addItem(target)

    def _pickDirectory(self):
        directory = QFileDialog.getExistingDirectory()
        self.inserter_input.setText(directory)

    def _addDirectory(self):
        # if exists(self.inserter_input.text()):
        #     self.addItem(self.inserter_input.text())

        self.addItem("test1")
        self.addItem("test2")
        self.addItem("test3")
        self.addItem("test4")
        self.inserter_input.clear()

    def addItem(self, path: str):
        item = DirectoryToCheck(path, self)
        self.list.addItem(item)

    def removeItem(self, item: DirectoryToCheck):
        self.list.removeItem(item)

    def getList(self) -> list[str]:
        return self.list.getList()
    