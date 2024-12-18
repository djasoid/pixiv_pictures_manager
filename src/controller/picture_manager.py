from typing import TYPE_CHECKING

from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QAbstractItemView, QTextEdit, QListWidgetItem, QDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QDropEvent, QBrush

from service.tag_tree import TagTree, Tag
from service.database import PicDatabase
from tools.log import log_execution
from component.widget.tag_widget import TagWidget
if TYPE_CHECKING:
    from view.picture_manager import MainWindow

class PictureManagerController:
    def __init__(self, view: 'MainWindow'):
        self.view = view
        self.tag_index_cache = {}
        self.database = PicDatabase()
        self._init_context()
        self._init_tag_tree()
        self.view.setup_controller(self)
        self._init_tag_search()
        
    def _init_context(self):
        self.show_restricted = False
        self.include_tag_set = set()
        self.exclude_tag_set = set()
        self.filtered_pids = set()
        self.sorted_pids = []
        
    def _init_tag_tree(self):
        self.tag_tree = TagTree()
        self.tag_item_dict: dict[str, set[QTreeWidgetItem]] = {}
        for top_tag in self.tag_tree.root.sub_tags.values():
            if top_tag.tag_type == '__CHARACTER__':
                self.character_top_tag = top_tag
                self.view.characterTagTree.addTopLevelItem(self._get_tree_item(top_tag))
                self.view.characterTagTree.expandItem(self.view.characterTagTree.topLevelItem(0))
            elif top_tag.tag_type == '__ATTRIBUTE__':
                self.attribute_top_tag = top_tag
                self.view.attributeTagTree.addTopLevelItem(self._get_tree_item(top_tag))
                self.view.attributeTagTree.expandItem(self.view.attributeTagTree.topLevelItem(0))
        
    def _get_tree_item(self, tag: Tag) -> QTreeWidgetItem:
        item = QTreeWidgetItem([tag.name])
        if tag.name in self.tag_item_dict:
            self.tag_item_dict[tag.name].add(item)
        else:
            self.tag_item_dict[tag.name] = {item}
        
        for sub_tag in tag.sub_tags.values():
            if not self.show_restricted and sub_tag.tag_type == 'R-18':
                continue
            item.addChild(self._get_tree_item(sub_tag))
        
        return item

    def add_include_tag(self, item: QTreeWidgetItem, column: int):
        tag_name = item.text(0)
        tag = self.tag_tree.get_tag(tag_name)
        if not tag.is_tag:
            return
        
        if tag_name not in self.include_tag_set and tag_name not in self.exclude_tag_set:
            self.include_tag_set.add(tag_name)
            tag_widget = TagWidget(self, tag_name, True)
            self.view.selectedTagLayout.insertWidget(0, tag_widget)
            self.last_added_tag = tag_widget
        else:
            return
        
    def add_exclude_tag(self, item: QTreeWidgetItem, column: int):
        tag_name = item.text(0)
        tag = self.tag_tree.get_tag(tag_name)
        if not tag.is_tag:
            return
        
        if tag_name not in self.exclude_tag_set:
            self.remove_selected_tag(self.last_added_tag)    
            self.exclude_tag_set.add(tag_name)
            self.view.selectedTagLayout.addWidget(TagWidget(self, tag_name, False))
        else:
            return
        
    def remove_selected_tag(self, tag_widget: TagWidget):
        if tag_widget.include:
            self.include_tag_set.remove(tag_widget.tag_name)
        else:
            self.exclude_tag_set.remove(tag_widget.tag_name)
        self.view.selectedTagLayout.removeWidget(tag_widget)
        tag_widget.deleteLater()
    
    def _init_tag_search(self):
        self.tag_last_search = ""
        self.tag_search_results = []
        self.tag_search_index = 0

    def tag_search(self, search_text: str):
        if search_text == self.tag_last_search and self.tag_search_results:
            if self.tag_search_index < len(self.tag_search_results):
                self._expand_and_scroll_to_tag_item(self.tag_search_results[self.tag_search_index])
                self.tag_search_index += 1
            else:
                self.tag_search_index = 0
                self._expand_and_scroll_to_tag_item(self.tag_search_results[self.tag_search_index])
        else:
            character_search_results = self.view.characterTagTree.findItems(search_text, Qt.MatchFlag.MatchContains | Qt.MatchFlag.MatchRecursive)
            attribute_search_results = self.view.attributeTagTree.findItems(search_text, Qt.MatchFlag.MatchContains | Qt.MatchFlag.MatchRecursive)
            self.tag_search_results = character_search_results + attribute_search_results
            self.tag_last_search = search_text
            self.tag_search_index = 0
            if self.tag_search_results:
                self._expand_and_scroll_to_tag_item(self.tag_search_results[self.tag_search_index])
                self.tag_search_index += 1
                
    def _expand_and_scroll_to_tag_item(self, tag_item: QTreeWidgetItem):
        """Expand the tag tree and select the tag item"""
        tree_widget = tag_item.treeWidget()
        if tree_widget is self.view.characterTagTree:
            self.view.tagTreeTabWidget.setCurrentIndex(0)
        elif tree_widget is self.view.attributeTagTree:
            self.view.tagTreeTabWidget.setCurrentIndex(1)
            
        parent_item = tag_item.parent()
        while parent_item:
            parent_item.setExpanded(True)
            parent_item = parent_item.parent()
            
        tree_widget.setCurrentItem(tag_item)
        tree_widget.scrollToItem(tag_item, QAbstractItemView.ScrollHint.PositionAtCenter)
        
    def _pic_tag_search(self) -> None:
        """
        Search for pictures with tags.
        the search will return a set of picture ids that have all the tags in includeTags and none of the tags in excludeTags.
        """
        def find_pids(tag: str) -> set:
            related_tags = {tag} | self.tag_tree.get_sub_tags(tag)
            pids = set()
            for related_tag in related_tags:
                if related_tag in self.tag_index_cache:
                    pids.update(self.tag_index_cache[related_tag])
                else:
                    tag_pids = self.database.get_pids_by_tag(related_tag)
                    self.tag_index_cache[related_tag] = tag_pids
                    pids.update(tag_pids)

            return pids
                
        included_pids = None
        for tag in self.include_tag_set:
            if included_pids is None:
                included_pids = find_pids(tag)
            else:
                included_pids &= find_pids(tag)

        excluded_pids = set()
        for tag in self.exclude_tag_set:
            excluded_pids.update(find_pids(tag))
        
        self.filtered_pids = included_pids - excluded_pids if included_pids else set()
    
    