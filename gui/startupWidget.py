from PyQt6.QtWidgets import (QPushButton, QWidget, QLabel, QApplication,
    QVBoxLayout, QHBoxLayout, QCheckBox, QFileDialog, QScrollArea, QLineEdit,
    QSizePolicy)

from PyQt6.QtCore import Qt

from os.path import exists, isdir

class ListContainer(QScrollArea):

    def __init__(self):
        super().__init__()
        
        self.itemList = []
       
        self.setWidgetResizable(True)
        scroll_list = QWidget(self)

        self.layout: QVBoxLayout = QVBoxLayout(scroll_list)
        scroll_list.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)

        self.setWidget(scroll_list)

    def addDirectory(self, item: 'DirectoryToCheck'):
        self.layout.addWidget(item)
        self.itemList.append(item)

    def removeDirectory(self, item):
        print(f"removing: {item.getPath()}")
        self.layout.removeWidget(item)
        self.itemList.remove(item)

    def getChecked(self) -> list[str]:
        return [item.getPath() for item in self.itemList if item.isChecked()]

    def getItems(self) -> list['DirectoryToCheck']:
        return self.itemList

class DirectoryToCheck(QWidget):
    def __init__(self, directory_path, parent):
        super().__init__()

        self.path = directory_path
        self.parent = parent

        layout: QHBoxLayout = QHBoxLayout()
        self.setLayout(layout)

        self.check = QCheckBox()
        self.check.click()
        layout.addWidget(self.check)
        self.check.clicked.connect(self._onClickCheckBox)

        # label to display this items target directory
        self.label = QLabel(self.path)
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.label.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        self.label.mousePressEvent = lambda x: self.check.click()
        layout.addWidget(self.label)

        # button to change this items target directory
        self.btn_pick_directory = QPushButton("Change Directory")
        self.btn_pick_directory.clicked.connect(self._pickDirectory)
        self.btn_pick_directory.setMinimumWidth(115)
        self.btn_pick_directory.setMaximumWidth(self.btn_pick_directory.minimumWidth())
        layout.addWidget(self.btn_pick_directory)

        # button to remove this item
        self.btn_remove = QPushButton("remove")
        self.btn_remove.clicked.connect(self._remove)
        self.btn_remove.setMinimumWidth(65)
        self.btn_remove.setMaximumWidth(self.btn_remove.minimumWidth())
        layout.addWidget(self.btn_remove)

    def _pickDirectory(self):
        directory = QFileDialog.getExistingDirectory()
        if exists(directory):
            self.label.setText(directory)

    def _remove(self):
        self.parent: StartUpWidget
        self.parent.removeDirectory(self)

    def _onClickCheckBox(self):
        self.parent.validate_toggle_btn()

    def isChecked(self):
        return self.check.isChecked()

    def getPath(self):
        return self.label.text()

class StartUpWidget(QWidget):
    def __init__(self, config):
        super().__init__()

        self.config = config
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.itemList = ListContainer()
        layout.addWidget(self.itemList)

        inserter = QWidget()
        inserter_layout = QHBoxLayout()
        inserter.setLayout(inserter_layout)
        layout.addWidget(inserter)

        self.check_uncheck_all_btn = QPushButton("Uncheck All")
        self.check_uncheck_all_btn.clicked.connect(self._toggle_all_entries)
        layout.addWidget(self.check_uncheck_all_btn)
        
        self.inserter_input: QLineEdit = QLineEdit()
        self.inserter_input.setPlaceholderText("input directory to check")
        inserter_layout.addWidget(self.inserter_input)

        inserter_btn_pick = QPushButton("Pick Directory")
        inserter_btn_pick.clicked.connect(self._pickDirectory)
        inserter_layout.addWidget(inserter_btn_pick)

        inserter_btn_add = QPushButton("Add")
        inserter_btn_add.clicked.connect(self._addDirectory)
        inserter_layout.addWidget(inserter_btn_add)

        targets = self.config.get("targets", [])
        for target in targets:
            self.addDirectory(target)
        self.config["targets"] = targets 

        self.setAcceptDrops(True)        

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path_to_file = url.path()[1:]

            if isdir(path_to_file):
                self.addDirectory(path_to_file)

    def _pickDirectory(self):
        directory = QFileDialog.getExistingDirectory()
        self.inserter_input.setText(directory)

    def _addDirectory(self):
        if exists(self.inserter_input.text()):
            self.addDirectory(self.inserter_input.text())

    def addDirectory(self, path: str):
        self.itemList.addDirectory(DirectoryToCheck(path, self))

    def removeDirectory(self, item: DirectoryToCheck):       
        self.itemList.removeDirectory(item)

        # remove target directory from config file
        if item.getPath() in self.config["targets"]:
            self.config["targets"].remove(item.getPath())

    def getList(self) -> list[str]:
        return self.itemList.getChecked()

    def validate_toggle_btn(self) -> None:
        items: list[DirectoryToCheck] = self.itemList.getItems()
        uncheck_all = [item.isChecked() for item in items].count(True) == len(items) 

        if uncheck_all:
            self.check_uncheck_all_btn.setText("Uncheck All")
        else:
            self.check_uncheck_all_btn.setText("Check All")

    def _toggle_all_entries(self) -> None:
        items: list[DirectoryToCheck] = self.itemList.getItems()
        uncheck_all = [item.isChecked() for item in items].count(True) == len(items) 

        if uncheck_all:
            self.check_uncheck_all_btn.setText("Uncheck All")
        else:
            self.check_uncheck_all_btn.setText("Check All")

        for item in items:
            item: DirectoryToCheck
            if item.isChecked() == uncheck_all:
                item.check.click()

