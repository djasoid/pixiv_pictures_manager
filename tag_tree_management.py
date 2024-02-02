from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QListWidgetItem, QTreeWidget, QAbstractItemView, QDialog
from PySide6.QtGui import QKeySequence, QShortcut

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

    def bind(self):
        # Connect the scrollbar between new_tag_orignal_lst and new_tag_store_lst
        self.new_tag_orignal_lst.verticalScrollBar().valueChanged.connect(
            self.new_tag_transl_lst.verticalScrollBar().setValue)
        self.new_tag_transl_lst.verticalScrollBar().valueChanged.connect(
            self.new_tag_orignal_lst.verticalScrollBar().setValue)
        
        # show tag info when a tag is selected
        self.view_tree.itemSelectionChanged.connect(self.showTagInfo)
        self.main_tree.itemSelectionChanged.connect(self.showTagInfo)

        # install event filter for new_tag_input and new_tag_orignal_lst
        self.new_tag_input.installEventFilter(self)
        self.new_tag_orignal_lst.installEventFilter(self)

        # Connect the save shortcut
        self.saveShortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.saveShortcut.activated.connect(self.saveTree)

        # double click to edit item in new_tag_transl_lst
        self.new_tag_transl_lst.itemDoubleClicked.connect(self.new_tag_transl_lst.editItem)

    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        # Filter for new_tag_input, implement tab to add '#' and enter to add tag
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
        # Filter for new_tag_orignal_lst, implement copy without '#' at the beginning
        elif (source == self.new_tag_orignal_lst and event.type() == QEvent.KeyPress):
            if event.matches(QKeySequence.Copy):
                text = self.new_tag_orignal_lst.currentItem().text()
                QApplication.clipboard().setText(text[1:])
                return True

        return super().eventFilter(source, event)
        
    def loadTagTree(self):
        """load tag tree from tag_tree.json and show it in the tree widget"""
        self.tagTree = dataFn.loadTagTree() # load tag tree from tag_tree.json

        self.view_tree.addTopLevelItem(self.tagTree.toTreeWidgetItem())

        self.main_tree.setTagTree(self.tagTree)
        self.main_tree.setOutputBox(self.output_text)
        self.main_tree.setListWidgets(self.new_tag_orignal_lst, self.new_tag_transl_lst, self.new_tag_store_lst)
    
    def reloadViewTree(self):
        """reload the view tree"""
        self.view_tree.clear()
        self.view_tree.addTopLevelItem(self.tagTree.toTreeWidgetItem())

    def loadNewTag(self):
        """load new tag file and show it in the new tag lst"""
        self.newTagLst = dataFn.loadJson("new_tag.json")
        newTagCount = 0
        for tagPair in self.newTagLst:
            if len(tagPair) > 2: # if the tag has been added to the tag tree, pass it
                continue
            if self.tagTree.isInTree(tagPair[0]): # if the tag is exist in tag tree, pass it
                if len(tagPair) == 2:
                    tagPair.append("added")
                continue
            self.new_tag_orignal_lst.addItem(tagPair[0])
            new_trasl_item = QListWidgetItem(tagPair[1])
            new_trasl_item.setFlags(new_trasl_item.flags() | Qt.ItemIsEditable) # make the item editable
            self.new_tag_transl_lst.addItem(new_trasl_item)
            newTagCount += 1
        
        self.output_text.append(f"new tag loaded, {newTagCount} tags in total")
        self.main_tree.setNewTagLst(self.newTagLst) # pass newTagLst to main_tree to record which tags are added

    def showTagInfo(self):
        """show the tag info of the selected tag in the tag tree widget"""
        # Get the currently selected item
        currentItem = self.sender().currentItem()
        if currentItem is None:
            return

        tagName = currentItem.text(0)
        tag = self.tagTree.tagDict[tagName]
        if not tag.isTag:
            self.tag_info.clear()
            return
        
        # Show the tag info in the tag info text edit
        self.tag_info.setText(f"标签名: {tag.name}\n"
                              f"同义标签:\n{', '.join(tag.synonyms)}\n"
                              f"父标签:\n{', '.join(tag.parent)}\n"
                              f"子标签:\n{', '.join(tag.subTags.keys())}\n")

    def saveTree(self):
        dataFn.writeJson(self.tagTree.toDict(), "tag_tree.json")
        dataFn.writeJson(self.newTagLst, "new_tag.json")
        self.output_text.append("标签树已保存")
        return

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()