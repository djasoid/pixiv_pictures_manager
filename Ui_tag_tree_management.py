# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tag_tree_management.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QLayout, QListWidget, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QStatusBar,
    QTextEdit, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(890, 750)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QSize(16777215, 16777212))
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionUndo = QAction(MainWindow)
        self.actionUndo.setObjectName(u"actionUndo")
        self.actionRedo = QAction(MainWindow)
        self.actionRedo.setObjectName(u"actionRedo")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.tag_widget = QWidget(self.centralwidget)
        self.tag_widget.setObjectName(u"tag_widget")
        self.horizontalLayout_2 = QHBoxLayout(self.tag_widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.view_tree = QTreeWidget(self.tag_widget)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.view_tree.setHeaderItem(__qtreewidgetitem)
        self.view_tree.setObjectName(u"view_tree")
        self.view_tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.view_tree.setDragEnabled(True)
        self.view_tree.setDragDropMode(QAbstractItemView.DragOnly)
        self.view_tree.setAnimated(True)

        self.horizontalLayout_2.addWidget(self.view_tree)

        self.main_tree = QTreeWidget(self.tag_widget)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setText(0, u"1");
        self.main_tree.setHeaderItem(__qtreewidgetitem1)
        self.main_tree.setObjectName(u"main_tree")
        self.main_tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.main_tree.setDragDropMode(QAbstractItemView.DropOnly)
        self.main_tree.setAnimated(True)

        self.horizontalLayout_2.addWidget(self.main_tree)

        self.tag_edit_layout = QVBoxLayout()
        self.tag_edit_layout.setSpacing(0)
        self.tag_edit_layout.setObjectName(u"tag_edit_layout")
        self.tag_layout = QHBoxLayout()
        self.tag_layout.setSpacing(0)
        self.tag_layout.setObjectName(u"tag_layout")
        self.new_tag_transl_lst = QListWidget(self.tag_widget)
        self.new_tag_transl_lst.setObjectName(u"new_tag_transl_lst")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.new_tag_transl_lst.sizePolicy().hasHeightForWidth())
        self.new_tag_transl_lst.setSizePolicy(sizePolicy1)
        self.new_tag_transl_lst.setMaximumSize(QSize(150, 16777215))
        self.new_tag_transl_lst.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.new_tag_transl_lst.setDragEnabled(True)
        self.new_tag_transl_lst.setDragDropMode(QAbstractItemView.DragOnly)
        self.new_tag_transl_lst.setDefaultDropAction(Qt.CopyAction)

        self.tag_layout.addWidget(self.new_tag_transl_lst)

        self.new_tag_orignal_lst = QListWidget(self.tag_widget)
        self.new_tag_orignal_lst.setObjectName(u"new_tag_orignal_lst")
        sizePolicy1.setHeightForWidth(self.new_tag_orignal_lst.sizePolicy().hasHeightForWidth())
        self.new_tag_orignal_lst.setSizePolicy(sizePolicy1)
        self.new_tag_orignal_lst.setMaximumSize(QSize(150, 16777215))
        self.new_tag_orignal_lst.setDragEnabled(True)
        self.new_tag_orignal_lst.setDragDropMode(QAbstractItemView.DragOnly)

        self.tag_layout.addWidget(self.new_tag_orignal_lst)


        self.tag_edit_layout.addLayout(self.tag_layout)

        self.new_tag_store_lst = QListWidget(self.tag_widget)
        self.new_tag_store_lst.setObjectName(u"new_tag_store_lst")
        sizePolicy1.setHeightForWidth(self.new_tag_store_lst.sizePolicy().hasHeightForWidth())
        self.new_tag_store_lst.setSizePolicy(sizePolicy1)
        self.new_tag_store_lst.setMaximumSize(QSize(16777215, 100))
        self.new_tag_store_lst.setDragEnabled(True)
        self.new_tag_store_lst.setDragDropMode(QAbstractItemView.DragDrop)

        self.tag_edit_layout.addWidget(self.new_tag_store_lst)

        self.new_tag_input = QTextEdit(self.tag_widget)
        self.new_tag_input.setObjectName(u"new_tag_input")
        sizePolicy1.setHeightForWidth(self.new_tag_input.sizePolicy().hasHeightForWidth())
        self.new_tag_input.setSizePolicy(sizePolicy1)
        self.new_tag_input.setMaximumSize(QSize(16777215, 30))

        self.tag_edit_layout.addWidget(self.new_tag_input)


        self.horizontalLayout_2.addLayout(self.tag_edit_layout)


        self.verticalLayout.addWidget(self.tag_widget)

        self.info_widget = QWidget(self.centralwidget)
        self.info_widget.setObjectName(u"info_widget")
        self.info_widget.setMaximumSize(QSize(16777215, 100))
        self.info_layout = QHBoxLayout(self.info_widget)
        self.info_layout.setSpacing(0)
        self.info_layout.setObjectName(u"info_layout")
        self.info_layout.setSizeConstraint(QLayout.SetMaximumSize)
        self.info_layout.setContentsMargins(0, 0, 0, 0)
        self.tag_info = QTextEdit(self.info_widget)
        self.tag_info.setObjectName(u"tag_info")
        self.tag_info.setMaximumSize(QSize(16777215, 100))
        self.tag_info.setUndoRedoEnabled(False)
        self.tag_info.setReadOnly(True)

        self.info_layout.addWidget(self.tag_info)

        self.output_text = QTextEdit(self.info_widget)
        self.output_text.setObjectName(u"output_text")
        self.output_text.setMaximumSize(QSize(16777215, 100))
        self.output_text.setUndoRedoEnabled(False)
        self.output_text.setLineWrapColumnOrWidth(0)
        self.output_text.setReadOnly(True)

        self.info_layout.addWidget(self.output_text)


        self.verticalLayout.addWidget(self.info_widget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 890, 21))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menu.addAction(self.actionOpen)
        self.menu.addAction(self.actionSave)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionUndo.setText(QCoreApplication.translate("MainWindow", u"Undo", None))
        self.actionRedo.setText(QCoreApplication.translate("MainWindow", u"Redo", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
    # retranslateUi

