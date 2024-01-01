from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QTextEdit

from Ui_tag_tree_management import Ui_MainWindow

import program_objects as progObjs
import pic_data_functions as dataFn

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.bind()
        self.loadTagTree()
        self.loadNewTag()

        self.new_tag_input.installEventFilter(self) # install event filter to new_tag_input

    def bind(self):
        # Connect the scrollbar between new_tag_orignal_lst and new_tag_store_lst
        self.new_tag_orignal_lst.verticalScrollBar().valueChanged.connect(
            self.new_tag_transl_lst.verticalScrollBar().setValue)
        self.new_tag_transl_lst.verticalScrollBar().valueChanged.connect(
            self.new_tag_orignal_lst.verticalScrollBar().setValue)
        
        # show tag info when a tag is selected
        self.view_tree.itemSelectionChanged.connect(self.showTagInfo)
        self.main_tree.itemSelectionChanged.connect(self.showTagInfo)

    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        if (source == self.new_tag_input and event.type() == QEvent.KeyPress):
            if event.key() == Qt.Key_Tab:
                text = self.new_tag_input.toPlainText()
                if text.startswith('#'):
                    self.new_tag_input.setPlainText(text[1:])
                else:
                    self.new_tag_input.setPlainText('#' + text)
                return True
            elif event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
                item = QListWidgetItem(self.new_tag_input.toPlainText())
                self.new_tag_store_lst.addItem(item)
                self.new_tag_input.clear()
                return True
        return super().eventFilter(source, event)
        
    def loadTagTree(self):
        """load tag tree from tag_tree.json and show it in the tree widget"""
        self.tagTree = dataFn.loadTagTree() # load tag tree from tag_tree.json
        # these widgets uses different widget item, so it needs synchronization after modified
        self.view_tree.addTopLevelItem(self.tagTree.toTreeWidgetItem())
        self.main_tree.addTopLevelItem(self.tagTree.toTreeWidgetItem())

    def loadNewTag(self):
        """load new tag file and show it in the new tag lst"""
        self.newTagLst = dataFn.loadJson("new_tag.json")
        for tagPair in self.newTagLst:
            self.new_tag_orignal_lst.addItem(tagPair[0])
            self.new_tag_transl_lst.addItem(tagPair[1])

    def showTagInfo(self):
        """show the tag info of the selected tag in the tag tree widget"""
        # Get the currently selected item
        current_item = self.sender().currentItem()

        # If no item is selected, do nothing
        if current_item is None:
            return

        # Get the tag name of the currently selected item
        tagName = current_item.text(0)
        tag = self.tagTree.tagDict[tagName]

        # If the selected item is not a tag, do nothing
        if not tag.isTag:
            return
        
        # Show the tag info in the tag info text edit
        self.tag_info.setText(f"Tag name: {tag.name}\n"
                              f"Parent tags: {', '.join(tag.parent)}\n"
                              f"Sub tags: {', '.join(tag.subTags.keys())}\n"
                              f"Synonyms: {', '.join(tag.synonyms)}\n")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()