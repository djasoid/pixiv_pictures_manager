# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'picture_manager.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDateEdit, QFrame,
    QGroupBox, QHBoxLayout, QHeaderView, QListWidget,
    QListWidgetItem, QMainWindow, QMenu, QMenuBar,
    QPlainTextEdit, QScrollArea, QSizePolicy, QSlider,
    QStatusBar, QTabWidget, QToolBox, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(999, 698)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_4 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.filterToolBox = QToolBox(self.centralwidget)
        self.filterToolBox.setObjectName(u"filterToolBox")
        self.filterToolBox.setMaximumSize(QSize(300, 16777215))
        self.tagSelector = QWidget()
        self.tagSelector.setObjectName(u"tagSelector")
        self.tagSelector.setGeometry(QRect(0, 0, 300, 541))
        self.verticalLayout = QVBoxLayout(self.tagSelector)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 0, -1, 0)
        self.tagTreeTabWidget = QTabWidget(self.tagSelector)
        self.tagTreeTabWidget.setObjectName(u"tagTreeTabWidget")
        self.tagTreeTabWidget.setTabPosition(QTabWidget.TabPosition.North)
        self.tagTreeTabWidget.setTabShape(QTabWidget.TabShape.Rounded)
        self.tagTreeTabWidget.setTabsClosable(False)
        self.characterTagTab = QWidget()
        self.characterTagTab.setObjectName(u"characterTagTab")
        self.verticalLayout_3 = QVBoxLayout(self.characterTagTab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.characterTagTree = QTreeWidget(self.characterTagTab)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.characterTagTree.setHeaderItem(__qtreewidgetitem)
        self.characterTagTree.setObjectName(u"characterTagTree")
        self.characterTagTree.header().setVisible(False)

        self.verticalLayout_3.addWidget(self.characterTagTree)

        self.tagTreeTabWidget.addTab(self.characterTagTab, "")
        self.attributeTagTab = QWidget()
        self.attributeTagTab.setObjectName(u"attributeTagTab")
        self.verticalLayout_4 = QVBoxLayout(self.attributeTagTab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.attributeTagTree = QTreeWidget(self.attributeTagTab)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setText(0, u"1");
        self.attributeTagTree.setHeaderItem(__qtreewidgetitem1)
        self.attributeTagTree.setObjectName(u"attributeTagTree")
        self.attributeTagTree.header().setVisible(False)

        self.verticalLayout_4.addWidget(self.attributeTagTree)

        self.tagTreeTabWidget.addTab(self.attributeTagTab, "")

        self.verticalLayout.addWidget(self.tagTreeTabWidget)

        self.searchTagTreeTextEdit = QPlainTextEdit(self.tagSelector)
        self.searchTagTreeTextEdit.setObjectName(u"searchTagTreeTextEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchTagTreeTextEdit.sizePolicy().hasHeightForWidth())
        self.searchTagTreeTextEdit.setSizePolicy(sizePolicy)
        self.searchTagTreeTextEdit.setMaximumSize(QSize(16777215, 30))
        self.searchTagTreeTextEdit.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.IBeamCursor))
        self.searchTagTreeTextEdit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.searchTagTreeTextEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.searchTagTreeTextEdit.setBackgroundVisible(False)
        self.searchTagTreeTextEdit.setCenterOnScroll(False)

        self.verticalLayout.addWidget(self.searchTagTreeTextEdit)

        self.filterToolBox.addItem(self.tagSelector, u"\u6807\u7b7e\u9009\u62e9")
        self.imageSelector = QWidget()
        self.imageSelector.setObjectName(u"imageSelector")
        self.imageSelector.setGeometry(QRect(0, 0, 300, 541))
        self.verticalLayout_5 = QVBoxLayout(self.imageSelector)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.fileTypeGroupBox = QGroupBox(self.imageSelector)
        self.fileTypeGroupBox.setObjectName(u"fileTypeGroupBox")
        self.checkBox = QCheckBox(self.fileTypeGroupBox)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(80, 40, 78, 19))
        self.checkBox_2 = QCheckBox(self.fileTypeGroupBox)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setGeometry(QRect(80, 80, 78, 19))
        self.checkBox_3 = QCheckBox(self.fileTypeGroupBox)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setGeometry(QRect(80, 120, 78, 19))

        self.verticalLayout_5.addWidget(self.fileTypeGroupBox)

        self.resolutionGroupBox = QGroupBox(self.imageSelector)
        self.resolutionGroupBox.setObjectName(u"resolutionGroupBox")
        self.resolutionWidthEdit = QPlainTextEdit(self.resolutionGroupBox)
        self.resolutionWidthEdit.setObjectName(u"resolutionWidthEdit")
        self.resolutionWidthEdit.setGeometry(QRect(10, 70, 104, 31))
        self.resolutionHightEdit = QPlainTextEdit(self.resolutionGroupBox)
        self.resolutionHightEdit.setObjectName(u"resolutionHightEdit")
        self.resolutionHightEdit.setGeometry(QRect(160, 70, 104, 31))

        self.verticalLayout_5.addWidget(self.resolutionGroupBox)

        self.timeGroupBox = QGroupBox(self.imageSelector)
        self.timeGroupBox.setObjectName(u"timeGroupBox")
        self.minDateEdit = QDateEdit(self.timeGroupBox)
        self.minDateEdit.setObjectName(u"minDateEdit")
        self.minDateEdit.setGeometry(QRect(10, 80, 120, 22))
        self.maxDateEdit = QDateEdit(self.timeGroupBox)
        self.maxDateEdit.setObjectName(u"maxDateEdit")
        self.maxDateEdit.setGeometry(QRect(150, 80, 120, 22))

        self.verticalLayout_5.addWidget(self.timeGroupBox)

        self.filterToolBox.addItem(self.imageSelector, u"\u56fe\u7247\u7b5b\u9009")
        self.imageSorter = QWidget()
        self.imageSorter.setObjectName(u"imageSorter")
        self.imageSorter.setGeometry(QRect(0, 0, 300, 541))
        self.verticalLayout_6 = QVBoxLayout(self.imageSorter)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.ratioGroupBox = QGroupBox(self.imageSorter)
        self.ratioGroupBox.setObjectName(u"ratioGroupBox")
        self.horizontalSlider = QSlider(self.ratioGroupBox)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setGeometry(QRect(60, 30, 160, 16))
        self.horizontalSlider.setToolTipDuration(2)
        self.horizontalSlider.setMinimum(-100)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setValue(0)
        self.horizontalSlider.setSliderPosition(0)
        self.horizontalSlider.setOrientation(Qt.Orientation.Horizontal)
        self.horizontalSlider.setInvertedAppearance(False)
        self.horizontalSlider.setInvertedControls(False)
        self.horizontalSlider.setTickPosition(QSlider.TickPosition.NoTicks)
        self.plainTextEdit_3 = QPlainTextEdit(self.ratioGroupBox)
        self.plainTextEdit_3.setObjectName(u"plainTextEdit_3")
        self.plainTextEdit_3.setGeometry(QRect(20, 90, 101, 41))
        self.plainTextEdit_4 = QPlainTextEdit(self.ratioGroupBox)
        self.plainTextEdit_4.setObjectName(u"plainTextEdit_4")
        self.plainTextEdit_4.setGeometry(QRect(160, 90, 101, 41))

        self.verticalLayout_6.addWidget(self.ratioGroupBox)

        self.priorityGroupBox = QGroupBox(self.imageSorter)
        self.priorityGroupBox.setObjectName(u"priorityGroupBox")
        self.listWidget = QListWidget(self.priorityGroupBox)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(30, 30, 221, 291))

        self.verticalLayout_6.addWidget(self.priorityGroupBox)

        self.verticalLayout_6.setStretch(0, 1)
        self.verticalLayout_6.setStretch(1, 2)
        self.filterToolBox.addItem(self.imageSorter, u"\u56fe\u7247\u6392\u5e8f")

        self.horizontalLayout_4.addWidget(self.filterToolBox)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.selectedTagFrame = QFrame(self.centralwidget)
        self.selectedTagFrame.setObjectName(u"selectedTagFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.selectedTagFrame.sizePolicy().hasHeightForWidth())
        self.selectedTagFrame.setSizePolicy(sizePolicy1)
        self.selectedTagFrame.setMinimumSize(QSize(0, 50))
        self.selectedTagFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.selectedTagFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.selectedTagFrame)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.includedTagWidget = QWidget(self.selectedTagFrame)
        self.includedTagWidget.setObjectName(u"includedTagWidget")

        self.horizontalLayout_5.addWidget(self.includedTagWidget)

        self.excludedTagWidget = QWidget(self.selectedTagFrame)
        self.excludedTagWidget.setObjectName(u"excludedTagWidget")

        self.horizontalLayout_5.addWidget(self.excludedTagWidget)


        self.verticalLayout_2.addWidget(self.selectedTagFrame)

        self.picBrowseScrollArea = QScrollArea(self.centralwidget)
        self.picBrowseScrollArea.setObjectName(u"picBrowseScrollArea")
        self.picBrowseScrollArea.setWidgetResizable(True)
        self.picBrowseContentWidget = QWidget()
        self.picBrowseContentWidget.setObjectName(u"picBrowseContentWidget")
        self.picBrowseContentWidget.setGeometry(QRect(0, 0, 671, 568))
        self.horizontalLayout_3 = QHBoxLayout(self.picBrowseContentWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.picBrowseWidget = QWidget(self.picBrowseContentWidget)
        self.picBrowseWidget.setObjectName(u"picBrowseWidget")

        self.horizontalLayout_3.addWidget(self.picBrowseWidget)

        self.picBrowseScrollArea.setWidget(self.picBrowseContentWidget)

        self.verticalLayout_2.addWidget(self.picBrowseScrollArea)


        self.horizontalLayout_4.addLayout(self.verticalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 999, 33))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        self.menu_3 = QMenu(self.menubar)
        self.menu_3.setObjectName(u"menu_3")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)

        self.filterToolBox.setCurrentIndex(0)
        self.tagTreeTabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.tagTreeTabWidget.setTabText(self.tagTreeTabWidget.indexOf(self.characterTagTab), QCoreApplication.translate("MainWindow", u"\u89d2\u8272", None))
        self.tagTreeTabWidget.setTabText(self.tagTreeTabWidget.indexOf(self.attributeTagTab), QCoreApplication.translate("MainWindow", u"\u5c5e\u6027", None))
        self.searchTagTreeTextEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u641c\u7d22\u6807\u7b7e", None))
        self.filterToolBox.setItemText(self.filterToolBox.indexOf(self.tagSelector), QCoreApplication.translate("MainWindow", u"\u6807\u7b7e\u9009\u62e9", None))
        self.fileTypeGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6\u683c\u5f0f", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"PNG", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"JPG", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"GIF", None))
        self.resolutionGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u5206\u8fa8\u7387", None))
        self.timeGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u65f6\u95f4\u8303\u56f4", None))
        self.filterToolBox.setItemText(self.filterToolBox.indexOf(self.imageSelector), QCoreApplication.translate("MainWindow", u"\u56fe\u7247\u7b5b\u9009", None))
        self.ratioGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u5bbd\u9ad8\u6bd4", None))
        self.priorityGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u6392\u5e8f\u4f18\u5148\u7ea7", None))
        self.filterToolBox.setItemText(self.filterToolBox.indexOf(self.imageSorter), QCoreApplication.translate("MainWindow", u"\u56fe\u7247\u6392\u5e8f", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
        self.menu_3.setTitle(QCoreApplication.translate("MainWindow", u"\u9009\u9879", None))
    # retranslateUi

