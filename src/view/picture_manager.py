from typing import TYPE_CHECKING

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QListWidgetItem, QTreeWidget, QTreeWidgetItem, QAbstractItemView
from PySide6.QtGui import QKeySequence, QShortcut, QTextCursor, QTextCharFormat, QFont

from ui_compiled.Ui_picture_manager import Ui_MainWindow
from controller.picture_manager import PictureManagerController

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    def setup_controller(self, controller: PictureManagerController):
        self.controller = controller
        self.bind()
        
    def bind(self):
        # install event filter
        self.searchTagTreeTextEdit.installEventFilter(self)

        # tag tree item click event
        self.characterTagTree.itemClicked.connect(self.controller.add_include_tag)
        self.attributeTagTree.itemClicked.connect(self.controller.add_include_tag)
        self.characterTagTree.itemDoubleClicked.connect(self.controller.add_exclude_tag)
        self.attributeTagTree.itemDoubleClicked.connect(self.controller.add_exclude_tag)

    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        # Filter for tag_search_edit, implement enter to search tag
        if (source == self.searchTagTreeTextEdit and event.type() == QEvent.Type.KeyPress):
            if event.key() == Qt.Key.Key_Return:
                self.controller.tag_search(self.searchTagTreeTextEdit.toPlainText())
                return True
        
        return super().eventFilter(source, event)