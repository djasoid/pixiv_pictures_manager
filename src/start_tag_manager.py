from PySide6.QtWidgets import QApplication

from view.tag_management import MainWindow
from controller.tag_management import TagManagementController as Controller
from tools.log import Log

if __name__ == "__main__":
    tag_tree_path = "tag_tree.json"
    new_tag_path = "new_tag.json"
    Log.init()
    app = QApplication([])
    window = MainWindow()
    controller = Controller(window, tag_tree_path, new_tag_path)
    window.show()
    app.exec()