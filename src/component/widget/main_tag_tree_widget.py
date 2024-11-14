from typing import TYPE_CHECKING

from PySide6.QtWidgets import QTextEdit, QTreeWidget, QTreeWidgetItem, QListWidget, QMenu, QDialog, QCheckBox, QAbstractItemView
from PySide6.QtGui import QContextMenuEvent, QFont, QAction
from PySide6.QtCore import QByteArray, Qt

if TYPE_CHECKING:
    from controller.tag_management import TagManagementController as Controller

class MainTagTreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_controller(self, controller: 'Controller'):
        self.controller = controller

    def dropEvent(self, event):
        """handle drop event and make changes to the tag tree"""
        self.controller.mainTree_drop_event(event)
    
    def contextMenuEvent(self, event: QContextMenuEvent):
        """show context menu when right click"""
        current_item = self.itemAt(event.pos())

        context_menu = QMenu(self)
        context_menu.addAction(QAction("在view tree中展开", self, triggered=lambda: self.controller.show_in_view_tree()))
        context_menu.addAction(QAction("编辑标签", self, triggered=lambda: self.controller.edit_tag(current_item.text(0))))
        context_menu.addAction(QAction("删除标签", self, triggered=lambda: self.controller.confirm_delete(current_item)))
        context_menu.exec_(event.globalPos())