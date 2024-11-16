from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QListWidgetItem, QTreeWidget, QTreeWidgetItem, QAbstractItemView
from PySide6.QtGui import QKeySequence, QShortcut, QTextCursor, QTextCharFormat, QFont

from ui_compiled.Ui_tag_tree_management import Ui_MainWindow
from controller.tag_management import TagManagementController as Controller

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    def setup_controller(self, controller: Controller):
        self.controller = controller
        self.mainTree.set_controller(controller)
        self.bind()
        
    def bind(self):
        """
        Binds various event handlers and connects signals to slots.

        This method is responsible for setting up the connections between different UI elements and their corresponding
        event handlers or slots. It also installs event filters and sets up keyboard shortcuts.

        Returns:
            None
        """
        # Connect the scrollbar between new_tag_original_lst and new_tag_store_lst
        self.newTagOriginalList.verticalScrollBar().valueChanged.connect(
            self.newTagTranslList.verticalScrollBar().setValue)
        self.newTagTranslList.verticalScrollBar().valueChanged.connect(
            self.newTagOriginalList.verticalScrollBar().setValue)
        
        # show tag info when a tag is selected
        self.viewTree.itemSelectionChanged.connect(self.show_tag_info)
        self.mainTree.itemSelectionChanged.connect(self.show_tag_info)

        # install event filter
        self.newTagInput.installEventFilter(self)
        self.newTagOriginalList.installEventFilter(self)
        self.viewTreeSearchEdit.installEventFilter(self)
        self.mainTreeSearchEdit.installEventFilter(self)

        # Connect the save shortcut
        self.save_shortcut = QShortcut(QKeySequence.StandardKey.Save, self)
        self.save_shortcut.activated.connect(self.controller.save_tree)

        # double click to edit item in new_tag_transl_lst
        self.newTagTranslList.itemDoubleClicked.connect(self.newTagTranslList.editItem)
        
        # Connect undo
        self.undo_shortcut = QShortcut(QKeySequence.StandardKey.Undo, self)
        self.undo_shortcut.activated.connect(self.controller.undo)

    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        # Filter for new_tag_input, implement tab to add '#' and enter to add tag
        if (source == self.newTagInput and event.type() == QEvent.Type.KeyPress):
            if event.key() == Qt.Key.Key_Tab:
                text = self.newTagInput.toPlainText()
                if text.startswith('#'):
                    self.newTagInput.setPlainText(text[1:])
                else:
                    self.newTagInput.setPlainText('#' + text)
                return True
            elif event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
                item = QListWidgetItem(self.newTagInput.toPlainText())
                self.newTagStoreList.addItem(item)
                self.newTagInput.clear()
                return True
        
        # Filter for new_tag_original_lst, implement copy without '#' at the beginning
        elif (source == self.newTagOriginalList and event.type() == QEvent.Type.KeyPress):
            if event.matches(QKeySequence.Copy):
                text = self.newTagOriginalList.currentItem().text()
                QApplication.clipboard().setText(text[1:])
                return True
        
        # Filter for view_tree_search_edit, implement search function
        elif (source == self.viewTreeSearchEdit and event.type() == QEvent.Type.KeyPress):
            if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
                self.controller.search_tree(
                    self.viewTree, 
                    self.viewTreeSearchEdit, 
                )
                return True

        # Filter for main_tree_search_edit, implement search function
        elif (source == self.mainTreeSearchEdit and event.type() == QEvent.Type.KeyPress):
            if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
                self.controller.search_tree(
                    self.mainTree, 
                    self.mainTreeSearchEdit, 
                )
                return True
        
        return super().eventFilter(source, event)
    
    def show_tag_info(self):
        current_item = self.sender().currentItem()
        if current_item is None:
            return
        self.controller.show_tag_info(current_item)
