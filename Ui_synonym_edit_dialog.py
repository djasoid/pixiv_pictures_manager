# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'synonym_edit_dialog.ui'
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
    QHBoxLayout, QPlainTextEdit, QSizePolicy, QWidget)

class Ui_synonym_edit_dialog(object):
    def setupUi(self, synonym_edit_dialog):
        if not synonym_edit_dialog.objectName():
            synonym_edit_dialog.setObjectName(u"synonym_edit_dialog")
        synonym_edit_dialog.resize(458, 406)
        self.horizontalLayout = QHBoxLayout(synonym_edit_dialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.synonym_text_edit = QPlainTextEdit(synonym_edit_dialog)
        self.synonym_text_edit.setObjectName(u"synonym_text_edit")
        self.synonym_text_edit.setPlainText(u"")

        self.horizontalLayout.addWidget(self.synonym_text_edit)

        self.buttonBox = QDialogButtonBox(synonym_edit_dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.horizontalLayout.addWidget(self.buttonBox)


        self.retranslateUi(synonym_edit_dialog)
        self.buttonBox.rejected.connect(synonym_edit_dialog.reject)
        self.buttonBox.accepted.connect(synonym_edit_dialog.accept)

        QMetaObject.connectSlotsByName(synonym_edit_dialog)
    # setupUi

    def retranslateUi(self, synonym_edit_dialog):
        synonym_edit_dialog.setWindowTitle(QCoreApplication.translate("synonym_edit_dialog", u"Edit Synonym", None))
    # retranslateUi

