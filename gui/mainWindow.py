
from PyQt6.QtWidgets import (QMainWindow, QPushButton, QWidget, QVBoxLayout, QApplication)
from os.path import exists

import json
from gui import (duplicateRemoverWidget, startupWidget, infoWidget)
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

        self.startup = startupWidget.StartUpWidget(self.config)
        layout.addWidget(self.startup)

        self.infoWidget = infoWidget.InfoWidget()
        self.infoWidget.hide()
        layout.addWidget(self.infoWidget)

        self.remover = duplicateRemoverWidget.RemoverWidget()
        self.remover.hide()
        layout.addWidget(self.remover)
                
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self._start)
        layout.addWidget(self.start_btn)

        self.results_file = self.config.get("results_file", "results.json")
        # self.results_file = self.config.get("results_file", "results-TEST.json")
        self.hashes = dict()
        self.dupes = dict()

        app = QApplication.instance()
        for i in range(0, 100):
            app.processEvents()

        self.resize(self.minimumSizeHint())

    def _start(self):
        self.start_btn.hide()
        self.startup.hide()
        self.infoWidget.show()

        self.work()
        
        self.infoWidget.hide()
        self.remover.show()
        self.remover.start(self.dupes)

    def work(self):
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

        self.infoWidget.updateTargets(f"targets: {targets}")

        self.infoWidget.updateCurrentState("loading hashes")
        self.hashes = util.loadCache(self.results_file)

        self._validateCache()

        self._addingHashes(directories_to_check)

        self.hashes = util.orderDupes(self.hashes)
        util.saveCache(self.hashes, self.results_file)

        # get only duplicates
        self.dupes = util.getDupes(self.hashes)

    def _validateCache(self):
        self.infoWidget.updateCurrentState("validating saved hashes")

        data = util.validateCache(self.hashes)
        app = QApplication.instance()

        for updated_hashes, current_status_str in data:
            self.infoWidget.updateStatusLoadedHashes(current_status_str)
            self.hashes = updated_hashes
    
            # process event loop to prevent freezing
            for i in range(0, 10):
                app.processEvents()

        util.saveCache(self.hashes, self.results_file)

    def _addingHashes(self, directories_to_check):
        self.infoWidget.updateCurrentState("calculating new hashes")

        data = util.addNewHashes(directories_to_check, self.hashes, self.results_file)
        app = QApplication.instance()

        for (updated_hashes, current_status_str) in data:
            self.infoWidget.updateStatusAddedHashes(current_status_str)
            self.hashes = updated_hashes
            
            # process event loop to prevent freezing
            for i in range(0, 10):
                app.processEvents()

        util.saveCache(self.hashes, self.results_file)
