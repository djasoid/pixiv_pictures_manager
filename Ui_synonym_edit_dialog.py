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
    QHBoxLayout, QLabel, QPlainTextEdit, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_synonym_edit_dialog(object):
    def setupUi(self, synonym_edit_dialog):
        if not synonym_edit_dialog.objectName():
            synonym_edit_dialog.setObjectName(u"synonym_edit_dialog")
        synonym_edit_dialog.resize(458, 406)
        self.horizontalLayout = QHBoxLayout(synonym_edit_dialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.synonyms_label = QLabel(synonym_edit_dialog)
        self.synonyms_label.setObjectName(u"synonyms_label")

        self.verticalLayout.addWidget(self.synonyms_label)

        self.synonymTextEdit = QPlainTextEdit(synonym_edit_dialog)
        self.synonymTextEdit.setObjectName(u"synonymTextEdit")
        self.synonymTextEdit.setPlainText(u"")

        self.verticalLayout.addWidget(self.synonymTextEdit)

        self.english_name_label = QLabel(synonym_edit_dialog)
        self.english_name_label.setObjectName(u"english_name_label")

        self.verticalLayout.addWidget(self.english_name_label)

        self.englishNameEdit = QPlainTextEdit(synonym_edit_dialog)
        self.englishNameEdit.setObjectName(u"englishNameEdit")
        self.englishNameEdit.setMaximumSize(QSize(16777215, 30))

        self.verticalLayout.addWidget(self.englishNameEdit)


        self.horizontalLayout.addLayout(self.verticalLayout)

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
        self.synonyms_label.setText(QCoreApplication.translate("synonym_edit_dialog", u"Synonyms", None))
        self.english_name_label.setText(QCoreApplication.translate("synonym_edit_dialog", u"English Name", None))
    # retranslateUi

