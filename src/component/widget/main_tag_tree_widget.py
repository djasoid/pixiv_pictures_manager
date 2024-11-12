from PySide6.QtWidgets import QTextEdit, QTreeWidget, QTreeWidgetItem, QListWidget, QMenu, QDialog, QCheckBox
from PySide6.QtGui import QContextMenuEvent, QFont, QAction
from PySide6.QtCore import QByteArray, Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controller.tag_management import TagManagementController

class MainTagTreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_controller(self, controller: 'TagManagementController'):
        self.controller = controller

    def dropEvent(self, event):
        """handle drop event and make changes to the tag tree"""
        self.controller.handle_drop_event(event)
    
    def contextMenuEvent(self, event: QContextMenuEvent):
        """show context menu when right click"""
        currentItem = self.itemAt(event.pos())
        parentItem = currentItem.parent()
        tagName = currentItem.text(0)
        parentTagName = parentItem.text(0)
        contextMenu = QMenu(self)
        contextMenu.addAction(QAction("在view tree中展开", self, triggered=lambda: self.controller.show_in_view_tree()))
        contextMenu.addAction(QAction("编辑标签", self, triggered=lambda: self.controller.synonym_edit(tagName)))
        contextMenu.addAction(QAction("删除标签", self, triggered=lambda: self.controller.confirm_delete(tagName, parentTagName, currentItem, parentItem)))
        contextMenu.exec_(event.globalPos())