# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'delete_tag_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QSizePolicy, QWidget)

class Ui_delete_tag_dialog(object):
    def setupUi(self, delete_tag_dialog):
        if not delete_tag_dialog.objectName():
            delete_tag_dialog.setObjectName(u"delete_tag_dialog")
        delete_tag_dialog.resize(350, 153)
        self.buttonBox = QDialogButtonBox(delete_tag_dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(0, 110, 341, 31))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.deleteInfoLabel = QLabel(delete_tag_dialog)
        self.deleteInfoLabel.setObjectName(u"deleteInfoLabel")
        self.deleteInfoLabel.setGeometry(QRect(30, 50, 291, 31))

        self.retranslateUi(delete_tag_dialog)
        self.buttonBox.accepted.connect(delete_tag_dialog.accept)
        self.buttonBox.rejected.connect(delete_tag_dialog.reject)

        QMetaObject.connectSlotsByName(delete_tag_dialog)
    # setupUi

    def retranslateUi(self, delete_tag_dialog):
        delete_tag_dialog.setWindowTitle(QCoreApplication.translate("delete_tag_dialog", u"Delete Tag?", None))
        self.deleteInfoLabel.setText(QCoreApplication.translate("delete_tag_dialog", u"TextLabel", None))
    # retranslateUi

