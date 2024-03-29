from PySide6.QtWidgets import QTextEdit, QTreeWidget, QTreeWidgetItem, QListWidget, QMenu, QDialog, QCheckBox
from PySide6.QtGui import QContextMenuEvent, QFont, QAction
from PySide6.QtCore import QByteArray, Qt

from Ui_delete_tag_dialog import Ui_delete_tag_dialog
from Ui_synonym_edit_dialog import Ui_synonym_edit_dialog

import program_objects as progObjs
import pic_data_functions as dataFn

class deleteDialog(QDialog, Ui_delete_tag_dialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
    
    def setContent(self, tagName, parentTagName):
        self.delete_info_label.setText(f"确认从 {parentTagName} 删除 {tagName} ？")
    
    def accept(self):
        super().accept()
    
    def reject(self):
        super().reject()

class synonymEditDialog(QDialog, Ui_synonym_edit_dialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def setContent(self, tagName: str, synonyms: set, enName: str):
        self.setWindowTitle(f"编辑同义标签：{tagName}")
        self.synonym_text_edit.setPlainText("\n".join(synonyms))
        self.english_name_edit.setPlainText(enName)

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
        self.delete_tag_dialog = deleteDialog(self)
        self.synonym_edit_dialog = synonymEditDialog(self)

    def setTagTree(self, tagTree: progObjs.TagTree):
        self.tagTree = tagTree
        self.addTopLevelItem(tagTree.toTreeWidgetItem())

    def setOutputBox(self, output_Box: QTextEdit): # pass output_box to show output
        self.output_Box = output_Box

    def setNewTagLst(self, newTagLst: list): # pass newTagLst to record which tags are added
        self.newTagLst = newTagLst
    
    def setListWidgets(self, new_tag_orignal_list: QListWidget, new_tag_transl_list: QListWidget, new_tag_store_list: QListWidget):
        self.new_tag_orignal_list = new_tag_orignal_list
        self.new_tag_transl_list = new_tag_transl_list
        self.new_tag_store_list = new_tag_store_list

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

        if source == "viewTree":
            if dragTag == targetTag:
                self.output_Box.append("不能将标签移动到自身")
            else:
                if self.tagMovingCheckBox.isChecked(): #TODO: update the Tree widget in real time
                        self.editTree("move", dragTag, targetTag, source = dragTagSource)
                        targetItem.addChild(QTreeWidgetItem([dragTag]))
                else:
                    self.editTree("add_parent", dragTag, targetTag)
                    targetItem.addChild(QTreeWidgetItem([dragTag]))

        elif source == "newTagStoreList":
            self.editTree("add_new", dragTag, targetTag)
            targetItem.addChild(QTreeWidgetItem([dragTag]))
            self.markAdded(dragTag, True)

        elif source == "newTagOrignalList":
            self.editTree("add_synonym", dragTag, targetTag)
            self.markAdded(dragTag, True)

        elif source == "newTagTranslList":
            self.editTree("add_new", dragTag, targetTag)
            targetItem.addChild(QTreeWidgetItem([dragTag]))
            originalTag = self.new_tag_orignal_list.item(self.new_tag_transl_list.row(event.source().currentItem())).text()
            self.editTree("add_synonym", originalTag, dragTag)
            self.markAdded(dragTag, False)
        
    def editTree(self, operation, sub, parent, subItem: QTreeWidgetItem = None, parentItem: QTreeWidgetItem = None, source: str = None):
        """edit the tag tree with the given operation"""

        if operation == "add_new": # add new tag
            self.tagTree.addNewTag(sub, parent)
            self.output_Box.append(f"添加新标签 {sub} 到 {parent}")
            return

        elif operation == "add_parent": # add parent tag
            self.tagTree.addParentTag(sub, parent)
            self.output_Box.append(f"标签 {sub} 添加至 {parent}")
            return

        elif operation == "add_synonym": # add synonym
            self.tagTree.tagDict[parent].addSynonym(sub)
            self.output_Box.append(f"同义标签 {sub} 添加至 {parent}")
            return

        elif operation == "del": # delete tag
            self.tagTree.deleteTag(sub, parent)
            parentItem.removeChild(subItem)
            self.output_Box.append(f"标签 {sub} 从 {parent} 删除")
            return
        
        elif operation == "move":
            self.tagTree.addParentTag(sub, parent)
            self.tagTree.deleteTag(sub, source)
            self.output_Box.append(f"标签 {sub} 从 {source} 移动至 {parent}")
        else:
            return

    def markAdded(self, tag: str, orignal: bool):
        """mark the tag as added to the tag tree"""
        if orignal:
            # set the font of the orignal tag to gray
            orignalItems = self.new_tag_orignal_list.findItems(tag, Qt.MatchExactly)
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
            translItem = self.new_tag_transl_list.findItems(tag, Qt.MatchExactly)[0]
            orignalItem = self.new_tag_orignal_list.item(self.new_tag_transl_list.row(translItem))
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
        contextMenu.addAction(QAction("编辑同义标签", self, triggered=lambda: self.synonymEdit(tagName)))
        contextMenu.addAction(QAction("删除标签", self, triggered=lambda: self.confirmDelete(tagName, parentTagName, currentItem, parentItem)))
        contextMenu.exec_(event.globalPos())

    def confirmDelete(self, tagName, parentTagName, currentItem, parentItem):
        """show the delete tag dialog"""
        self.delete_tag_dialog.setContent(tagName, parentTagName)
        result = self.delete_tag_dialog.exec_()
        if result == QDialog.Accepted:
            self.editTree("del", tagName, parentTagName, currentItem, parentItem)

    def synonymEdit(self, tagName):
        """show the synonym edit dialog"""
        synonyms = self.tagTree.tagDict[tagName].synonyms
        enName = self.tagTree.tagDict[tagName].enName
        self.synonym_edit_dialog.setContent(tagName, synonyms, enName)
        result = self.synonym_edit_dialog.exec_()
        if result == QDialog.Accepted:
            synonymsInput = set(self.synonym_edit_dialog.synonym_text_edit.toPlainText().split("\n"))
            enNameInput = self.synonym_edit_dialog.english_name_edit.toPlainText()

            if enNameInput.isascii():
                self.tagTree.tagDict[tagName].setEnName(enNameInput)
            else:
                self.output_Box.append("英文名只能包含ASCII字符")
            
            edited = {i for i in synonymsInput if i.startswith("#")}
            self.tagTree.tagDict[tagName].synonyms = edited


    def undoOperation(self):
        if len(self.history) > 1:
            pass
        else:
            self.output_Box.append("no operation to undo")
        return