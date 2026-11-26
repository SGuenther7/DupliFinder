
from PyQt6.QtWidgets import QApplication
from gui import mainWindow

CURRENT_VERSION = "v1.0"

def showApp(config_file: str) -> None:
    app = QApplication([])

    window = mainWindow.MainWindow(config_file)
    window.resize(800, 500)
    window.setWindowTitle(f"DupliChecker {CURRENT_VERSION}")
    window.show()

    app.exec()

def start() -> None:

    showApp("./data/config.json")
    # showApp("./data/config-TEST.json")

if __name__ == "__main__":
    start()
