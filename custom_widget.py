from PySide6.QtWidgets import QTextEdit, QTreeWidget, QTreeWidgetItem, QListWidget, QMenu, QDialog, QCheckBox
from PySide6.QtGui import QContextMenuEvent, QFont, QAction
from PySide6.QtCore import QByteArray, Qt

from Ui_delete_tag_dialog import Ui_delete_tag_dialog
from Ui_synonym_edit_dialog import Ui_synonym_edit_dialog

import tag_tree as tree
import data as dataFn

class DeleteDialog(QDialog, Ui_delete_tag_dialog):
    def __init__(self, parent, tag_name, parent_tag_name):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.deleteInfoLabel.setText(f"确认从 {parent_tag_name} 删除 {tag_name} ?")
    
    def accept(self):
        super().accept()
    
    def reject(self):
        super().reject()

class SynonymEditDialog(QDialog, Ui_synonym_edit_dialog):
    def __init__(self, parent, tag_name: str, synonyms: set, enName: str, type: str):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.setWindowTitle(f"编辑同义标签：{tag_name}")
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

    def set_tag_tree(self, tag_tree: tree.TagTree):
        self.tag_tree = tag_tree
        
    def set_view_tree(self, view_tree: QTreeWidget):
        self.view_tree = view_tree

    def set_output_box(self, output_box: QTextEdit):
        self.output_box = output_box

    def set_new_tag_list(self, new_tag_list: list):
        self.new_tag_list = new_tag_list
    
    def set_list_widgets(self, new_tag_orignal_list: QListWidget, new_tag_transl_list: QListWidget, new_tag_store_list: QListWidget):
        self.new_tag_orignal_list = new_tag_orignal_list
        self.new_tag_transl_list = new_tag_transl_list
        self.new_tag_store_list = new_tag_store_list

    def set_check_box(self, tag_moving_check_box: QCheckBox):
        self.tag_moving_check_box = tag_moving_check_box

    def dropEvent(self, event):
        """handle drop event and make changes to the tag tree"""
        target_item = self.itemAt(event.position().toPoint())
        if target_item is None:
            return
        
        target_tag = target_item.text(0)
        
        source = event.source().objectName()

        if source == "viewTree":
            drag_tag_item = event.source().currentItem()
            drag_tag_source_item = drag_tag_item.parent()
            drag_tag_source = drag_tag_source_item.text(0)
            drag_tag = drag_tag_item.text(0)
        else:
            drag_tag = event.source().currentItem().text()

        try:
            if source == "viewTree": # copy and move operation
                if drag_tag == target_tag:
                    self.output_box.append("不能将标签移动到自身")
                else:
                    if self.tag_moving_check_box.isChecked():
                        self.move_tag(drag_tag, target_tag, drag_tag_source, drag_tag_item, target_item, drag_tag_source_item) 
                    else:
                        self.add_parent_tag(drag_tag, target_tag, target_item)

            elif source == "newTagStoreList": # add operation
                self.add_new_tag(drag_tag, target_tag, target_item)
                self.mark_added(drag_tag, True)

            elif source == "newTagOrignalList":
                self.add_synonym(drag_tag, target_tag)
                self.mark_added(drag_tag, True)

            elif source == "newTagTranslList": # add operation
                self.add_new_tag(drag_tag, target_tag, target_item)
                original_tag = self.new_tag_orignal_list.item(self.new_tag_transl_list.row(event.source().currentItem())).text()
                self.add_synonym(original_tag, drag_tag)
                self.mark_added(drag_tag, False)
                
        except ValueError as e:
            self.output_box.append(f"<b><span style='color: red;'>操作失败: {str(e)}</span></b>")
    
    def add_new_tag(self, sub: str, parent: str, parent_item: QTreeWidgetItem):
        """Add a new tag"""
        self.tag_tree.add_new_tag(sub, parent)
        parent_item.addChild(QTreeWidgetItem([sub]))
        view_parent_item = self.get_corresponding_tree_item(parent_item, self.view_tree)
        view_parent_item.addChild(QTreeWidgetItem([sub]))
        self.output_box.append(f"添加新标签 <b>{sub}</b>到 <b>{parent}</b>")
    
    def add_parent_tag(self, sub: str, parent: str, parentItem: QTreeWidgetItem):
        """Add a parent tag"""
        self.tag_tree.add_parent_tag(sub, parent)
        parentItem.addChild(QTreeWidgetItem([sub]))
        viewParentItem = self.get_corresponding_tree_item(parentItem, self.view_tree)
        viewParentItem.addChild(QTreeWidgetItem([sub]))
        self.output_box.append(f"标签 <b>{sub}</b> 添加至 <b>{parent}</b> 下")
    
    def add_synonym(self, sub: str, parent: str):
        """Add a synonym"""
        self.tag_tree.tag_dict[parent].add_synonym(sub)
        self.output_box.append(f"同义标签 <b>{sub}</b> 添加至 <b>{parent}</b>")
    
    def delete_tag(self, sub: str, parent: str, subItem: QTreeWidgetItem, parent_item: QTreeWidgetItem):
        """Delete a tag"""
        self.tag_tree.delete_tag(sub, parent)
        view_parent_item = self.get_corresponding_tree_item(parent_item, self.view_tree)
        view_parent_item.removeChild(self.get_corresponding_tree_item(subItem, self.view_tree))
        parent_item.removeChild(subItem)
        self.output_box.append(f"标签 <b>{sub}</b> 从 <b>{parent}</b> 删除")
    
    def move_tag(self, sub: str, parent: str, source: str, subItem: QTreeWidgetItem, parent_item: QTreeWidgetItem, source_item: QTreeWidgetItem):
        """Move a tag"""
        self.tag_tree.add_parent_tag(sub, parent)
        self.tag_tree.delete_tag(sub, source)
        main_tree_source_item = self.get_corresponding_tree_item(source_item, self)
        main_tree_sub_item = self.get_corresponding_tree_item(subItem, self)
        view_tree_parent_item = self.get_corresponding_tree_item(parent_item, self.view_tree)
        parent_item.addChild(main_tree_sub_item.clone())
        view_tree_parent_item.addChild(subItem.clone())
        main_tree_source_item.removeChild(main_tree_sub_item)
        source_item.removeChild(subItem)
        self.output_box.append(f"标签 <b>{sub}</b> 从 <b>{source}</b> 移动至 <b>{parent}</b>")

    def get_corresponding_tree_item(self, source_item: QTreeWidgetItem, target_tree: QTreeWidget) -> QTreeWidgetItem:
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
        p_item = source_item.parent()
        while p_item:
            index.append(p_item.indexOfChild(source_item))
            source_item = p_item
            p_item = source_item.parent()
        index.reverse()
        target_item = target_tree.topLevelItem(0)
        for i in index:
                target_item = target_item.child(i)
        return target_item

    def mark_added(self, tag: str, orignal: bool):
        """mark the tag as added to the tag tree"""
        if orignal:
            orignal_items = self.new_tag_orignal_list.findItems(tag, Qt.MatchExactly)
            if orignal_items:
                orignal_item = orignal_items[0]
                orignal_item.setForeground(Qt.gray)
            else:
                return

            for tag_pair in self.new_tag_list:
                if tag_pair[0] == tag:
                    tag_pair.append("added")
                    return
                
        else:
            transl_item = self.new_tag_transl_list.findItems(tag, Qt.MatchExactly)[0]
            orignal_item = self.new_tag_orignal_list.item(self.new_tag_transl_list.row(transl_item))
            orignal_item.setForeground(Qt.gray)
            transl_item.setForeground(Qt.gray)
            orignal_tag = orignal_item.text()
            for tag_pair in self.new_tag_list:
                if tag_pair[0] == orignal_tag:
                    tag_pair.append("added")
                    return
    
    def contextMenuEvent(self, event: QContextMenuEvent):
        """show context menu when right click"""
        currentItem = self.itemAt(event.pos())
        parentItem = currentItem.parent()
        tagName = currentItem.text(0)
        parentTagName = parentItem.text(0)
        contextMenu = QMenu(self)
        contextMenu.addAction(QAction("在view tree中展开", self, triggered=lambda: self.show_in_view_tree()))
        contextMenu.addAction(QAction("编辑同义标签", self, triggered=lambda: self.synonym_edit(tagName)))
        contextMenu.addAction(QAction("删除标签", self, triggered=lambda: self.confirm_delete(tagName, parentTagName, currentItem, parentItem)))
        contextMenu.exec_(event.globalPos())

    def show_in_view_tree(self):
        result_item = self.get_corresponding_tree_item(self.currentItem(), self.view_tree)
        self.view_tree.setFocus()
        self.view_tree.setCurrentItem(result_item)
        self.view_tree.scrollToItem(result_item)

    def confirm_delete(self, tag_name, parent_tag_name, current_item, parent_item):
        """show the delete tag dialog"""
        dialog = DeleteDialog(self, tag_name, parent_tag_name)
        result = dialog.exec_()
        if result == QDialog.DialogCode.Accepted:
            self.delete_tag(tag_name, parent_tag_name, current_item, parent_item)

    def synonym_edit(self, tag_name):
        """show the synonym edit dialog"""
        synonyms = self.tag_tree.tag_dict[tag_name].synonyms
        en_name = self.tag_tree.tag_dict[tag_name].en_name
        tag_type = self.tag_tree.tag_dict[tag_name].tag_type
        dialog = SynonymEditDialog(self, tag_name, synonyms, en_name, tag_type)
        result = dialog.exec_()
        if result == QDialog.DialogCode.Accepted:
            synonyms_input = set(dialog.synonymTextEdit.toPlainText().split("\n"))
            en_name_input = dialog.englishNameEdit.toPlainText()
            type_input = dialog.typeComboBox.currentText()
            
            if en_name_input.isascii():
                self.tag_tree.tag_dict[tag_name].set_en_name(en_name_input)
            else:
                self.output_box.append("英文名只能包含ASCII字符")
            
            if type_input:
                self.tag_tree.tag_dict[tag_name].tag_type = type_input
            
            edited = {i for i in synonyms_input if i.startswith("#")}
            self.tag_tree.tag_dict[tag_name].synonyms = edited