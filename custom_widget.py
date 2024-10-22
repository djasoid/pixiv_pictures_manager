from PySide6.QtWidgets import QTextEdit, QTreeWidget, QTreeWidgetItem, QListWidget, QMenu, QDialog, QCheckBox
from PySide6.QtGui import QContextMenuEvent, QFont, QAction
from PySide6.QtCore import QByteArray, Qt

from Ui_delete_tag_dialog import Ui_delete_tag_dialog
from Ui_synonym_edit_dialog import Ui_synonym_edit_dialog

import tag_tree as tree
import data as dataFn

class DeleteDialog(QDialog, Ui_delete_tag_dialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
    
    def setContent(self, tagName, parentTagName):
        self.deleteInfoLabel.setText(f"确认从 {parentTagName} 删除 {tagName} ?")
    
    def accept(self):
        super().accept()
    
    def reject(self):
        super().reject()

class SynonymEditDialog(QDialog, Ui_synonym_edit_dialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def setContent(self, tagName: str, synonyms: set, enName: str):
        self.setWindowTitle(f"编辑同义标签：{tagName}")
        self.synonymTextEdit.setPlainText("\n".join(synonyms))
        self.englishNameEdit.setPlainText(enName)

    def accept(self):
        super().accept()
    
    def reject(self):
        super().reject()

# Customized QTreeWidget for tag tree
class MainTagTreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.history = []
        self.addedFont = QFont()
        self.deleteTagDialog = DeleteDialog(self)
        self.synonymEditDialog = SynonymEditDialog(self)

    def setTagTree(self, tagTree: tree.TagTree):
        self.tagTree = tagTree
        self.addTopLevelItem(tagTree.toTreeWidgetItem())
        
    def setViewTree(self, viewTree: QTreeWidget):
        self.viewTree = viewTree

    def setOutputBox(self, outputBox: QTextEdit): # pass output_box to show output
        self.outputBox = outputBox

    def setNewTagLst(self, newTagLst: list): # pass newTagLst to record which tags are added
        self.newTagLst = newTagLst
    
    def setListWidgets(self, newTagOrignalList: QListWidget, newTagTranslList: QListWidget, newTagStoreList: QListWidget):
        self.newTagOrignalList = newTagOrignalList
        self.newTagTranslList = newTagTranslList
        self.newTagStoreList = newTagStoreList

    def setCheckBox(self, tagMovingCheckBox: QCheckBox):
        self.tagMovingCheckBox = tagMovingCheckBox

    def dropEvent(self, event):
        """handle drop event and make changes to the tag tree"""
        targetItem = self.itemAt(event.position().toPoint()) # get the item at the drop position
        if targetItem is None: # if the drop position is not on an item, do nothing
            return
        
        targetTag = targetItem.text(0)
        
        source = event.source().objectName()

        if source == "viewTree": # get the tag name from the source
            dragTagItem = event.source().currentItem()
            dragTagSourceItem = dragTagItem.parent()
            dragTagSource = dragTagSourceItem.text(0)
            dragTag = dragTagItem.text(0)
        else:
            dragTag = event.source().currentItem().text()

        self.history.append(({source}, {dragTag}, {targetTag})) # record the operation

        if source == "viewTree": # copy and move operation
            if dragTag == targetTag:
                self.outputBox.append("不能将标签移动到自身")
            else:
                if self.tagMovingCheckBox.isChecked():
                    self.editTree("move",
                                    dragTag,
                                    targetTag,
                                    source = dragTagSource,
                                    sourceItem=dragTagSourceItem,
                                    parentItem=targetItem,
                                    subItem=dragTagItem)
                else:
                    self.editTree("add_parent", dragTag, targetTag, parentItem=targetItem)


        elif source == "newTagStoreList": # add operation
            self.editTree("add_new", dragTag, targetTag, parentItem=targetItem)
            self.markAdded(dragTag, True)

        elif source == "newTagOrignalList":
            self.editTree("add_synonym", dragTag, targetTag)
            self.markAdded(dragTag, True)

        elif source == "newTagTranslList": # add operation
            self.editTree("add_new", dragTag, targetTag, parentItem=targetItem)
            originalTag = self.newTagOrignalList.item(self.newTagTranslList.row(event.source().currentItem())).text()
            self.editTree("add_synonym", originalTag, dragTag)
            self.markAdded(dragTag, False)
        
    def editTree(self, operation, 
                 sub: str, parent: str, 
                 subItem: QTreeWidgetItem = None, 
                 parentItem: QTreeWidgetItem = None, 
                 sourceItem: QTreeWidgetItem = None,
                 source: str = None):
        """edit the tag tree with the given operation, sync the view tree and the tag tree, and show the operation in the output box"""

        if operation == "add_new": # add new tag
            # add the new tag to the tag tree
            self.tagTree.addNewTag(sub, parent)
            # sync the view tree and main tree
            parentItem.addChild(QTreeWidgetItem([sub]))
            viewParentItem = self.getCorrespondingTreeItem(parentItem, self.viewTree)
            viewParentItem.addChild(QTreeWidgetItem([sub]))
            # show the operation in the output box
            self.outputBox.append(f"添加新标签 {sub} 到 {parent}")
            return

        elif operation == "add_parent": # add parent tag
            # add the parent tag to the tag
            self.tagTree.addParentTag(sub, parent)
            # sync the view tree and main tree
            parentItem.addChild(QTreeWidgetItem([sub]))
            viewParentItem = self.getCorrespondingTreeItem(parentItem, self.viewTree)
            viewParentItem.addChild(QTreeWidgetItem([sub]))
            # show the operation in the output box
            self.outputBox.append(f"标签 {sub} 添加至 {parent}下")
            return

        elif operation == "add_synonym": # add synonym
            self.tagTree.tagDict[parent].addSynonym(sub)
            self.outputBox.append(f"同义标签 {sub} 添加至 {parent}")
            return

        elif operation == "del": # delete tag
            self.tagTree.deleteTag(sub, parent)
            viewParentItem = self.getCorrespondingTreeItem(parentItem, self.viewTree)
            viewParentItem.removeChild(self.getCorrespondingTreeItem(subItem, self.viewTree))
            parentItem.removeChild(subItem)
            self.outputBox.append(f"标签 {sub} 从 {parent} 删除")
            return
        
        elif operation == "move":
            self.tagTree.addParentTag(sub, parent)
            self.tagTree.deleteTag(sub, source)

            mainTreeSourceItem = self.getCorrespondingTreeItem(sourceItem, self)
            mainTreeSubItem = self.getCorrespondingTreeItem(subItem, self)
            viewTreeParentItem = self.getCorrespondingTreeItem(parentItem, self.viewTree)
            parentItem.addChild(mainTreeSubItem.clone()) # parentItem is from the main tree  
            viewTreeParentItem.addChild(subItem.clone())
            mainTreeSourceItem.removeChild(mainTreeSubItem)
            sourceItem.removeChild(subItem) # sourceItem and subItem is from the view tree
            self.outputBox.append(f"标签 {sub} 从 {source} 移动至 {parent}")
            return
        else:
            return

    def getCorrespondingTreeItem(self, sourceItem: QTreeWidgetItem, targetTree: QTreeWidget) -> QTreeWidgetItem:
        """
        Retrieves the corresponding tree item in the target tree for a given source tree item.

        Args:
            sourceItem (QTreeWidgetItem): The source tree item for which to find the corresponding target tree item.
            sourceTree (QTreeWidget): The tree widget of the source item.
            targetTree (QTreeWidget): The target tree widget where the corresponding item is to be found.

        Returns:
            QTreeWidgetItem: The corresponding tree item in the target tree.
        """
        index = []
        pItem = sourceItem.parent()
        while pItem:
            index.append(pItem.indexOfChild(sourceItem))
            sourceItem = pItem
            pItem = sourceItem.parent()
        index.reverse()
        targetItem = targetTree.topLevelItem(0)
        for i in index:
                targetItem = targetItem.child(i)
        return targetItem

    def markAdded(self, tag: str, orignal: bool):
        """mark the tag as added to the tag tree"""
        if orignal:
            # set the font of the orignal tag to gray
            orignalItems = self.newTagOrignalList.findItems(tag, Qt.MatchExactly)
            if orignalItems:
                orignalItem = orignalItems[0]
                orignalItem.setForeground(Qt.gray)
            else:
                return
            

            # mark the tag in the new tag list as added
            for tagPair in self.newTagLst:
                if tagPair[0] == tag:
                    tagPair.append("added")
                    return
                
        else:
            # set the font of the transl tag and the orignal tag to gray
            translItem = self.newTagTranslList.findItems(tag, Qt.MatchExactly)[0]
            orignalItem = self.newTagOrignalList.item(self.newTagTranslList.row(translItem))
            orignalItem.setForeground(Qt.gray)
            translItem.setForeground(Qt.gray)

            orignalTag = orignalItem.text()

            # mark the tag in the new tag list as added
            for tagPair in self.newTagLst:
                if tagPair[0] == orignalTag:
                    tagPair.append("added")
                    return
    
    def contextMenuEvent(self, event: QContextMenuEvent):
        """show context menu when right click"""
        # Get the currently selected item
        currentItem = self.itemAt(event.pos())
        # get the parent item of the currently selected item
        parentItem = currentItem.parent()
        # get the tag name of the currently selected item
        tagName = currentItem.text(0)
        # get the tag name of the parent item
        parentTagName = parentItem.text(0)
        contextMenu = QMenu(self)
        contextMenu.addAction(QAction("在view tree中展开", self, triggered=lambda: self.showInViewTree()))
        contextMenu.addAction(QAction("编辑同义标签", self, triggered=lambda: self.synonymEdit(tagName)))
        contextMenu.addAction(QAction("删除标签", self, triggered=lambda: self.confirmDelete(tagName, parentTagName, currentItem, parentItem)))
        contextMenu.exec_(event.globalPos())

    def showInViewTree(self):
        resultItem = self.getCorrespondingTreeItem(self.currentItem(), self.viewTree)
        self.viewTree.setFocus()
        self.viewTree.setCurrentItem(resultItem)
        self.viewTree.scrollToItem(resultItem)

    def confirmDelete(self, tagName, parentTagName, currentItem, parentItem):
        """show the delete tag dialog"""
        self.deleteTagDialog.setContent(tagName, parentTagName)
        result = self.deleteTagDialog.exec_()
        if result == QDialog.Accepted:
            self.editTree("del", tagName, parentTagName, subItem=currentItem, parentItem=parentItem)

    def synonymEdit(self, tagName):
        """show the synonym edit dialog"""
        synonyms = self.tagTree.tagDict[tagName].synonyms
        enName = self.tagTree.tagDict[tagName].enName
        self.synonymEditDialog.setContent(tagName, synonyms, enName)
        result = self.synonymEditDialog.exec_()
        if result == QDialog.Accepted:
            synonymsInput = set(self.synonymEditDialog.synonymTextEdit.toPlainText().split("\n"))
            enNameInput = self.synonymEditDialog.englishNameEdit.toPlainText()

            if enNameInput.isascii():
                self.tagTree.tagDict[tagName].setEnName(enNameInput)
            else:
                self.outputBox.append("英文名只能包含ASCII字符")
            
            edited = {i for i in synonymsInput if i.startswith("#")}
            self.tagTree.tagDict[tagName].synonyms = edited


    def undoOperation(self):
        if len(self.history) > 1:
            pass
        else:
            self.outputBox.append("no operation to undo")
        return