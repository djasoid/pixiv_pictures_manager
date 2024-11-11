from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QListWidgetItem, QTreeWidget, QTreeWidgetItem, QAbstractItemView
from PySide6.QtGui import QKeySequence, QShortcut, QTextCursor, QTextCharFormat, QFont

from ui_compiled.Ui_tag_tree_management import Ui_MainWindow

import data as dataFn
from tag_tree import Tag

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_tree_search()
        self.bind()
        self.load_tag_tree()
        self.load_new_tag()
        self.set_main_tree_ref()
        self.expand_top_level()
        
    def init_tree_search(self):
        self.view_tree_last_search = ""
        self.view_tree_search_index = 0
        self.view_tree_search_list = []
        self.main_tree_last_search = ""
        self.main_tree_search_index = 0
        self.main_tree_search_list = []
        
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
        self.viewTree.itemSelectionChanged.connect(self.show_tag_info)
        self.mainTree.itemSelectionChanged.connect(self.show_tag_info)

        # install event filter
        self.newTagInput.installEventFilter(self)
        self.newTagOrignalList.installEventFilter(self)
        self.viewTreeSearchEdit.installEventFilter(self)
        self.mainTreeSearchEdit.installEventFilter(self)

        # Connect the save shortcut
        self.save_shortcut = QShortcut(QKeySequence.StandardKey.Save, self)
        self.save_shortcut.activated.connect(self.save_tree)

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
                self.view_tree_last_search, self.view_tree_search_index, self.view_tree_search_list = \
                    self.search_tree(
                        self.viewTree, 
                        self.viewTreeSearchEdit, 
                        self.view_tree_last_search, 
                        self.view_tree_search_index, 
                        self.view_tree_search_list
                    )
                return True

        # Filter for main_tree_search_edit, implement search function
        elif (source == self.mainTreeSearchEdit and event.type() == QEvent.Type.KeyPress):
            if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
                self.main_tree_last_search, self.main_tree_search_index, self.main_tree_search_list = \
                    self.search_tree(
                        self.mainTree, 
                        self.mainTreeSearchEdit, 
                        self.main_tree_last_search, 
                        self.main_tree_search_index, 
                        self.main_tree_search_list
                    )
                return True
        
        return super().eventFilter(source, event)
    
    def search_tree(
            self, 
            tree: QTreeWidget, 
            searchEdit: QTextEdit, 
            last_search: str, 
            search_index: int, 
            search_list: list[QTreeWidgetItem]
        ):
        """search the tree widget"""
        def expand_and_scroll_to_item(item: QTreeWidgetItem):
            """expand the tree widget and scroll to the item"""
            parent = item.parent()
            while parent:
                parent.setExpanded(True)
                parent = parent.parent()
            tree.scrollToItem(item, QAbstractItemView.ScrollHint.PositionAtCenter)
            tree.setCurrentItem(item)
            
        search_text = searchEdit.toPlainText()
        if search_text == last_search and search_list:
            if search_index < len(search_list):
                expand_and_scroll_to_item(search_list[search_index])
                search_index += 1
            else:
                search_index = 0
                expand_and_scroll_to_item(search_list[search_index])
        else:
            search_list = tree.findItems(search_text, Qt.MatchFlag.MatchContains | Qt.MatchFlag.MatchRecursive)
            search_index = 0
            last_search = search_text
            if search_list:
                expand_and_scroll_to_item(search_list[search_index])
                search_index += 1
                
        return last_search, search_index, search_list
    
    def get_tree_item(self, tag: Tag) -> QTreeWidgetItem:
        item = QTreeWidgetItem([tag.name])
        for subTag in tag.sub_tags.values():
            item.addChild(self.get_tree_item(subTag))
        return item
    
    def load_tag_tree(self):
        """load tag tree from tag_tree.json and show it in the tree widget"""
        self.tag_tree = dataFn.load_tag_tree()
        self.viewTree.addTopLevelItem(self.get_tree_item(self.tag_tree.root))
        self.mainTree.addTopLevelItem(self.get_tree_item(self.tag_tree.root))
        
    def set_main_tree_ref(self):
        self.mainTree.set_tag_tree(self.tag_tree)
        self.mainTree.set_output_box(self.outputTextEdit)
        self.mainTree.set_list_widgets(self.newTagOrignalList, self.newTagTranslList, self.newTagStoreList)
        self.mainTree.set_check_box(self.tagMovingCheckBox)
        self.mainTree.set_view_tree(self.viewTree)
        self.mainTree.set_new_tag_list(self.newTagLst)
        
    def expand_top_level(self):
        self.viewTree.expandItem(self.viewTree.topLevelItem(0))
        for i in range(self.viewTree.topLevelItem(0).childCount()):
            self.viewTree.expandItem(self.viewTree.topLevelItem(0).child(i))
        self.mainTree.expandItem(self.mainTree.topLevelItem(0))
        for i in range(self.mainTree.topLevelItem(0).childCount()):
            self.mainTree.expandItem(self.mainTree.topLevelItem(0).child(i))

    def load_new_tag(self):
        """load new tag file and show it in the new tag lst"""
        self.newTagLst = dataFn.load_json("new_tag.json")
        newTagCount = 0
        for tagPair in self.newTagLst:
            if len(tagPair) > 2: # if the tag has been added to the tag tree, pass it
                continue
            if self.tag_tree.is_in_tree(tagPair[0]):
                if len(tagPair) == 2:
                    tagPair.append("added")
                continue
            self.newTagOrignalList.addItem(tagPair[0])
            new_trasl_item = QListWidgetItem(tagPair[1])
            new_trasl_item.setFlags(new_trasl_item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.newTagTranslList.addItem(new_trasl_item)
            newTagCount += 1
        
        self.outputTextEdit.append(f"new tag loaded, {newTagCount} tags in total")

    def show_tag_info(self):
        """show the tag info of the selected tag in the tag tree widget"""
        current_item = self.sender().currentItem()
        if current_item is None:
            return
    
        tag_name = current_item.text(0)
        tag = self.tag_tree.tag_dict[tag_name]
        
        self.tagInfo.clear()
    
        if not tag.is_tag:
            self.tagInfo.append("<b>类:</b> " + tag.name)
            self.tagInfo.append("<b>子标签:</b>")
            self.tagInfo.append(", ".join(tag.sub_tags.keys()))
        else:
            items = [
                ("标签名: ", tag.name),
                ("标签类型: ", tag.tag_type),
                ("同义标签: ", ", ".join(tag.synonyms)),
                ("父标签: ", ", ".join(tag.parent)),
                ("子标签: ", ", ".join(tag.sub_tags.keys()))
            ]
            for label, content in items:
                self.tagInfo.append(f"<b>{label}</b>{content}")
    
        self.tagInfo.verticalScrollBar().setValue(0)
    
    def save_tree(self):
        dataFn.write_json(self.tag_tree.to_dict(), "tag_tree.json")
        dataFn.write_json(self.newTagLst, "new_tag.json")
        self.outputTextEdit.append("标签树已保存")
        return

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()