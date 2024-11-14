from typing import TYPE_CHECKING

from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QAbstractItemView, QTextEdit, QListWidgetItem, QDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QDropEvent

from service.tag_tree import TagTree, Tag
from utils.json import load_json, write_json
from component.dialog.tag_delete_dialog import DeleteDialog
from component.dialog.tag_edit_dialog import TagEditDialog

if TYPE_CHECKING:
    from view.tag_management import MainWindow


class TagManagementController:
    new_tag_list: list[list[str]]
    
    def __init__(self, view: 'MainWindow', tag_tree_path: str, new_tag_path: str) -> None:
        self.view = view
        self.view.setup_controller(self)
        
        self.tag_tree = TagTree(tag_tree_path)
        self.load_tag_tree()
        
        self.new_tag_path = new_tag_path
        self.load_new_tag(new_tag_path)
        
        self.init_tree_search()

        self.history = []
    
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
        existing_tags = self.get_existing_tags()
        new_tag_count = 0
        for tag_pair in self.new_tag_list:
            if tag_pair[0] in existing_tags or tag_pair[1] in existing_tags: # skip existing tags
                continue

            self.view.newTagOriginalList.addItem(tag_pair[0])
            new_trasl_item = QListWidgetItem(tag_pair[1])
            new_trasl_item.setFlags(new_trasl_item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.view.newTagTranslList.addItem(new_trasl_item)
            new_tag_count += 1
        
        self.view.outputTextEdit.append(f"共有 {new_tag_count} 个新标签")
        return
    
    def get_existing_tags(self) -> set[str]:
        """get all the existing tags in the tag tree"""
        existing_tags = set()
        for tag in self.tag_tree.tag_dict:
            existing_tags.add(tag)
            existing_tags.update(self.tag_tree.tag_dict[tag].synonyms)

        return existing_tags

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

    def mainTree_drop_event(self, event: QDropEvent):
        """handle drop event and make changes to the tag tree"""
        target_item = self.view.mainTree.itemAt(event.pos())
        if target_item is None:
            return
        
        source = event.source()
        drag_item = source.currentItem()

        try:
            if source is self.view.viewTree: # copy and move operation
                if drag_item.text(0) == target_item.text(0):
                    self.view.outputTextEdit.append("不能将标签移动到自身")
                else:
                    if self.view.tagMovingCheckBox.isChecked(): # move tag
                        self.move_tag(drag_item, target_item) 
                    else: # copy tag
                        self.add_parent_tag(drag_item, target_item)

            elif source is self.view.newTagStoreList: # add new tag
                self.add_new_tag(drag_item, target_item)
                self.mark_added(drag_item)

            elif source is self.view.newTagOriginalList: # add synonym
                self.add_synonym(drag_item.text(), target_item.text(0))
                self.mark_added(drag_item)

            elif source is self.view.newTagTranslList: # add new tag
                self.add_new_tag(drag_item, target_item)
                original_item = self.view.newTagOriginalList.item(self.view.newTagTranslList.row(drag_item))
                self.add_synonym(original_item.text(), drag_item.text())
                self.mark_added(drag_item)
                
        except ValueError as e:
            self.view.outputTextEdit.append(f"<b><span style='color: red;'>操作失败: {str(e)}</span></b>")
        
        except KeyError as e:
            self.view.outputTextEdit.append(f"<b><span style='color: red;'>操作失败: {str(e)}</span></b>")
    
    def add_new_tag(self, sub_item: QListWidgetItem, parent_item: QTreeWidgetItem):
        """Add a new tag"""
        sub_tag = sub_item.text()
        parent_tag = parent_item.text(0)
        self.tag_tree.add_new_tag(sub_tag, parent_tag)
        
        parent_item.addChild(QTreeWidgetItem([sub_tag]))
        view_parent_item = self.get_corresponding_tree_item(parent_item)
        view_parent_item.addChild(QTreeWidgetItem([sub_tag]))
        
        self.view.outputTextEdit.append(f"添加新标签 <b>{sub_tag}</b>到 <b>{parent_tag}</b>")
    
    def add_parent_tag(self, sub_item: QTreeWidgetItem, parent_item: QTreeWidgetItem):
        """Add a parent tag"""
        sub_tag = sub_item.text(0)
        parent_tag = parent_item.text(0)
        
        self.tag_tree.add_parent_tag(sub_tag, parent_tag)
        
        parent_item.addChild(QTreeWidgetItem([sub_tag]))
        viewParentItem = self.get_corresponding_tree_item(parent_item)
        viewParentItem.addChild(QTreeWidgetItem([sub_tag]))
        
        self.view.outputTextEdit.append(f"标签 <b>{sub_tag}</b> 添加至 <b>{parent_tag}</b> 下")
    
    def add_synonym(self, sub_tag: str, parent_tag: str):
        """Add a synonym"""        
        self.tag_tree.tag_dict[parent_tag].add_synonym(sub_tag)
        
        self.view.outputTextEdit.append(f"同义标签 <b>{sub_tag}</b> 添加至 <b>{parent_tag}</b>")
    
    def delete_tag(self, sub_item: QTreeWidgetItem):
        """Delete a tag"""
        parent_item = sub_item.parent()
        sub_tag = sub_item.text(0)
        parent_tag = parent_item.text(0)
        
        self.tag_tree.delete_tag(sub_tag, parent_tag)
        
        view_parent_item = self.get_corresponding_tree_item(parent_item)
        view_parent_item.removeChild(self.get_corresponding_tree_item(sub_item))
        parent_item.removeChild(sub_item)
        
        self.view.outputTextEdit.append(f"标签 <b>{sub_tag}</b> 从 <b>{parent_tag}</b> 删除")
    
    def move_tag(self, sub_item: QTreeWidgetItem, target_item: QTreeWidgetItem):
        """Move a tag"""
        source_item = sub_item.parent()
        
        source_tag = source_item.text(0)
        destination_tag = target_item.text(0)
        sub_tag = sub_item.text(0)
        
        self.tag_tree.add_parent_tag(sub_tag, destination_tag)
        self.tag_tree.delete_tag(sub_tag, source_tag)
        
        main_tree_source_item = self.get_corresponding_tree_item(source_item)
        main_tree_sub_item = self.get_corresponding_tree_item(sub_item)
        view_tree_target_item = self.get_corresponding_tree_item(target_item)
        target_item.addChild(main_tree_sub_item.clone())
        view_tree_target_item.addChild(sub_item.clone())
        main_tree_source_item.removeChild(main_tree_sub_item)
        source_item.removeChild(sub_item)
        
        self.view.outputTextEdit.append(f"标签 <b>{sub_tag}</b> 从 <b>{source_tag}</b> 移动至 <b>{destination_tag}</b>")

    def get_corresponding_tree_item(self, source_item: QTreeWidgetItem) -> QTreeWidgetItem:
        """
        Retrieves the corresponding tree item in the other tree widget.
        """
        index = []

        source_tree = source_item.treeWidget()
        if source_tree is self.view.viewTree:
            target_tree = self.view.mainTree
        elif source_tree is self.view.mainTree:
            target_tree = self.view.viewTree

        parent_item = source_item.parent()
        while parent_item:
            index.append(parent_item.indexOfChild(source_item))
            source_item = parent_item
            parent_item = source_item.parent()

        index.reverse()
        target_item = target_tree.topLevelItem(0)
        for i in index:
                target_item = target_item.child(i)

        return target_item

    def mark_added(self, tag_item: QListWidgetItem):
        """mark the tag as added in the new tag list"""
        tag_item.setForeground(Qt.gray)
        if tag_item.listWidget() is self.view.newTagTranslList:
            original_item = self.view.newTagOriginalList.item(self.view.newTagTranslList.row(tag_item))
            original_item.setForeground(Qt.gray)
        elif tag_item.listWidget() is self.view.newTagStoreList:
            transl_item = self.view.newTagTranslList.findItems(tag_item.text(), Qt.MatchExactly)
            original_item = self.view.newTagOriginalList.findItems(tag_item.text(), Qt.MatchExactly)
            if transl_item:
                transl_item[0].setForeground(Qt.gray)

            if original_item:
                original_item[0].setForeground(Qt.gray)

        return

    def show_in_view_tree(self):
        result_item = self.get_corresponding_tree_item(self.view.mainTree.currentItem())
        self.view.viewTree.setFocus()
        self.view.viewTree.setCurrentItem(result_item)
        self.view.viewTree.scrollToItem(result_item)

    def confirm_delete(self, current_item: QTreeWidgetItem):
        """show the delete tag dialog"""
        parent_item = current_item.parent()
        tag_name = current_item.text(0)
        parent_tag_name = parent_item.text(0)
        
        dialog = DeleteDialog(self.view, tag_name, parent_tag_name)
        result = dialog.exec_()
        if result == QDialog.DialogCode.Accepted:
            self.delete_tag(current_item)

    def edit_tag(self, tag_name):
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