
from PyQt6.QtWidgets import (QMainWindow, QPushButton, QWidget, QLabel,
    QVBoxLayout, QHBoxLayout, QGroupBox, QSizePolicy, QSpinBox)

import json
from gui import (startupWindow, duplicateRemoverWindow)
from os.path import exists
from util import util

class MainWindow(QMainWindow):
    def __init__(self, config_file):
        super().__init__()

        self.setCentralWidget(MainWidget(config_file))
        
class MainWidget(QWidget):
    def __init__(self, config_file):
        super().__init__()

        # reading in config if the file exists
        self.config_file = config_file
        if exists(config_file):
            with open(config_file, "r") as f:
                self.config = json.load(f)
        else:
            self.config = dict()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.startup = startupWindow.StartUpWidget(self.config)
        layout.addWidget(self.startup)

        self.remover = duplicateRemoverWindow.RemoverWidget()
        self.remover.hide()
        layout.addWidget(self.remover)
                
        start_btn = QPushButton("Start")
        start_btn.clicked.connect(self._start)
        layout.addWidget(start_btn)

    def _start(self):

        self.startup.hide()
        directories_to_check = self.startup.getList()

        # getting targets from config
        targets = self.config.get("targets", [])
        for dir in directories_to_check:
            targets.append(dir)
        targets = list(set(targets))
        self.config["targets"] = targets

        # save config with added targets       
        with open(self.config_file, "w") as file:
            json.dump(self.config, file)

        # get name of results file from config
        results_file = self.config.get("results_file", "results.json")

        print(targets)

        print("loading hashes")
        hashes = util.loadCache(results_file)

        print("validating saved hashes")
        hashes = util.validateCache(hashes)
        util.saveCache(hashes, results_file)

        print("calculating new hashes")
        hashes = util.addNewHashes(directories_to_check, hashes)
        util.saveCache(hashes, results_file)

        print("ordering dupes")
        hashes = util.orderDupes(hashes)
        util.saveCache(hashes, results_file)

        dupes = util.getDupes(hashes)

        self.remover.show()
        self.remover.start(dupes)
