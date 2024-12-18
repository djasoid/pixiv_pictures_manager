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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDateEdit, QDoubleSpinBox,
    QFrame, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QListWidget, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QPlainTextEdit, QPushButton,
    QScrollArea, QSizePolicy, QSlider, QStatusBar,
    QTabWidget, QToolBox, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(955, 661)
        self.actionR_18 = QAction(MainWindow)
        self.actionR_18.setObjectName(u"actionR_18")
        self.action = QAction(MainWindow)
        self.action.setObjectName(u"action")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_4 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.filterToolBox = QToolBox(self.centralwidget)
        self.filterToolBox.setObjectName(u"filterToolBox")
        self.filterToolBox.setMaximumSize(QSize(300, 16777215))
        self.tagSelector = QWidget()
        self.tagSelector.setObjectName(u"tagSelector")
        self.tagSelector.setGeometry(QRect(0, 0, 300, 504))
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
        self.searchTagTreeTextEdit.setMaximumSize(QSize(16777215, 25))
        self.searchTagTreeTextEdit.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.IBeamCursor))
        self.searchTagTreeTextEdit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.searchTagTreeTextEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.searchTagTreeTextEdit.setBackgroundVisible(False)
        self.searchTagTreeTextEdit.setCenterOnScroll(False)

        self.verticalLayout.addWidget(self.searchTagTreeTextEdit)

        self.filterToolBox.addItem(self.tagSelector, u"\u6807\u7b7e\u9009\u62e9")
        self.imageSelector = QWidget()
        self.imageSelector.setObjectName(u"imageSelector")
        self.imageSelector.setGeometry(QRect(0, 0, 300, 504))
        self.verticalLayout_5 = QVBoxLayout(self.imageSelector)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.fileTypeGroupBox = QGroupBox(self.imageSelector)
        self.fileTypeGroupBox.setObjectName(u"fileTypeGroupBox")
        self.verticalLayout_10 = QVBoxLayout(self.fileTypeGroupBox)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(100, -1, -1, -1)
        self.pngCheckBox = QCheckBox(self.fileTypeGroupBox)
        self.pngCheckBox.setObjectName(u"pngCheckBox")
        self.pngCheckBox.setChecked(True)

        self.verticalLayout_10.addWidget(self.pngCheckBox)

        self.jpgCheckBox = QCheckBox(self.fileTypeGroupBox)
        self.jpgCheckBox.setObjectName(u"jpgCheckBox")
        self.jpgCheckBox.setChecked(True)

        self.verticalLayout_10.addWidget(self.jpgCheckBox)

        self.gifCheckBox = QCheckBox(self.fileTypeGroupBox)
        self.gifCheckBox.setObjectName(u"gifCheckBox")
        self.gifCheckBox.setChecked(True)

        self.verticalLayout_10.addWidget(self.gifCheckBox)


        self.verticalLayout_5.addWidget(self.fileTypeGroupBox)

        self.resolutionGroupBox = QGroupBox(self.imageSelector)
        self.resolutionGroupBox.setObjectName(u"resolutionGroupBox")
        self.pushButton_3 = QPushButton(self.resolutionGroupBox)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(190, 120, 75, 23))
        self.layoutWidget = QWidget(self.resolutionGroupBox)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(50, 40, 171, 31))
        self.horizontalLayout_6 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_6.addWidget(self.label)

        self.resolutionWidthEdit = QPlainTextEdit(self.layoutWidget)
        self.resolutionWidthEdit.setObjectName(u"resolutionWidthEdit")

        self.horizontalLayout_6.addWidget(self.resolutionWidthEdit)

        self.layoutWidget1 = QWidget(self.resolutionGroupBox)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(50, 80, 171, 31))
        self.horizontalLayout_7 = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.layoutWidget1)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_7.addWidget(self.label_2)

        self.resolutionHightEdit = QPlainTextEdit(self.layoutWidget1)
        self.resolutionHightEdit.setObjectName(u"resolutionHightEdit")

        self.horizontalLayout_7.addWidget(self.resolutionHightEdit)


        self.verticalLayout_5.addWidget(self.resolutionGroupBox)

        self.timeGroupBox = QGroupBox(self.imageSelector)
        self.timeGroupBox.setObjectName(u"timeGroupBox")
        self.minDateEdit = QDateEdit(self.timeGroupBox)
        self.minDateEdit.setObjectName(u"minDateEdit")
        self.minDateEdit.setGeometry(QRect(10, 80, 120, 22))
        self.maxDateEdit = QDateEdit(self.timeGroupBox)
        self.maxDateEdit.setObjectName(u"maxDateEdit")
        self.maxDateEdit.setGeometry(QRect(150, 80, 120, 22))
        self.checkBox_2 = QCheckBox(self.timeGroupBox)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setGeometry(QRect(20, 40, 78, 19))

        self.verticalLayout_5.addWidget(self.timeGroupBox)

        self.filterToolBox.addItem(self.imageSelector, u"\u56fe\u7247\u7b5b\u9009")
        self.imageSorter = QWidget()
        self.imageSorter.setObjectName(u"imageSorter")
        self.imageSorter.setGeometry(QRect(0, 0, 300, 504))
        self.verticalLayout_6 = QVBoxLayout(self.imageSorter)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.ratioGroupBox = QGroupBox(self.imageSorter)
        self.ratioGroupBox.setObjectName(u"ratioGroupBox")
        self.verticalLayout_9 = QVBoxLayout(self.ratioGroupBox)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(20, 10, 20, 20)
        self.checkBox = QCheckBox(self.ratioGroupBox)
        self.checkBox.setObjectName(u"checkBox")

        self.verticalLayout_9.addWidget(self.checkBox)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.ratioGroupBox)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.label_3)

        self.label_4 = QLabel(self.ratioGroupBox)
        self.label_4.setObjectName(u"label_4")
        sizePolicy1.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy1)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_4)

        self.label_5 = QLabel(self.ratioGroupBox)
        self.label_5.setObjectName(u"label_5")
        sizePolicy1.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy1)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label_5)


        self.verticalLayout_7.addLayout(self.horizontalLayout_2)

        self.horizontalSlider = QSlider(self.ratioGroupBox)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setMinimumSize(QSize(0, 20))
        self.horizontalSlider.setToolTipDuration(2)
        self.horizontalSlider.setMinimum(-100)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setValue(0)
        self.horizontalSlider.setSliderPosition(0)
        self.horizontalSlider.setOrientation(Qt.Orientation.Horizontal)
        self.horizontalSlider.setInvertedAppearance(False)
        self.horizontalSlider.setInvertedControls(False)
        self.horizontalSlider.setTickPosition(QSlider.TickPosition.NoTicks)

        self.verticalLayout_7.addWidget(self.horizontalSlider)


        self.verticalLayout_9.addLayout(self.verticalLayout_7)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.doubleSpinBox = QDoubleSpinBox(self.ratioGroupBox)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        self.doubleSpinBox.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.doubleSpinBox)

        self.label_6 = QLabel(self.ratioGroupBox)
        self.label_6.setObjectName(u"label_6")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy2)
        self.label_6.setMaximumSize(QSize(10, 16777215))
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label_6)

        self.doubleSpinBox_2 = QDoubleSpinBox(self.ratioGroupBox)
        self.doubleSpinBox_2.setObjectName(u"doubleSpinBox_2")
        self.doubleSpinBox_2.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.doubleSpinBox_2)


        self.verticalLayout_9.addLayout(self.horizontalLayout)


        self.verticalLayout_6.addWidget(self.ratioGroupBox)

        self.sortPriorityGroupBox = QGroupBox(self.imageSorter)
        self.sortPriorityGroupBox.setObjectName(u"sortPriorityGroupBox")
        self.verticalLayout_8 = QVBoxLayout(self.sortPriorityGroupBox)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(20, 20, 20, 20)
        self.listWidget = QListWidget(self.sortPriorityGroupBox)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout_8.addWidget(self.listWidget)

        self.pushButton_2 = QPushButton(self.sortPriorityGroupBox)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout_8.addWidget(self.pushButton_2)


        self.verticalLayout_6.addWidget(self.sortPriorityGroupBox)

        self.verticalLayout_6.setStretch(0, 1)
        self.verticalLayout_6.setStretch(1, 2)
        self.filterToolBox.addItem(self.imageSorter, u"\u56fe\u7247\u6392\u5e8f")

        self.horizontalLayout_4.addWidget(self.filterToolBox)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.selectedTagFrame = QFrame(self.centralwidget)
        self.selectedTagFrame.setObjectName(u"selectedTagFrame")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.selectedTagFrame.sizePolicy().hasHeightForWidth())
        self.selectedTagFrame.setSizePolicy(sizePolicy3)
        self.selectedTagFrame.setMinimumSize(QSize(0, 50))
        self.selectedTagFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.selectedTagFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.selectedTagLayout = QHBoxLayout(self.selectedTagFrame)
        self.selectedTagLayout.setObjectName(u"selectedTagLayout")

        self.verticalLayout_2.addWidget(self.selectedTagFrame)

        self.picBrowseScrollArea = QScrollArea(self.centralwidget)
        self.picBrowseScrollArea.setObjectName(u"picBrowseScrollArea")
        self.picBrowseScrollArea.setWidgetResizable(True)
        self.picBrowseContentWidget = QWidget()
        self.picBrowseContentWidget.setObjectName(u"picBrowseContentWidget")
        self.picBrowseContentWidget.setGeometry(QRect(0, 0, 627, 531))
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
        self.menubar.setGeometry(QRect(0, 0, 955, 33))
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
        self.menu.addAction(self.action)
        self.menu_3.addAction(self.actionR_18)

        self.retranslateUi(MainWindow)

        self.filterToolBox.setCurrentIndex(2)
        self.tagTreeTabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionR_18.setText(QCoreApplication.translate("MainWindow", u"R-18", None))
        self.action.setText(QCoreApplication.translate("MainWindow", u"\u6dfb\u52a0\u6587\u4ef6\u5939", None))
        self.tagTreeTabWidget.setTabText(self.tagTreeTabWidget.indexOf(self.characterTagTab), QCoreApplication.translate("MainWindow", u"\u89d2\u8272", None))
        self.tagTreeTabWidget.setTabText(self.tagTreeTabWidget.indexOf(self.attributeTagTab), QCoreApplication.translate("MainWindow", u"\u5c5e\u6027", None))
        self.searchTagTreeTextEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u641c\u7d22\u6807\u7b7e", None))
        self.filterToolBox.setItemText(self.filterToolBox.indexOf(self.tagSelector), QCoreApplication.translate("MainWindow", u"\u6807\u7b7e\u9009\u62e9", None))
        self.fileTypeGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6\u683c\u5f0f", None))
        self.pngCheckBox.setText(QCoreApplication.translate("MainWindow", u"PNG", None))
        self.jpgCheckBox.setText(QCoreApplication.translate("MainWindow", u"JPG", None))
        self.gifCheckBox.setText(QCoreApplication.translate("MainWindow", u"GIF", None))
        self.resolutionGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u5206\u8fa8\u7387", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u7a7a", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u5bbd\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u9ad8\uff1a", None))
        self.timeGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u65f6\u95f4\u8303\u56f4", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"\u542f\u7528", None))
        self.filterToolBox.setItemText(self.filterToolBox.indexOf(self.imageSelector), QCoreApplication.translate("MainWindow", u"\u56fe\u7247\u7b5b\u9009", None))
        self.ratioGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u5bbd\u9ad8\u6bd4", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"\u542f\u7528", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u5bbd\u56fe", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u6b63\u65b9\u56fe", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u957f\u56fe", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u":", None))
        self.sortPriorityGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u6392\u5e8f\u4f18\u5148\u7ea7", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u7f6e", None))
        self.filterToolBox.setItemText(self.filterToolBox.indexOf(self.imageSorter), QCoreApplication.translate("MainWindow", u"\u56fe\u7247\u6392\u5e8f", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
        self.menu_3.setTitle(QCoreApplication.translate("MainWindow", u"\u9009\u9879", None))
    # retranslateUi

