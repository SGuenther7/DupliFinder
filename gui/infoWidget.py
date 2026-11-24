from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout)
from PyQt6.QtCore import Qt

class InfoWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        self.label_targets = QLabel()
        layout.addWidget(self.label_targets)

        self.label_current_state = QLabel()
        layout.addWidget(self.label_current_state)

        self.label_current_loaded_hashes = QLabel()
        layout.addWidget(self.label_current_loaded_hashes)

        self.label_current_added_hashes = QLabel()
        layout.addWidget(self.label_current_added_hashes)

    def updateTargets(self, targets: str) -> None:
        self.label_targets.setText(targets)

    def updateCurrentState(self, current_state: str) -> None:
        self.label_current_state.setText(current_state)        
        
    def updateStatusLoadedHashes(self, current_loaded_hashes: str) -> None:
        self.label_current_loaded_hashes.setText(current_loaded_hashes)

    def updateStatusAddedHashes(self, current_added_hashes: str) -> None:
        self.label_current_added_hashes.setText(current_added_hashes)
