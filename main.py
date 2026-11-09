
import math

from PyQt6.QtWidgets import QApplication
from gui import mainWindow
from util import util

targets = []
targets = ["C:/Users/Mister P/Downloads/p","D:/p", "F:/p", "H:/p", "M:/DL", "M:/p"]
# targets = targets[:-2]

results_file = "results.json"

display_filter = ["jpg","jpeg", "png"]


def showApp(config_file: str) -> None:
    app = QApplication([])

    window = mainWindow.MainWindow(config_file)
    window.setMinimumSize(800,800)
    window.setWindowTitle("DupliChecker")
    window.show()

    app.exec()

def start() -> None:

    showApp("config.json")
    return

    print(targets)

    print("loading hashes")
    hashes = loadCache(results_file)

    print("validating saved hashes")
    hashes = validateCache(hashes)
    saveCache(hashes, results_file)

    # print("calculating new hashes")
    # hashes = addNewHashes(targets, hashes)
    # saveCache(hashes, results_file)

    print("ordering dupes")
    hashes = orderDupes(hashes)
    saveCache(hashes, results_file)

    # displayDupes(hashes, display_filter, 250_000_000)
    # displayDupes(hashes, display_filter, 0)

    dupes = getDupes(hashes)

    print("starting duplicate remover GUI")
    showApp(dupes)

if __name__ == "__main__":
    start()
