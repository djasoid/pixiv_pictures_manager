from view.tag_management import MainWindow

from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    tag_tree_path = "tag_tree.json"
    new_tag_path = "new_tag.json"
    app = QApplication([])
    window = MainWindow(tag_tree_path, new_tag_path)
    window.show()
    app.exec()