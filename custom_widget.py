from PySide6.QtWidgets import QTextEdit, QTreeWidget, QTreeWidgetItem, QListWidget, QMenu, QDialog, QCheckBox
from PySide6.QtGui import QContextMenuEvent, QFont, QAction
from PySide6.QtCore import QByteArray, Qt

from Ui_delete_tag_dialog import Ui_delete_tag_dialog
from Ui_synonym_edit_dialog import Ui_synonym_edit_dialog

import tag_tree as tree
import data as dataFn

class DeleteDialog(QDialog, Ui_delete_tag_dialog):
    def __init__(self, parent, tagName, parentTagName):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.deleteInfoLabel.setText(f"确认从 {parentTagName} 删除 {tagName} ?")
    
    def accept(self):
        super().accept()
    
    def reject(self):
        super().reject()

class SynonymEditDialog(QDialog, Ui_synonym_edit_dialog):
    def __init__(self, parent, tagName: str, synonyms: set, enName: str, type: str):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.setWindowTitle(f"编辑同义标签：{tagName}")
        self.synonymTextEdit.setPlainText("\n".join(synonyms))
        self.englishNameEdit.setPlainText(enName)
        self.typeComboBox.addItems(["", "IP", "Character", "R-18"])
        if type:
            self.typeComboBox.setCurrentText(type)

    def accept(self):
        super().accept()
    
    def reject(self):
        super().reject()

class MainTagTreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addedFont = QFont()

    def setTagTree(self, tagTree: tree.TagTree):
        self.tagTree = tagTree
        
    def setViewTree(self, viewTree: QTreeWidget):
        self.viewTree = viewTree

    def setOutputBox(self, outputBox: QTextEdit):
        self.outputBox = outputBox

    def setNewTagLst(self, newTagLst: list):
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

        try:
            if source == "viewTree": # copy and move operation
                if dragTag == targetTag:
                    self.outputBox.append("不能将标签移动到自身")
                else:
                    if self.tagMovingCheckBox.isChecked():
                        self.moveTag(dragTag, targetTag, dragTagSource, dragTagItem, targetItem, dragTagSourceItem) 
                    else:
                        self.addParentTag(dragTag, targetTag, targetItem)

            elif source == "newTagStoreList": # add operation
                self.addNewTag(dragTag, targetTag, targetItem)
                self.markAdded(dragTag, True)

            elif source == "newTagOrignalList":
                self.addSynonym(dragTag, targetTag)
                self.markAdded(dragTag, True)

            elif source == "newTagTranslList": # add operation
                self.addNewTag(dragTag, targetTag, targetItem)
                originalTag = self.newTagOrignalList.item(self.newTagTranslList.row(event.source().currentItem())).text()
                self.addSynonym(originalTag, dragTag)
                self.markAdded(dragTag, False)
        except ValueError as e:
            self.outputBox.append(f"<b><span style='color: red;'>操作失败: {str(e)}</span></b>")
    
    def addNewTag(self, sub: str, parent: str, parentItem: QTreeWidgetItem):
        """Add a new tag"""
        self.tagTree.addNewTag(sub, parent)
        parentItem.addChild(QTreeWidgetItem([sub]))
        viewParentItem = self.getCorrespondingTreeItem(parentItem, self.viewTree)
        viewParentItem.addChild(QTreeWidgetItem([sub]))
        self.outputBox.append(f"添加新标签 {sub} 到 {parent}")
    
    def addParentTag(self, sub: str, parent: str, parentItem: QTreeWidgetItem):
        """Add a parent tag"""
        self.tagTree.addParentTag(sub, parent)
        parentItem.addChild(QTreeWidgetItem([sub]))
        viewParentItem = self.getCorrespondingTreeItem(parentItem, self.viewTree)
        viewParentItem.addChild(QTreeWidgetItem([sub]))
        self.outputBox.append(f"标签 {sub} 添加至 {parent}下")
    
    def addSynonym(self, sub: str, parent: str):
        """Add a synonym"""
        self.tagTree.tagDict[parent].addSynonym(sub)
        self.outputBox.append(f"同义标签 {sub} 添加至 {parent}")
    
    def deleteTag(self, sub: str, parent: str, subItem: QTreeWidgetItem, parentItem: QTreeWidgetItem):
        """Delete a tag"""
        self.tagTree.deleteTag(sub, parent)
        viewParentItem = self.getCorrespondingTreeItem(parentItem, self.viewTree)
        viewParentItem.removeChild(self.getCorrespondingTreeItem(subItem, self.viewTree))
        parentItem.removeChild(subItem)
        self.outputBox.append(f"标签 {sub} 从 {parent} 删除")
    
    def moveTag(self, sub: str, parent: str, source: str, subItem: QTreeWidgetItem, parentItem: QTreeWidgetItem, sourceItem: QTreeWidgetItem):
        """Move a tag"""
        self.tagTree.addParentTag(sub, parent)
        self.tagTree.deleteTag(sub, source)
        mainTreeSourceItem = self.getCorrespondingTreeItem(sourceItem, self)
        mainTreeSubItem = self.getCorrespondingTreeItem(subItem, self)
        viewTreeParentItem = self.getCorrespondingTreeItem(parentItem, self.viewTree)
        parentItem.addChild(mainTreeSubItem.clone())
        viewTreeParentItem.addChild(subItem.clone())
        mainTreeSourceItem.removeChild(mainTreeSubItem)
        sourceItem.removeChild(subItem)
        self.outputBox.append(f"标签 {sub} 从 {source} 移动至 {parent}")

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
        dialog = DeleteDialog(self, tagName, parentTagName)
        result = dialog.exec_()
        if result == QDialog.DialogCode.Accepted:
            self.deleteTag(tagName, parentTagName, currentItem, parentItem)

    def synonymEdit(self, tagName):
        """show the synonym edit dialog"""
        synonyms = self.tagTree.tagDict[tagName].synonyms
        enName = self.tagTree.tagDict[tagName].enName
        tagType = self.tagTree.tagDict[tagName].tagType
        dialog = SynonymEditDialog(self, tagName, synonyms, enName, tagType)
        result = dialog.exec_()
        if result == QDialog.DialogCode.Accepted:
            synonymsInput = set(dialog.synonymTextEdit.toPlainText().split("\n"))
            enNameInput = dialog.englishNameEdit.toPlainText()
            typeInput = dialog.typeComboBox.currentText()
            
            if enNameInput.isascii():
                self.tagTree.tagDict[tagName].setEnName(enNameInput)
            else:
                self.outputBox.append("英文名只能包含ASCII字符")
            
            if typeInput:
                self.tagTree.tagDict[tagName].tagType = typeInput
            
            edited = {i for i in synonymsInput if i.startswith("#")}
            self.tagTree.tagDict[tagName].synonyms = edited