from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QListWidgetItem, QTreeWidget, QTreeWidgetItem, QAbstractItemView
from PySide6.QtGui import QKeySequence, QShortcut, QTextCursor, QTextCharFormat, QFont

from Ui_tag_tree_management import Ui_MainWindow

import data as dataFn
from tag_tree import Tag

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initTreeSearch()
        self.bind()
        self.loadTagTree()
        self.loadNewTag()
        self.setMainTreeRef()
        self.expandTopLevel()
        
    def initTreeSearch(self):
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
        self.saveShortcut = QShortcut(QKeySequence.StandardKey.Save, self)
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
    
    def searchTree(
            self, 
            tree: QTreeWidget, 
            searchEdit: QTextEdit, 
            lastSearch: str, 
            searchIndex: int, 
            searchList: list[QTreeWidgetItem]
        ):
        """search the tree widget"""
        def expandAndScrollToItem(item: QTreeWidgetItem):
            """expand the tree widget and scroll to the item"""
            parent = item.parent()
            while parent:
                parent.setExpanded(True)
                parent = parent.parent()
            tree.scrollToItem(item, QAbstractItemView.ScrollHint.PositionAtCenter)
            tree.setCurrentItem(item)
            
        searchText = searchEdit.toPlainText()
        if searchText == lastSearch and searchList:
            if searchIndex < len(searchList):
                expandAndScrollToItem(searchList[searchIndex])
                searchIndex += 1
            else:
                searchIndex = 0
                expandAndScrollToItem(searchList[searchIndex])
        else:
            searchList = tree.findItems(searchText, Qt.MatchFlag.MatchContains | Qt.MatchFlag.MatchRecursive)
            searchIndex = 0
            lastSearch = searchText
            if searchList:
                expandAndScrollToItem(searchList[searchIndex])
                searchIndex += 1
                
        return lastSearch, searchIndex, searchList
    
    def getTreeItem(self, tag: Tag) -> QTreeWidgetItem:
        item = QTreeWidgetItem([tag.name])
        for subTag in tag.subTags.values():
            item.addChild(self.getTreeItem(subTag))
        return item
    
    def loadTagTree(self):
        """load tag tree from tag_tree.json and show it in the tree widget"""
        self.tagTree = dataFn.loadTagTree()
        self.viewTree.addTopLevelItem(self.getTreeItem(self.tagTree.root))
        self.mainTree.addTopLevelItem(self.getTreeItem(self.tagTree.root))
        
    def setMainTreeRef(self):
        self.mainTree.setTagTree(self.tagTree)
        self.mainTree.setOutputBox(self.outputTextEdit)
        self.mainTree.setListWidgets(self.newTagOrignalList, self.newTagTranslList, self.newTagStoreList)
        self.mainTree.setCheckBox(self.tagMovingCheckBox)
        self.mainTree.setViewTree(self.viewTree)
        self.mainTree.setNewTagLst(self.newTagLst)
        
    def expandTopLevel(self):
        self.viewTree.expandItem(self.viewTree.topLevelItem(0))
        for i in range(self.viewTree.topLevelItem(0).childCount()):
            self.viewTree.expandItem(self.viewTree.topLevelItem(0).child(i))
        self.mainTree.expandItem(self.mainTree.topLevelItem(0))
        for i in range(self.mainTree.topLevelItem(0).childCount()):
            self.mainTree.expandItem(self.mainTree.topLevelItem(0).child(i))

    def loadNewTag(self):
        """load new tag file and show it in the new tag lst"""
        self.newTagLst = dataFn.loadJson("new_tag.json")
        newTagCount = 0
        for tagPair in self.newTagLst:
            if len(tagPair) > 2: # if the tag has been added to the tag tree, pass it
                continue
            if self.tagTree.isInTree(tagPair[0]):
                if len(tagPair) == 2:
                    tagPair.append("added")
                continue
            self.newTagOrignalList.addItem(tagPair[0])
            newTraslItem = QListWidgetItem(tagPair[1])
            newTraslItem.setFlags(newTraslItem.flags() | Qt.ItemFlag.ItemIsEditable)
            self.newTagTranslList.addItem(newTraslItem)
            newTagCount += 1
        
        self.outputTextEdit.append(f"new tag loaded, {newTagCount} tags in total")

    def showTagInfo(self):
        """show the tag info of the selected tag in the tag tree widget"""
        currentItem = self.sender().currentItem()
        if currentItem is None:
            return
    
        tagName = currentItem.text(0)
        tag = self.tagTree.tagDict[tagName]
        
        self.tagInfo.clear()
    
        if not tag.isTag:
            self.tagInfo.append("<b>类:</b> " + tag.name)
            self.tagInfo.append("<b>子标签:</b>")
            self.tagInfo.append(", ".join(tag.subTags.keys()))
        else:
            items = [
                ("标签名: ", tag.name),
                ("标签类型: ", tag.tagType),
                ("同义标签: ", ", ".join(tag.synonyms)),
                ("父标签: ", ", ".join(tag.parent)),
                ("子标签: ", ", ".join(tag.subTags.keys()))
            ]
            for label, content in items:
                self.tagInfo.append(f"<b>{label}</b>{content}")
    
        self.tagInfo.verticalScrollBar().setValue(0)
    
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