from typing import TYPE_CHECKING

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QListWidgetItem, QTreeWidget, QTreeWidgetItem, QAbstractItemView
from PySide6.QtGui import QKeySequence, QShortcut, QTextCursor, QTextCharFormat, QFont

from ui_compiled.Ui_picture_manager import Ui_MainWindow
from controller.picture_manager import PictureManagerController

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    def setup_controller(self, controller: PictureManagerController):
        self.controller = controller
        self.bind()                    
        
    def bind(self):
        # install event filter
        self.searchTagTreeTextEdit.installEventFilter(self)

        # tag tree item click event
        self.characterTagTree.itemClicked.connect(self.controller.add_include_tag)
        self.attributeTagTree.itemClicked.connect(self.controller.add_include_tag)
        self.characterTagTree.itemDoubleClicked.connect(self.controller.add_exclude_tag)
        self.attributeTagTree.itemDoubleClicked.connect(self.controller.add_exclude_tag)

        # file type selection event
        self.jpgCheckBox.stateChanged.connect(self.controller.filter_pic_files)
        self.pngCheckBox.stateChanged.connect(self.controller.filter_pic_files)
        self.gifCheckBox.stateChanged.connect(self.controller.filter_pic_files)
        
        # resolution selection event
        self.resolutionHeightEdit.textChanged.connect(self.controller.filter_pic_files)
        self.resolutionWidthEdit.textChanged.connect(self.controller.filter_pic_files)
        self.clearResolutionPushButton.clicked.connect(self.controller.clear_resolution_filter)

        # ratio sort event
        self.enableRatioCheckBox.checkStateChanged.connect(self.controller.ratio_spin_box_sort)
        self.widthRatioSpinBox.valueChanged.connect(self.controller.ratio_spin_box_sort)
        self.heightRatioSpinBox.valueChanged.connect(self.controller.ratio_spin_box_sort)
        self.ratioSlider.valueChanged.connect(self.controller.ratio_slider_sort)

    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        # Filter for tag_search_edit, implement enter to search tag
        if (source == self.searchTagTreeTextEdit and event.type() == QEvent.Type.KeyPress):
            if event.key() == Qt.Key.Key_Return:
                self.controller.tag_search(self.searchTagTreeTextEdit.toPlainText())
                return True
        
        return super().eventFilter(source, event)