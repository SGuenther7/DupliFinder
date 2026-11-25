
from PyQt6.QtWidgets import QApplication
from gui import mainWindow


def showApp(config_file: str) -> None:
    app = QApplication([])

    window = mainWindow.MainWindow(config_file)
    window.setMinimumSize(800, 500)
    window.setWindowTitle("DupliChecker")
    window.show()

    app.exec()

def start() -> None:

    showApp("./data/config.json")
    # showApp("./data/config-TEST.json")

if __name__ == "__main__":
    start()
