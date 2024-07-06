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
        self.initVariables()
        self.bind()
        self.loadTagTree()
        self.loadNewTag()
        
    def initVariables(self):
        self.viewTreeLastSearch = ""
        self.viewTreeSearchIndex = 0
        self.viewTreeSearchList = []
        self.mainTreeLastSearch = ""
        self.mainTreeSearchIndex = 0
        self.mainTreeSearchList = []
        
    def bind(self):
        """
        Binds various event handlers and connects signals to slots.

        This method is responsible for setting up the connections between different UI elements and their corresponding
        event handlers or slots. It also installs event filters and sets up keyboard shortcuts.

        Returns:
            None
        """
        # Connect the scrollbar between new_tag_orignal_lst and new_tag_store_lst
        self.newTagOrignalList.verticalScrollBar().valueChanged.connect(
            self.newTagTranslList.verticalScrollBar().setValue)
        self.newTagTranslList.verticalScrollBar().valueChanged.connect(
            self.newTagOrignalList.verticalScrollBar().setValue)
        
        # show tag info when a tag is selected
        self.viewTree.itemSelectionChanged.connect(self.showTagInfo)
        self.mainTree.itemSelectionChanged.connect(self.showTagInfo)

        # install event filter for new_tag_input and new_tag_orignal_lst
        self.newTagInput.installEventFilter(self)
        self.newTagOrignalList.installEventFilter(self)
        self.viewTreeSearchEdit.installEventFilter(self)
        self.mainTreeSearchEdit.installEventFilter(self)

        # Connect the save shortcut
        self.saveShortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.saveShortcut.activated.connect(self.saveTree)

        # double click to edit item in new_tag_transl_lst
        self.newTagTranslList.itemDoubleClicked.connect(self.newTagTranslList.editItem)

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
        
        # Filter for new_tag_orignal_lst, implement copy without '#' at the beginning
        elif (source == self.newTagOrignalList and event.type() == QEvent.Type.KeyPress):
            if event.matches(QKeySequence.Copy):
                text = self.newTagOrignalList.currentItem().text()
                QApplication.clipboard().setText(text[1:])
                return True
        
        # Filter for view_tree_search_edit, implement search function
        elif (source == self.viewTreeSearchEdit and event.type() == QEvent.Type.KeyPress):
            if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
                self.viewTreeLastSearch, self.viewTreeSearchIndex, self.viewTreeSearchList = \
                    self.searchTree(
                        self.viewTree, 
                        self.viewTreeSearchEdit, 
                        self.viewTreeLastSearch, 
                        self.viewTreeSearchIndex, 
                        self.viewTreeSearchList
                    )
                return True

        # Filter for main_tree_search_edit, implement search function
        elif (source == self.mainTreeSearchEdit and event.type() == QEvent.Type.KeyPress):
            if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
                self.mainTreeLastSearch, self.mainTreeSearchIndex, self.mainTreeSearchList = \
                    self.searchTree(
                        self.mainTree, 
                        self.mainTreeSearchEdit, 
                        self.mainTreeLastSearch, 
                        self.mainTreeSearchIndex, 
                        self.mainTreeSearchList
                    )
                return True
        
        return super().eventFilter(source, event)
    
    def searchTree(self, tree: QTreeWidget, searchEdit: QTextEdit, lastSearch: str, searchIndex: int, searchList: list):
        """search the tree widget"""
        searchText = searchEdit.toPlainText()
        if searchText == lastSearch:
            if searchList:
                if searchIndex < len(searchList):
                    tree.setCurrentItem(searchList[searchIndex])
                    tree.scrollToItem(searchList[searchIndex])
                    searchIndex += 1
                else:
                    searchIndex = 0
                    tree.setCurrentItem(searchList[searchIndex])
                    tree.scrollToItem(searchList[searchIndex])
        else:
            searchList = tree.findItems(searchText, Qt.MatchFlag.MatchContains | Qt.MatchFlag.MatchRecursive)
            searchIndex = 0
            lastSearch = searchText
            if searchList:
                tree.setCurrentItem(searchList[searchIndex])
                tree.scrollToItem(searchList[searchIndex])
                searchIndex += 1
        return lastSearch, searchIndex, searchList
    
    def loadTagTree(self):
        """load tag tree from tag_tree.json and show it in the tree widget"""
        self.tagTree = dataFn.loadTagTree() # load tag tree from tag_tree.json

        self.viewTree.addTopLevelItem(self.tagTree.toTreeWidgetItem())

        self.mainTree.setTagTree(self.tagTree)
        self.mainTree.setOutputBox(self.outputTextEdit)
        self.mainTree.setListWidgets(self.newTagOrignalList, self.newTagTranslList, self.newTagStoreList)
        self.mainTree.setCheckBox(self.tagMovingCheckBox)
        self.mainTree.setViewTree(self.viewTree)
        
        # expand the tree widget
        self.viewTree.expandItem(self.viewTree.topLevelItem(0))
        for i in range(self.viewTree.topLevelItem(0).childCount()):
            self.viewTree.expandItem(self.viewTree.topLevelItem(0).child(i))
        self.mainTree.expandItem(self.mainTree.topLevelItem(0))
        for i in range(self.mainTree.topLevelItem(0).childCount()):
            self.mainTree.expandItem(self.mainTree.topLevelItem(0).child(i))
    
    def reloadViewTree(self):
        """reload the view tree"""
        self.viewTree.clear()
        self.viewTree.addTopLevelItem(self.tagTree.toTreeWidgetItem())

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
            self.newTagOrignalList.addItem(tagPair[0])
            newTraslItem = QListWidgetItem(tagPair[1])
            newTraslItem.setFlags(newTraslItem.flags() | Qt.ItemIsEditable) # make the item editable
            self.newTagTranslList.addItem(newTraslItem)
            newTagCount += 1
        
        self.outputTextEdit.append(f"new tag loaded, {newTagCount} tags in total")
        self.mainTree.setNewTagLst(self.newTagLst) # pass newTagLst to main_tree to record which tags are added

    def showTagInfo(self):
        """show the tag info of the selected tag in the tag tree widget"""
        # Get the currently selected item
        currentItem = self.sender().currentItem()
        if currentItem is None:
            return

        tagName = currentItem.text(0)
        tag = self.tagTree.tagDict[tagName]
        if not tag.isTag:
            self.tagInfo.setText(f"类: {tag.name}\n"
                                 f"子标签:\n{', '.join(tag.subTags.keys())}\n"
                                )
            return
        
        # Show the tag info in the tag info text edit
        self.tagInfo.setText(f"标签名: {tag.name}\n"
                             f"同义标签:\n{', '.join(tag.synonyms)}\n"
                             f"父标签:\n{', '.join(tag.parent)}\n"
                             f"子标签:\n{', '.join(tag.subTags.keys())}\n"
                            )

    def saveTree(self):
        dataFn.writeJson(self.tagTree.toDict(), "tag_tree.json")
        dataFn.writeJson(self.newTagLst, "new_tag.json")
        self.outputTextEdit.append("标签树已保存")
        return

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()