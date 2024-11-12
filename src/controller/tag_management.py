from service.tag_tree import TagTree, Tag
from utils.json import load_json, write_json
from component.dialog.tag_delete_dialog import DeleteDialog
from component.dialog.tag_edit_dialog import TagEditDialog

from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QAbstractItemView, QTextEdit, QListWidgetItem, QDialog
from PySide6.QtCore import Qt
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from view.tag_management import MainWindow


class TagManagementController:
    new_tag_list: list[list[str]]
    
    def __init__(self, view: 'MainWindow', tag_tree_path: str, new_tag_path: str) -> None:
        self.view = view
        self.tag_tree = TagTree(tag_tree_path)
        self.load_tag_tree()
        self.new_tag_path = new_tag_path
        self.load_new_tag(new_tag_path)
        self.init_tree_search()
    
    def init_tree_search(self):
        self.view_tree_last_search = ""
        self.view_tree_search_index = 0
        self.view_tree_search_list = []
        self.main_tree_last_search = ""
        self.main_tree_search_index = 0
        self.main_tree_search_list = []
    
    def get_tree_item(self, tag: Tag) -> QTreeWidgetItem:
        item = QTreeWidgetItem([tag.name])
        for subTag in tag.sub_tags.values():
            item.addChild(self.get_tree_item(subTag))
        return item
    
    def load_tag_tree(self):
        """load tag tree from tag_tree.json and show it in the tree widget"""
        self.view.viewTree.addTopLevelItem(self.get_tree_item(self.tag_tree.root))
        self.view.mainTree.addTopLevelItem(self.get_tree_item(self.tag_tree.root))

        self.view.viewTree.expandItem(self.view.viewTree.topLevelItem(0))
        for i in range(self.view.viewTree.topLevelItem(0).childCount()):
            self.view.viewTree.expandItem(self.view.viewTree.topLevelItem(0).child(i))
        self.view.mainTree.expandItem(self.view.mainTree.topLevelItem(0))
        for i in range(self.view.mainTree.topLevelItem(0).childCount()):
            self.view.mainTree.expandItem(self.view.mainTree.topLevelItem(0).child(i))
        
        return
            
    def load_new_tag(self, new_tag_path: str):
        """load new tag file and show it in the new tag lst"""
        self.new_tag_list = load_json(new_tag_path)
        new_tag_count = 0
        for tag_pair in self.new_tag_list:
            if len(tag_pair) > 2: # if the tag has been added to the tag tree, pass it
                continue
            if self.tag_tree.is_in_tree(tag_pair[0]):
                if len(tag_pair) == 2:
                    tag_pair.append("added")
                continue
            self.view.newTagOrignalList.addItem(tag_pair[0])
            new_trasl_item = QListWidgetItem(tag_pair[1])
            new_trasl_item.setFlags(new_trasl_item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.view.newTagTranslList.addItem(new_trasl_item)
            new_tag_count += 1
        
        self.view.outputTextEdit.append(f"new tag loaded, {new_tag_count} tags in total")
        return
        
    def search_tree(
            self, 
            tree: QTreeWidget, 
            searchEdit: QTextEdit, 
        ):
        """search the tree widget"""
        if tree == self.view.viewTree:
            last_search = self.view_tree_last_search
            search_index = self.view_tree_search_index
            search_list = self.view_tree_search_list
        elif tree == self.view.mainTree:
            last_search = self.main_tree_last_search
            search_index = self.main_tree_search_index
            search_list = self.main_tree_search_list
        
        search_text = searchEdit.toPlainText()
        if search_text == last_search and search_list:
            if search_index < len(search_list):
                self.expand_and_scroll_to_item(search_list[search_index])
                search_index += 1
            else:
                search_index = 0
                self.expand_and_scroll_to_item(search_list[search_index])
        else:
            search_list = tree.findItems(search_text, Qt.MatchFlag.MatchContains | Qt.MatchFlag.MatchRecursive)
            search_index = 0
            last_search = search_text
            if search_list:
                self.expand_and_scroll_to_item(search_list[search_index])
                search_index += 1
                
        if tree == self.view.viewTree:
            self.view_tree_last_search = last_search
            self.view_tree_search_index = search_index
            self.view_tree_search_list = search_list
        elif tree == self.view.mainTree:
            self.main_tree_last_search = last_search
            self.main_tree_search_index = search_index
            self.main_tree_search_list = search_list
        return
            
    def expand_and_scroll_to_item(self, item: QTreeWidgetItem):
        """expand the tree widget and scroll to the item"""
        tree = item.treeWidget()
        parent = item.parent()
        while parent:
            parent.setExpanded(True)
            parent = parent.parent()
        tree.scrollToItem(item, QAbstractItemView.ScrollHint.PositionAtCenter)
        tree.setCurrentItem(item)

    def show_tag_info(self, current_item):
        """show the tag info of the selected tag in the tag tree widget"""
    
        tag_name = current_item.text(0)
        tag = self.tag_tree.tag_dict[tag_name]
        
        self.view.tagInfo.clear()
    
        if not tag.is_tag:
            self.view.tagInfo.append("<b>类:</b> " + tag.name)
            self.view.tagInfo.append("<b>子标签:</b>")
            self.view.tagInfo.append(", ".join(tag.sub_tags.keys()))
        else:
            items = [
                ("标签名: ", tag.name),
                ("标签类型: ", tag.tag_type),
                ("同义标签: ", ", ".join(tag.synonyms)),
                ("父标签: ", ", ".join(tag.parent)),
                ("子标签: ", ", ".join(tag.sub_tags.keys()))
            ]
            for label, content in items:
                self.view.tagInfo.append(f"<b>{label}</b>{content}")
    
        self.view.tagInfo.verticalScrollBar().setValue(0)
        return
        
    def save_tree(self):
        self.tag_tree.save_tree()
        write_json(self.new_tag_list, self.new_tag_path)
        self.view.outputTextEdit.append("标签树已保存")
        return

    def handle_drop_event(self, event):
        """handle drop event and make changes to the tag tree"""
        target_item = self.view.mainTree.itemAt(event.position().toPoint())
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
                    self.view.outputTextEdit.append("不能将标签移动到自身")
                else:
                    if self.view.tagMovingCheckBox.isChecked():
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
                original_tag = self.view.newTagOrignalList.item(self.view.newTagTranslList.row(event.source().currentItem())).text()
                self.add_synonym(original_tag, drag_tag)
                self.mark_added(drag_tag, False)
                
        except ValueError as e:
            self.view.outputTextEdit.append(f"<b><span style='color: red;'>操作失败: {str(e)}</span></b>")
    
    def add_new_tag(self, sub: str, parent: str, parent_item: QTreeWidgetItem):
        """Add a new tag"""
        self.tag_tree.add_new_tag(sub, parent)
        parent_item.addChild(QTreeWidgetItem([sub]))
        view_parent_item = self.get_corresponding_tree_item(parent_item, self.view.viewTree)
        view_parent_item.addChild(QTreeWidgetItem([sub]))
        self.view.outputTextEdit.append(f"添加新标签 <b>{sub}</b>到 <b>{parent}</b>")
    
    def add_parent_tag(self, sub: str, parent: str, parentItem: QTreeWidgetItem):
        """Add a parent tag"""
        self.tag_tree.add_parent_tag(sub, parent)
        parentItem.addChild(QTreeWidgetItem([sub]))
        viewParentItem = self.get_corresponding_tree_item(parentItem, self.view.viewTree)
        viewParentItem.addChild(QTreeWidgetItem([sub]))
        self.view.outputTextEdit.append(f"标签 <b>{sub}</b> 添加至 <b>{parent}</b> 下")
    
    def add_synonym(self, sub: str, parent: str):
        """Add a synonym"""
        self.tag_tree.tag_dict[parent].add_synonym(sub)
        self.view.outputTextEdit.append(f"同义标签 <b>{sub}</b> 添加至 <b>{parent}</b>")
    
    def delete_tag(self, sub: str, parent: str, subItem: QTreeWidgetItem, parent_item: QTreeWidgetItem):
        """Delete a tag"""
        self.tag_tree.delete_tag(sub, parent)
        view_parent_item = self.get_corresponding_tree_item(parent_item, self.view.viewTree)
        view_parent_item.removeChild(self.get_corresponding_tree_item(subItem, self.view.viewTree))
        parent_item.removeChild(subItem)
        self.view.outputTextEdit.append(f"标签 <b>{sub}</b> 从 <b>{parent}</b> 删除")
    
    def move_tag(self, sub: str, parent: str, source: str, subItem: QTreeWidgetItem, parent_item: QTreeWidgetItem, source_item: QTreeWidgetItem):
        """Move a tag"""
        self.tag_tree.add_parent_tag(sub, parent)
        self.tag_tree.delete_tag(sub, source)
        main_tree_source_item = self.get_corresponding_tree_item(source_item, self.view.mainTree)
        main_tree_sub_item = self.get_corresponding_tree_item(subItem, self.view.mainTree)
        view_tree_parent_item = self.get_corresponding_tree_item(parent_item, self.view.viewTree)
        parent_item.addChild(main_tree_sub_item.clone())
        view_tree_parent_item.addChild(subItem.clone())
        main_tree_source_item.removeChild(main_tree_sub_item)
        source_item.removeChild(subItem)
        self.view.outputTextEdit.append(f"标签 <b>{sub}</b> 从 <b>{source}</b> 移动至 <b>{parent}</b>")

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
            orignal_items = self.view.newTagOrignalList.findItems(tag, Qt.MatchExactly)
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
            transl_item = self.view.newTagTranslList.findItems(tag, Qt.MatchExactly)[0]
            orignal_item = self.view.newTagOrignalList.item(self.view.newTagTranslList.row(transl_item))
            orignal_item.setForeground(Qt.gray)
            transl_item.setForeground(Qt.gray)
            orignal_tag = orignal_item.text()
            for tag_pair in self.new_tag_list:
                if tag_pair[0] == orignal_tag:
                    tag_pair.append("added")
                    return

    def show_in_view_tree(self):
        result_item = self.get_corresponding_tree_item(self.view.mainTree.currentItem(), self.view.viewTree)
        self.view.viewTree.setFocus()
        self.view.viewTree.setCurrentItem(result_item)
        self.view.viewTree.scrollToItem(result_item)

    def confirm_delete(self, tag_name, parent_tag_name, current_item, parent_item):
        """show the delete tag dialog"""
        dialog = DeleteDialog(self.view, tag_name, parent_tag_name)
        result = dialog.exec_()
        if result == QDialog.DialogCode.Accepted:
            self.delete_tag(tag_name, parent_tag_name, current_item, parent_item)

    def synonym_edit(self, tag_name):
        """show the synonym edit dialog"""
        synonyms = self.tag_tree.tag_dict[tag_name].synonyms
        en_name = self.tag_tree.tag_dict[tag_name].en_name
        tag_type = self.tag_tree.tag_dict[tag_name].tag_type
        dialog = TagEditDialog(self.view, tag_name, synonyms, en_name, tag_type)
        result = dialog.exec_()
        if result == QDialog.DialogCode.Accepted:
            synonyms_input = set(dialog.synonymTextEdit.toPlainText().split("\n"))
            en_name_input = dialog.englishNameEdit.toPlainText()
            type_input = dialog.typeComboBox.currentText()
            
            if en_name_input.isascii():
                self.tag_tree.tag_dict[tag_name].set_en_name(en_name_input)
            else:
                self.view.outputTextEdit.append("英文名只能包含ASCII字符")
            
            if type_input:
                self.tag_tree.tag_dict[tag_name].tag_type = type_input
            
            edited = {i for i in synonyms_input if i.startswith("#")}
            self.tag_tree.tag_dict[tag_name].synonyms = edited