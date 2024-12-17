from PySide6.QtWidgets import QApplication

from view.picture_manager import MainWindow
from controller.picture_manager import PictureManagerController as Controller
from tools.log import Log

if __name__ == "__main__":
    Log.init()
    app = QApplication([])
    window = MainWindow()
    controller = Controller(window)
    window.show()
    app.exec()