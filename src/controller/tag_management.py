from typing import TYPE_CHECKING

from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QAbstractItemView, QLineEdit, QListWidgetItem, QDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QDropEvent, QBrush

from service.tag_tree import TagTree, Tag
from service.database import PicDatabase
from utils.json import load_json, write_json
from component.dialog.tag_delete_dialog import DeleteDialog
from component.dialog.tag_edit_dialog import TagEditDialog
from tools.log import log_execution

if TYPE_CHECKING:
    from view.tag_management import MainWindow


class TagManagementController:
    new_tag_list: list[tuple[str, str, int]]
    
    
    def __init__(self, view: 'MainWindow') -> None:
        self.MIN_APPEARANCE = 5
        self.view = view
        self.view.setup_controller(self)
        
        self.tag_tree = TagTree()
        self._load_tag_tree()
        
        self.database = PicDatabase()
        self._load_new_tag()
        
        self._init_tree_search()

        self.undo_stack = []
        self.redo_stack = [] #TODO: implement redo
    
    def search_tree(
            self,
            tree: QTreeWidget, 
            searchEdit: QLineEdit, 
        ):
        """search the tree widget"""
        if tree is self.view.viewTree:
            last_search = self.view_tree_last_search
            search_index = self.view_tree_search_index
            search_list = self.view_tree_search_list
        elif tree is self.view.mainTree:
            last_search = self.main_tree_last_search
            search_index = self.main_tree_search_index
            search_list = self.main_tree_search_list
        
        search_text = searchEdit.text()
        if search_text == last_search and search_list:
            if search_index < len(search_list):
                self._expand_and_scroll_to_item(search_list[search_index])
                search_index += 1
            else:
                search_index = 0
                self._expand_and_scroll_to_item(search_list[search_index])
        else:
            search_list = tree.findItems(search_text, Qt.MatchFlag.MatchContains | Qt.MatchFlag.MatchRecursive)
            search_index = 0
            last_search = search_text
            if search_list:
                self._expand_and_scroll_to_item(search_list[search_index])
                search_index += 1
                
        if tree is self.view.viewTree:
            self.view_tree_last_search = last_search
            self.view_tree_search_index = search_index
            self.view_tree_search_list = search_list
        elif tree is self.view.mainTree:
            self.main_tree_last_search = last_search
            self.main_tree_search_index = search_index
            self.main_tree_search_list = search_list

        return
            
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
        
    @log_execution("Info", None, "Tag tree saved")
    def save_tree(self):
        self.tag_tree.save_tree()
        write_json(self.new_tag_list, self.new_tag_path)
        self.view.outputTextEdit.append("标签树已保存")
        return

    def main_tree_drop_event(self, event: QDropEvent):
        """handle drop event and make changes to the tag tree"""
        target_item = self.view.mainTree.itemAt(event.pos())
        if target_item is None:
            return
        
        source = event.source()
        drag_item = source.currentItem()

        try:
            if source is self.view.viewTree:
                if drag_item.text(0) == target_item.text(0):
                    self.view.outputTextEdit.append("不能将标签移动到自身")
                if self.view.tagMovingCheckBox.isChecked():
                    source_item = drag_item.parent()
                    moved_item = self._move_tag(drag_item, target_item)
                    self.view.outputTextEdit.append(
                        f"标签 <b>{drag_item.text(0)}</b> 从 <b>{source_item.text(0)}</b> 移动至 <b>{target_item.text(0)}</b>"
                    )
                    self._add_history(("move", moved_item, source_item))
                else:
                    added_item = self._add_parent_tag(drag_item, target_item)
                    self.view.outputTextEdit.append(
                        f"标签 <b>{drag_item.text(0)}</b> 添加父标签 <b>{target_item.text(0)}</b>"
                    )
                    self._add_history(("add_parent", added_item))

            elif source is self.view.newTagStoreList:
                added_item = self._add_new_tag(drag_item, target_item)
                self._mark_added(drag_item)
                self.view.outputTextEdit.append(
                    f"添加新标签 <b>{drag_item.text()}</b> 到 <b>{target_item.text(0)}</b>"
                )
                self._add_history(("add_new", added_item))

            elif source is self.view.newTagOriginalList:
                self._add_synonym(drag_item.text(), target_item.text(0))
                self._mark_added(drag_item)
                self.view.outputTextEdit.append(
                    f"同义标签 <b>{drag_item.text()}</b> 添加至 <b>{target_item.text(0)}</b>"
                )
                self._add_history(("add_synonym", drag_item.text(), target_item.text(0)))

            elif source is self.view.newTagTranslList:
                original_item = self.view.newTagOriginalList.item(self.view.newTagTranslList.row(drag_item))
                if original_item.text() == drag_item.text(): # add new tag if the original tag and the translation are the same
                    added_item = self._add_new_tag(drag_item, target_item)
                    self._mark_added(drag_item)
                    self.view.outputTextEdit.append(
                        f"添加新标签 <b>{drag_item.text()}</b> 到 <b>{target_item.text(0)}</b>"
                    )
                    self._add_history(("add_new", added_item))
                else: # add new tag and synonym if the original tag and the translation are different
                    added_item = self._add_new_tag(drag_item, target_item)
                    self._add_synonym(original_item.text(), drag_item.text())
                    self._mark_added(drag_item)
                    self.view.outputTextEdit.append(
                        f"添加新标签 <b>{drag_item.text()}</b> 到 <b>{target_item.text(0)}</b>, 并添加同义标签 <b>{original_item.text()}</b>"
                    )
                    self._add_history(("add_new_and_synonym", added_item, drag_item, original_item))
                
        except ValueError as e:
            self.view.outputTextEdit.append(f"<b><span style='color: red;'>操作失败: {str(e)}</span></b>")
        
        except KeyError as e:
            self.view.outputTextEdit.append(f"<b><span style='color: red;'>操作失败: {str(e)}</span></b>")
            
    def show_in_view_tree(self):
        result_item = self._get_corresponding_tree_item(self.view.mainTree.currentItem())
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
            self._delete_tag(current_item)
            self.undo_stack.append(("delete", tag_name, parent_item))
            self.view.outputTextEdit.append(f"标签 <b>{tag_name}</b> 从 <b>{parent_tag_name}</b> 删除")

    def edit_tag(self, tag_name):
        """show the synonym edit dialog"""
        synonyms = self.tag_tree.tag_dict[tag_name].synonyms
        en_name = self.tag_tree.tag_dict[tag_name].en_name
        tag_type = self.tag_tree.tag_dict[tag_name].tag_type
        
        dialog = TagEditDialog(self.view, tag_name, synonyms, en_name, tag_type)
        result = dialog.exec_()
        if result == QDialog.DialogCode.Accepted:
            synonyms_input = set(dialog.synonymTextEdit.toPlainText().split("\n"))
            en_name_input = dialog.englishNameEdit.text()
            type_input = dialog.typeComboBox.currentText()
            if en_name_input.isascii():
                self.tag_tree.tag_dict[tag_name].set_en_name(en_name_input)
            else:
                self.view.outputTextEdit.append("英文名只能包含ASCII字符")
            
            if type_input:
                self.tag_tree.tag_dict[tag_name].tag_type = type_input
            
            edited = {i for i in synonyms_input if i.startswith("#")}
            self.tag_tree.tag_dict[tag_name].synonyms = edited

    def undo(self):
        if not self.undo_stack:
            return
        
        operation = self.undo_stack.pop()
        self.redo_stack.append(operation)
        if operation[0] == "add_parent":
            parent_tag = operation[1].parent().text(0)
            sub_tag = operation[1].text(0)
            self._delete_tag(operation[1])
            self.view.outputTextEdit.append(
                f"撤销添加父标签 <b>{parent_tag}</b> 到 <b>{sub_tag}</b>"
            )
        
        elif operation[0] == "add_synonym":
            self.tag_tree.tag_dict[operation[2]].remove_synonym(operation[1])
            self.view.newTagOriginalList.findItems(operation[1], Qt.MatchFlag.MatchExactly)[0].setForeground(QBrush())
            self.view.outputTextEdit.append(
                f"撤销添加同义标签 <b>{operation[1]}</b> 到 <b>{operation[2]}</b>"
            )
        
        elif operation[0] == "add_new":
            self._delete_tag(operation[1])
            self.view.outputTextEdit.append(
                f"撤销添加新标签 <b>{operation[1].text(0)}</b> 到 <b>{operation[2].text(0)}</b>"
            )
        
        elif operation[0] == "add_new_and_synonym":
            self._delete_tag(operation[1])
            operation[2].setForeground(QBrush())
            operation[3].setForeground(QBrush())
            self.view.outputTextEdit.append(
                f"撤销添加新标签 <b>{operation[1].text(0)}</b>, 并添加同义标签 <b>{operation[3].text()}</b>"
            )
        
        elif operation[0] == "delete":
            self._add_parent_tag(QTreeWidgetItem([operation[1]]), operation[2])
            self.view.outputTextEdit.append(
                f"撤销从 <b>{operation[2].text(0)}</b> 删除标签 <b>{operation[1]}</b>"
            )
        
        elif operation[0] == "move":
            tag = operation[1].text(0)
            parent_tag = operation[1].parent().text(0)
            self._move_tag(operation[1], operation[2])
            self.view.outputTextEdit.append(
                f"撤销从 <b>{operation[2].text(0)}</b> 移动标签 <b>{tag}</b> 到 <b>{parent_tag}</b>"
            )
    
    def _init_tree_search(self):
        self.view_tree_last_search = ""
        self.view_tree_search_index = 0
        self.view_tree_search_list = []
        self.main_tree_last_search = ""
        self.main_tree_search_index = 0
        self.main_tree_search_list = []
    
    def _expand_and_scroll_to_item(self, item: QTreeWidgetItem):
        """expand the tree widget and scroll to the item"""
        tree = item.treeWidget()
        parent = item.parent()
        while parent:
            parent.setExpanded(True)
            parent = parent.parent()

        tree.scrollToItem(item, QAbstractItemView.ScrollHint.PositionAtCenter)
        tree.setCurrentItem(item)
        
    def _get_tree_item(self, tag: Tag) -> QTreeWidgetItem:
        item = QTreeWidgetItem([tag.name])
        for subTag in tag.sub_tags.values():
            item.addChild(self._get_tree_item(subTag))
        return item
    
    @log_execution("Info", None, "Tag tree loaded")
    def _load_tag_tree(self):
        """load tag tree from tag_tree.json and show it in the tree widget"""
        self.view.viewTree.addTopLevelItem(self._get_tree_item(self.tag_tree.root))
        self.view.mainTree.addTopLevelItem(self._get_tree_item(self.tag_tree.root))

        self.view.viewTree.expandItem(self.view.viewTree.topLevelItem(0))
        for i in range(self.view.viewTree.topLevelItem(0).childCount()):
            self.view.viewTree.expandItem(self.view.viewTree.topLevelItem(0).child(i))

        self.view.mainTree.expandItem(self.view.mainTree.topLevelItem(0))
        for i in range(self.view.mainTree.topLevelItem(0).childCount()):
            self.view.mainTree.expandItem(self.view.mainTree.topLevelItem(0).child(i))
        
        return
            
    @log_execution("Info", None, "New tag loaded")
    def _load_new_tag(self):
        """load new tag file and show it in the new tag lst"""
        self.database.count_tags()
        self.new_tag_list = self.database.get_tag_count_list()
        existing_tags = self._get_existing_tags()
        new_tag_count = 0
        for tag_pair in self.new_tag_list:
            if tag_pair[0].endswith("入り"):
                continue
            
            if tag_pair[0] in existing_tags or tag_pair[1] in existing_tags or tag_pair[2] < self.MIN_APPEARANCE: # skip existing tags and tags with low appearance
                continue

            self.view.newTagOriginalList.addItem(tag_pair[0])
            new_trasl_item = QListWidgetItem(tag_pair[1])
            new_trasl_item.setFlags(new_trasl_item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.view.newTagTranslList.addItem(new_trasl_item)
            new_tag_count += 1
        
        self.view.outputTextEdit.append(f"共有 {new_tag_count} 个新标签")
        return
    
    def _get_existing_tags(self) -> set[str]:
        """get all the existing tags in the tag tree"""
        existing_tags = set()
        for tag in self.tag_tree.tag_dict:
            existing_tags.add(tag)
            existing_tags.update(self.tag_tree.tag_dict[tag].synonyms)

        return existing_tags
    
    def _add_new_tag(self, sub_item: QListWidgetItem, parent_item: QTreeWidgetItem):
        """Add a new tag"""
        sub_tag = sub_item.text()
        parent_tag = parent_item.text(0)
        self.tag_tree.add_new_tag(sub_tag, parent_tag)
        
        added_item = QTreeWidgetItem([sub_tag])
        parent_item.addChild(added_item)
        view_parent_item = self._get_corresponding_tree_item(parent_item)
        view_parent_item.addChild(QTreeWidgetItem([sub_tag]))

        return added_item
    
    def _add_parent_tag(self, sub_item: QTreeWidgetItem, parent_item: QTreeWidgetItem):
        """Add a parent tag"""
        sub_tag = sub_item.text(0)
        parent_tag = parent_item.text(0)
        
        self.tag_tree.add_parent_tag(sub_tag, parent_tag)
        
        added_item = QTreeWidgetItem([sub_tag])
        parent_item.addChild(added_item)
        corres_tree_parent_item = self._get_corresponding_tree_item(parent_item)
        corres_tree_parent_item.addChild(QTreeWidgetItem([sub_tag]))

        return added_item
    
    def _add_synonym(self, sub_tag: str, parent_tag: str):
        """Add a synonym"""        
        self.tag_tree.tag_dict[parent_tag].add_synonym(sub_tag)
    
    def _delete_tag(self, sub_item: QTreeWidgetItem):
        """Delete a tag"""
        parent_item = sub_item.parent()
        sub_tag = sub_item.text(0)
        parent_tag = parent_item.text(0)
        
        self.tag_tree.delete_tag(sub_tag, parent_tag)
        
        view_tree_parent_item = self._get_corresponding_tree_item(parent_item)
        view_tree_parent_item.removeChild(self._get_corresponding_tree_item(sub_item))
        parent_item.removeChild(sub_item)
    
    def _move_tag(self, sub_item: QTreeWidgetItem, target_item: QTreeWidgetItem):
        """Move a tag"""
        source_item = sub_item.parent()
        
        source_tag = source_item.text(0)
        destination_tag = target_item.text(0)
        sub_tag = sub_item.text(0)
        
        self.tag_tree.add_parent_tag(sub_tag, destination_tag)
        self.tag_tree.delete_tag(sub_tag, source_tag)
        
        main_tree_source_item = self._get_corresponding_tree_item(source_item)
        main_tree_sub_item = self._get_corresponding_tree_item(sub_item)
        view_tree_target_item = self._get_corresponding_tree_item(target_item)
        added_item = QTreeWidgetItem([sub_tag])
        target_item.addChild(added_item)
        view_tree_target_item.addChild(QTreeWidgetItem([sub_tag]))
        main_tree_source_item.removeChild(main_tree_sub_item)
        source_item.removeChild(sub_item)

        return added_item

    def _get_corresponding_tree_item(self, source_item: QTreeWidgetItem) -> QTreeWidgetItem:
        """
        Retrieves the corresponding tree item in the other tree widget.
        """
        index = []

        if source_item.treeWidget() is self.view.viewTree:
            target_tree = self.view.mainTree
        elif source_item.treeWidget() is self.view.mainTree:
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

    def _mark_added(self, tag_item: QListWidgetItem):
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

    def _add_history(self, operation: tuple):
        self.undo_stack.append(operation)
        if len(self.undo_stack) > 10:
            self.undo_stack.pop(0)
                