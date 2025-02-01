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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QSlider, QSpacerItem, QStatusBar,
    QTabWidget, QToolBox, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(940, 643)
        icon = QIcon()
        icon.addFile(u"res/image/icon/picture_manager.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.showRestrictedAction = QAction(MainWindow)
        self.showRestrictedAction.setObjectName(u"showRestrictedAction")
        self.showRestrictedAction.setCheckable(True)
        self.addNewPicsAction = QAction(MainWindow)
        self.addNewPicsAction.setObjectName(u"addNewPicsAction")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_4 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.filterToolBox = QToolBox(self.centralwidget)
        self.filterToolBox.setObjectName(u"filterToolBox")
        self.filterToolBox.setMaximumSize(QSize(250, 16777215))
        self.tagSelector = QWidget()
        self.tagSelector.setObjectName(u"tagSelector")
        self.tagSelector.setGeometry(QRect(0, 0, 250, 515))
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

        self.searchTagTreeTextEdit = QLineEdit(self.tagSelector)
        self.searchTagTreeTextEdit.setObjectName(u"searchTagTreeTextEdit")
        self.searchTagTreeTextEdit.setMinimumSize(QSize(0, 25))

        self.verticalLayout.addWidget(self.searchTagTreeTextEdit)

        self.filterToolBox.addItem(self.tagSelector, u"\u6807\u7b7e\u9009\u62e9")
        self.imageSelector = QWidget()
        self.imageSelector.setObjectName(u"imageSelector")
        self.imageSelector.setGeometry(QRect(0, 0, 213, 454))
        self.verticalLayout_5 = QVBoxLayout(self.imageSelector)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.filterGroupBox = QGroupBox(self.imageSelector)
        self.filterGroupBox.setObjectName(u"filterGroupBox")
        self.verticalLayout_6 = QVBoxLayout(self.filterGroupBox)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.filterGroupBox)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gifCheckBox = QCheckBox(self.filterGroupBox)
        self.gifCheckBox.setObjectName(u"gifCheckBox")
        self.gifCheckBox.setChecked(True)

        self.horizontalLayout.addWidget(self.gifCheckBox)

        self.jpgCheckBox = QCheckBox(self.filterGroupBox)
        self.jpgCheckBox.setObjectName(u"jpgCheckBox")
        self.jpgCheckBox.setChecked(True)

        self.horizontalLayout.addWidget(self.jpgCheckBox)

        self.pngCheckBox = QCheckBox(self.filterGroupBox)
        self.pngCheckBox.setObjectName(u"pngCheckBox")
        self.pngCheckBox.setChecked(True)

        self.horizontalLayout.addWidget(self.pngCheckBox)


        self.verticalLayout_6.addLayout(self.horizontalLayout)

        self.line = QFrame(self.filterGroupBox)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_6.addWidget(self.line)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_4 = QLabel(self.filterGroupBox)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_9.addWidget(self.label_4)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer)


        self.verticalLayout_6.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label = QLabel(self.filterGroupBox)
        self.label.setObjectName(u"label")

        self.horizontalLayout_6.addWidget(self.label)

        self.resolutionWidthEdit = QLineEdit(self.filterGroupBox)
        self.resolutionWidthEdit.setObjectName(u"resolutionWidthEdit")
        self.resolutionWidthEdit.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_6.addWidget(self.resolutionWidthEdit)


        self.verticalLayout_6.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_2 = QLabel(self.filterGroupBox)
        self.label_2.setObjectName(u"label_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)

        self.horizontalLayout_7.addWidget(self.label_2)

        self.resolutionHeightEdit = QLineEdit(self.filterGroupBox)
        self.resolutionHeightEdit.setObjectName(u"resolutionHeightEdit")
        self.resolutionHeightEdit.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_7.addWidget(self.resolutionHeightEdit)


        self.verticalLayout_6.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_3)

        self.clearResolutionPushButton = QPushButton(self.filterGroupBox)
        self.clearResolutionPushButton.setObjectName(u"clearResolutionPushButton")

        self.horizontalLayout_10.addWidget(self.clearResolutionPushButton)


        self.verticalLayout_6.addLayout(self.horizontalLayout_10)


        self.verticalLayout_5.addWidget(self.filterGroupBox)

        self.sortGroupBox = QGroupBox(self.imageSelector)
        self.sortGroupBox.setObjectName(u"sortGroupBox")
        self.verticalLayout_7 = QVBoxLayout(self.sortGroupBox)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_5 = QLabel(self.sortGroupBox)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_11.addWidget(self.label_5)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_4)

        self.enableRatioCheckBox = QCheckBox(self.sortGroupBox)
        self.enableRatioCheckBox.setObjectName(u"enableRatioCheckBox")

        self.horizontalLayout_11.addWidget(self.enableRatioCheckBox)


        self.verticalLayout_7.addLayout(self.horizontalLayout_11)

        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_7 = QLabel(self.sortGroupBox)
        self.label_7.setObjectName(u"label_7")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.label_7)

        self.label_8 = QLabel(self.sortGroupBox)
        self.label_8.setObjectName(u"label_8")
        sizePolicy1.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy1)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_5.addWidget(self.label_8)

        self.label_9 = QLabel(self.sortGroupBox)
        self.label_9.setObjectName(u"label_9")
        sizePolicy1.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy1)
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.label_9)


        self.verticalLayout_12.addLayout(self.horizontalLayout_5)

        self.ratioSlider = QSlider(self.sortGroupBox)
        self.ratioSlider.setObjectName(u"ratioSlider")
        self.ratioSlider.setMinimumSize(QSize(0, 20))
        self.ratioSlider.setToolTipDuration(2)
        self.ratioSlider.setStyleSheet(u"QSlider::sub-page:horizontal, QSlider::add-page:horizontal {\n"
"background: rgb(200,200,200);\n"
"}")
        self.ratioSlider.setMinimum(-40)
        self.ratioSlider.setMaximum(40)
        self.ratioSlider.setPageStep(1)
        self.ratioSlider.setValue(0)
        self.ratioSlider.setSliderPosition(0)
        self.ratioSlider.setOrientation(Qt.Orientation.Horizontal)
        self.ratioSlider.setInvertedAppearance(False)
        self.ratioSlider.setInvertedControls(False)
        self.ratioSlider.setTickPosition(QSlider.TickPosition.NoTicks)

        self.verticalLayout_12.addWidget(self.ratioSlider)


        self.verticalLayout_7.addLayout(self.verticalLayout_12)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.widthRatioSpinBox = QDoubleSpinBox(self.sortGroupBox)
        self.widthRatioSpinBox.setObjectName(u"widthRatioSpinBox")
        self.widthRatioSpinBox.setMinimumSize(QSize(0, 30))
        self.widthRatioSpinBox.setMaximum(100.000000000000000)
        self.widthRatioSpinBox.setSingleStep(1.000000000000000)
        self.widthRatioSpinBox.setValue(1.000000000000000)

        self.horizontalLayout_8.addWidget(self.widthRatioSpinBox)

        self.label_10 = QLabel(self.sortGroupBox)
        self.label_10.setObjectName(u"label_10")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy2)
        self.label_10.setMaximumSize(QSize(10, 16777215))
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_8.addWidget(self.label_10)

        self.heightRatioSpinBox = QDoubleSpinBox(self.sortGroupBox)
        self.heightRatioSpinBox.setObjectName(u"heightRatioSpinBox")
        self.heightRatioSpinBox.setMinimumSize(QSize(0, 30))
        self.heightRatioSpinBox.setMaximum(100.000000000000000)
        self.heightRatioSpinBox.setSingleStep(1.000000000000000)
        self.heightRatioSpinBox.setValue(1.000000000000000)

        self.horizontalLayout_8.addWidget(self.heightRatioSpinBox)


        self.verticalLayout_7.addLayout(self.horizontalLayout_8)

        self.line_2 = QFrame(self.sortGroupBox)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_7.addWidget(self.line_2)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_6 = QLabel(self.sortGroupBox)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_12.addWidget(self.label_6)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_5)


        self.verticalLayout_7.addLayout(self.horizontalLayout_12)

        self.sortComboBox = QComboBox(self.sortGroupBox)
        self.sortComboBox.setObjectName(u"sortComboBox")
        self.sortComboBox.setMinimumSize(QSize(0, 25))

        self.verticalLayout_7.addWidget(self.sortComboBox)


        self.verticalLayout_5.addWidget(self.sortGroupBox)

        self.verticalLayout_5.setStretch(0, 1)
        self.verticalLayout_5.setStretch(1, 1)
        self.filterToolBox.addItem(self.imageSelector, u"\u7b5b\u9009\u6392\u5e8f")

        self.horizontalLayout_4.addWidget(self.filterToolBox)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy3)
        self.scrollArea.setMinimumSize(QSize(0, 50))
        self.scrollArea.setMaximumSize(QSize(16777215, 50))
        self.scrollArea.setWidgetResizable(True)
        self.selectedTagScrollAreaWidgetContent = QWidget()
        self.selectedTagScrollAreaWidgetContent.setObjectName(u"selectedTagScrollAreaWidgetContent")
        self.selectedTagScrollAreaWidgetContent.setGeometry(QRect(0, 0, 662, 48))
        self.selectedTagLayout = QHBoxLayout(self.selectedTagScrollAreaWidgetContent)
        self.selectedTagLayout.setSpacing(5)
        self.selectedTagLayout.setObjectName(u"selectedTagLayout")
        self.selectedTagLayout.setContentsMargins(5, 5, 5, 5)
        self.scrollArea.setWidget(self.selectedTagScrollAreaWidgetContent)

        self.verticalLayout_2.addWidget(self.scrollArea)

        self.picBrowseScrollArea = QScrollArea(self.centralwidget)
        self.picBrowseScrollArea.setObjectName(u"picBrowseScrollArea")
        self.picBrowseScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.picBrowseScrollArea.setWidgetResizable(True)
        self.picBrowseContentWidget = QWidget()
        self.picBrowseContentWidget.setObjectName(u"picBrowseContentWidget")
        self.picBrowseContentWidget.setGeometry(QRect(0, 0, 662, 513))
        sizePolicy.setHeightForWidth(self.picBrowseContentWidget.sizePolicy().hasHeightForWidth())
        self.picBrowseContentWidget.setSizePolicy(sizePolicy)
        self.picDisplayLayout = QGridLayout(self.picBrowseContentWidget)
        self.picDisplayLayout.setObjectName(u"picDisplayLayout")
        self.picBrowseScrollArea.setWidget(self.picBrowseContentWidget)

        self.verticalLayout_2.addWidget(self.picBrowseScrollArea)


        self.horizontalLayout_4.addLayout(self.verticalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 940, 33))
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
        self.menu.addAction(self.addNewPicsAction)
        self.menu_3.addAction(self.showRestrictedAction)

        self.retranslateUi(MainWindow)

        self.filterToolBox.setCurrentIndex(0)
        self.tagTreeTabWidget.setCurrentIndex(0)
        self.sortComboBox.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Pixiv\u56fe\u7247\u7ba1\u7406", None))
        self.showRestrictedAction.setText(QCoreApplication.translate("MainWindow", u"R-18", None))
        self.addNewPicsAction.setText(QCoreApplication.translate("MainWindow", u"\u6dfb\u52a0\u65b0\u56fe\u7247...", None))
        self.tagTreeTabWidget.setTabText(self.tagTreeTabWidget.indexOf(self.characterTagTab), QCoreApplication.translate("MainWindow", u"\u89d2\u8272", None))
        self.tagTreeTabWidget.setTabText(self.tagTreeTabWidget.indexOf(self.attributeTagTab), QCoreApplication.translate("MainWindow", u"\u5c5e\u6027", None))
        self.searchTagTreeTextEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u641c\u7d22\u6807\u7b7e", None))
        self.filterToolBox.setItemText(self.filterToolBox.indexOf(self.tagSelector), QCoreApplication.translate("MainWindow", u"\u6807\u7b7e\u9009\u62e9", None))
        self.filterGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u7b5b\u9009", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6\u683c\u5f0f", None))
        self.gifCheckBox.setText(QCoreApplication.translate("MainWindow", u"GIF", None))
        self.jpgCheckBox.setText(QCoreApplication.translate("MainWindow", u"JPG", None))
        self.pngCheckBox.setText(QCoreApplication.translate("MainWindow", u"PNG", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u5206\u8fa8\u7387", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u5bbd\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u9ad8\uff1a", None))
        self.clearResolutionPushButton.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u7a7a", None))
        self.sortGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u6392\u5e8f", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u5bbd\u9ad8\u6bd4", None))
        self.enableRatioCheckBox.setText(QCoreApplication.translate("MainWindow", u"\u542f\u7528", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u5bbd\u56fe", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u6b63\u65b9\u56fe", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u957f\u56fe", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u":", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u6392\u5217\u987a\u5e8f", None))
        self.sortComboBox.setCurrentText("")
        self.filterToolBox.setItemText(self.filterToolBox.indexOf(self.imageSelector), QCoreApplication.translate("MainWindow", u"\u7b5b\u9009\u6392\u5e8f", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
        self.menu_3.setTitle(QCoreApplication.translate("MainWindow", u"\u9009\u9879", None))
    # retranslateUi

