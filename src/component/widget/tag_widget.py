from typing import TYPE_CHECKING

from PySide6.QtWidgets import QPushButton , QWidget

if TYPE_CHECKING:
    from controller.picture_manager import PictureManagerController

class TagWidget(QPushButton):
    def __init__(self, parent: QWidget , controller: 'PictureManagerController', tag_name: str, include: bool):
        super().__init__(tag_name, parent)
        self.tag_name = tag_name
        self.controller = controller
        self.include = include
        if self.include:
            self.setStyleSheet("background-color: green")
        else:
            self.setStyleSheet("background-color: red")
        self.setText(tag_name)
        self.clicked.connect(lambda: self.controller.remove_selected_tag(self))