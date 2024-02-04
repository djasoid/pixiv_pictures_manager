# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tag_tree_management.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QHBoxLayout,
    QHeaderView, QLayout, QListWidget, QListWidgetItem,
    QMainWindow, QMenu, QMenuBar, QSizePolicy,
    QStatusBar, QTextEdit, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

from custom_widget import MainTagTreeWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(921, 750)
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
        self.tagWidget = QWidget(self.centralwidget)
        self.tagWidget.setObjectName(u"tagWidget")
        self.horizontalLayout = QHBoxLayout(self.tagWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.viewTreeLayout = QVBoxLayout()
        self.viewTreeLayout.setSpacing(0)
        self.viewTreeLayout.setObjectName(u"viewTreeLayout")
        self.viewTreeLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.viewTree = QTreeWidget(self.tagWidget)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.viewTree.setHeaderItem(__qtreewidgetitem)
        self.viewTree.setObjectName(u"viewTree")
        self.viewTree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.viewTree.setProperty("showDropIndicator", False)
        self.viewTree.setDragEnabled(True)
        self.viewTree.setDragDropMode(QAbstractItemView.DragOnly)
        self.viewTree.setAnimated(True)
        self.viewTree.setHeaderHidden(True)
        self.viewTree.setColumnCount(1)

        self.viewTreeLayout.addWidget(self.viewTree)

        self.viewTreeSearchWidget = QWidget(self.tagWidget)
        self.viewTreeSearchWidget.setObjectName(u"viewTreeSearchWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.viewTreeSearchWidget.sizePolicy().hasHeightForWidth())
        self.viewTreeSearchWidget.setSizePolicy(sizePolicy1)
        self.viewTreeSearchWidget.setMinimumSize(QSize(0, 30))
        self.viewTreeSearchWidget.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout_2 = QHBoxLayout(self.viewTreeSearchWidget)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.viewTreeSearchEdit = QTextEdit(self.viewTreeSearchWidget)
        self.viewTreeSearchEdit.setObjectName(u"viewTreeSearchEdit")
        self.viewTreeSearchEdit.setMaximumSize(QSize(16777215, 30))
        self.viewTreeSearchEdit.setAcceptRichText(False)

        self.horizontalLayout_2.addWidget(self.viewTreeSearchEdit)

        self.tagMovingCheckBox = QCheckBox(self.viewTreeSearchWidget)
        self.tagMovingCheckBox.setObjectName(u"tagMovingCheckBox")

        self.horizontalLayout_2.addWidget(self.tagMovingCheckBox)


        self.viewTreeLayout.addWidget(self.viewTreeSearchWidget)


        self.horizontalLayout.addLayout(self.viewTreeLayout)

        self.mainTreeLayout = QVBoxLayout()
        self.mainTreeLayout.setSpacing(0)
        self.mainTreeLayout.setObjectName(u"mainTreeLayout")
        self.mainTree = MainTagTreeWidget(self.tagWidget)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setText(0, u"1");
        self.mainTree.setHeaderItem(__qtreewidgetitem1)
        self.mainTree.setObjectName(u"mainTree")
        self.mainTree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.mainTree.setDragDropMode(QAbstractItemView.DropOnly)
        self.mainTree.setAnimated(True)
        self.mainTree.setHeaderHidden(True)
        self.mainTree.setColumnCount(1)

        self.mainTreeLayout.addWidget(self.mainTree)

        self.mainTreeSearchEdit = QTextEdit(self.tagWidget)
        self.mainTreeSearchEdit.setObjectName(u"mainTreeSearchEdit")
        self.mainTreeSearchEdit.setMaximumSize(QSize(16777215, 30))
        self.mainTreeSearchEdit.setAcceptRichText(False)

        self.mainTreeLayout.addWidget(self.mainTreeSearchEdit)


        self.horizontalLayout.addLayout(self.mainTreeLayout)

        self.tagEditLayout = QVBoxLayout()
        self.tagEditLayout.setSpacing(0)
        self.tagEditLayout.setObjectName(u"tagEditLayout")
        self.newTagLayout = QHBoxLayout()
        self.newTagLayout.setSpacing(0)
        self.newTagLayout.setObjectName(u"newTagLayout")
        self.newTagTranslList = QListWidget(self.tagWidget)
        self.newTagTranslList.setObjectName(u"newTagTranslList")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.newTagTranslList.sizePolicy().hasHeightForWidth())
        self.newTagTranslList.setSizePolicy(sizePolicy2)
        self.newTagTranslList.setMaximumSize(QSize(150, 16777215))
        self.newTagTranslList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.newTagTranslList.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.newTagTranslList.setDragEnabled(True)
        self.newTagTranslList.setDragDropMode(QAbstractItemView.DragOnly)
        self.newTagTranslList.setDefaultDropAction(Qt.CopyAction)

        self.newTagLayout.addWidget(self.newTagTranslList)

        self.newTagOrignalList = QListWidget(self.tagWidget)
        self.newTagOrignalList.setObjectName(u"newTagOrignalList")
        sizePolicy2.setHeightForWidth(self.newTagOrignalList.sizePolicy().hasHeightForWidth())
        self.newTagOrignalList.setSizePolicy(sizePolicy2)
        self.newTagOrignalList.setMaximumSize(QSize(150, 16777215))
        self.newTagOrignalList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.newTagOrignalList.setDragEnabled(True)
        self.newTagOrignalList.setDragDropMode(QAbstractItemView.DragOnly)

        self.newTagLayout.addWidget(self.newTagOrignalList)


        self.tagEditLayout.addLayout(self.newTagLayout)

        self.newTagStoreList = QListWidget(self.tagWidget)
        self.newTagStoreList.setObjectName(u"newTagStoreList")
        sizePolicy2.setHeightForWidth(self.newTagStoreList.sizePolicy().hasHeightForWidth())
        self.newTagStoreList.setSizePolicy(sizePolicy2)
        self.newTagStoreList.setMaximumSize(QSize(16777215, 100))
        self.newTagStoreList.setDragEnabled(True)
        self.newTagStoreList.setDragDropMode(QAbstractItemView.DragDrop)

        self.tagEditLayout.addWidget(self.newTagStoreList)

        self.newTagInput = QTextEdit(self.tagWidget)
        self.newTagInput.setObjectName(u"newTagInput")
        sizePolicy2.setHeightForWidth(self.newTagInput.sizePolicy().hasHeightForWidth())
        self.newTagInput.setSizePolicy(sizePolicy2)
        self.newTagInput.setMaximumSize(QSize(16777215, 30))
        self.newTagInput.setAcceptRichText(False)

        self.tagEditLayout.addWidget(self.newTagInput)


        self.horizontalLayout.addLayout(self.tagEditLayout)


        self.verticalLayout.addWidget(self.tagWidget)

        self.infoWidget = QWidget(self.centralwidget)
        self.infoWidget.setObjectName(u"infoWidget")
        self.infoWidget.setMaximumSize(QSize(16777215, 100))
        self.info_layout = QHBoxLayout(self.infoWidget)
        self.info_layout.setSpacing(0)
        self.info_layout.setObjectName(u"info_layout")
        self.info_layout.setSizeConstraint(QLayout.SetMaximumSize)
        self.info_layout.setContentsMargins(0, 0, 0, 0)
        self.tagInfo = QTextEdit(self.infoWidget)
        self.tagInfo.setObjectName(u"tagInfo")
        self.tagInfo.setMaximumSize(QSize(16777215, 100))
        self.tagInfo.setUndoRedoEnabled(False)
        self.tagInfo.setReadOnly(True)

        self.info_layout.addWidget(self.tagInfo)

        self.outputTextEdit = QTextEdit(self.infoWidget)
        self.outputTextEdit.setObjectName(u"outputTextEdit")
        self.outputTextEdit.setMaximumSize(QSize(16777215, 100))
        self.outputTextEdit.setUndoRedoEnabled(False)
        self.outputTextEdit.setLineWrapColumnOrWidth(0)
        self.outputTextEdit.setReadOnly(True)

        self.info_layout.addWidget(self.outputTextEdit)


        self.verticalLayout.addWidget(self.infoWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 921, 21))
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
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u6807\u7b7e\u7ba1\u7406", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionUndo.setText(QCoreApplication.translate("MainWindow", u"Undo", None))
        self.actionRedo.setText(QCoreApplication.translate("MainWindow", u"Redo", None))
        self.tagMovingCheckBox.setText(QCoreApplication.translate("MainWindow", u"\u79fb\u52a8\u6807\u7b7e", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
    # retranslateUi

