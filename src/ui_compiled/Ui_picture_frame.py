# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'picture_frame.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_pictureFrame(object):
    def setupUi(self, pictureFrame):
        if not pictureFrame.objectName():
            pictureFrame.setObjectName(u"pictureFrame")
        pictureFrame.resize(250, 325)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pictureFrame.sizePolicy().hasHeightForWidth())
        pictureFrame.setSizePolicy(sizePolicy)
        pictureFrame.setMinimumSize(QSize(250, 325))
        pictureFrame.setMaximumSize(QSize(250, 325))
        pictureFrame.setFrameShape(QFrame.Shape.Box)
        self.verticalLayout_2 = QVBoxLayout(pictureFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.imageLabel = QLabel(pictureFrame)
        self.imageLabel.setObjectName(u"imageLabel")
        sizePolicy.setHeightForWidth(self.imageLabel.sizePolicy().hasHeightForWidth())
        self.imageLabel.setSizePolicy(sizePolicy)
        self.imageLabel.setMinimumSize(QSize(232, 218))
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.imageLabel)

        self.picInfoWidget = QWidget(pictureFrame)
        self.picInfoWidget.setObjectName(u"picInfoWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.picInfoWidget.sizePolicy().hasHeightForWidth())
        self.picInfoWidget.setSizePolicy(sizePolicy1)
        self.picInfoWidget.setMaximumSize(QSize(16777215, 86))
        self.verticalLayout = QVBoxLayout(self.picInfoWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.titleLabel = QLabel(self.picInfoWidget)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setMinimumSize(QSize(0, 35))

        self.horizontalLayout_3.addWidget(self.titleLabel)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.illustratorLabel = QLabel(self.picInfoWidget)
        self.illustratorLabel.setObjectName(u"illustratorLabel")
        self.illustratorLabel.setMinimumSize(QSize(0, 20))

        self.horizontalLayout.addWidget(self.illustratorLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.resolutionLabel = QLabel(self.picInfoWidget)
        self.resolutionLabel.setObjectName(u"resolutionLabel")
        self.resolutionLabel.setMinimumSize(QSize(0, 20))

        self.horizontalLayout.addWidget(self.resolutionLabel)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pidLabel = QLabel(self.picInfoWidget)
        self.pidLabel.setObjectName(u"pidLabel")
        self.pidLabel.setMinimumSize(QSize(0, 20))

        self.horizontalLayout_2.addWidget(self.pidLabel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.fileTypeAndSizeLabel = QLabel(self.picInfoWidget)
        self.fileTypeAndSizeLabel.setObjectName(u"fileTypeAndSizeLabel")
        self.fileTypeAndSizeLabel.setMinimumSize(QSize(0, 20))

        self.horizontalLayout_2.addWidget(self.fileTypeAndSizeLabel)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_2.addWidget(self.picInfoWidget)


        self.retranslateUi(pictureFrame)

        QMetaObject.connectSlotsByName(pictureFrame)
    # setupUi

    def retranslateUi(self, pictureFrame):
        pictureFrame.setWindowTitle(QCoreApplication.translate("pictureFrame", u"Frame", None))
        self.imageLabel.setText(QCoreApplication.translate("pictureFrame", u"Image", None))
        self.titleLabel.setText("")
        self.illustratorLabel.setText("")
        self.resolutionLabel.setText("")
        self.pidLabel.setText("")
        self.fileTypeAndSizeLabel.setText("")
    # retranslateUi

