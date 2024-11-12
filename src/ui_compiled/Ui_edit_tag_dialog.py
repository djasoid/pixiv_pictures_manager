# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edit_tag_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QHBoxLayout, QLabel, QPlainTextEdit,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_edit_tag_dialog(object):
    def setupUi(self, edit_tag_dialog):
        if not edit_tag_dialog.objectName():
            edit_tag_dialog.setObjectName(u"edit_tag_dialog")
        edit_tag_dialog.resize(458, 406)
        self.horizontalLayout = QHBoxLayout(edit_tag_dialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.english_name_label = QLabel(edit_tag_dialog)
        self.english_name_label.setObjectName(u"english_name_label")

        self.verticalLayout.addWidget(self.english_name_label)

        self.englishNameEdit = QPlainTextEdit(edit_tag_dialog)
        self.englishNameEdit.setObjectName(u"englishNameEdit")
        self.englishNameEdit.setMaximumSize(QSize(16777215, 30))

        self.verticalLayout.addWidget(self.englishNameEdit)

        self.type_label = QLabel(edit_tag_dialog)
        self.type_label.setObjectName(u"type_label")

        self.verticalLayout.addWidget(self.type_label)

        self.typeComboBox = QComboBox(edit_tag_dialog)
        self.typeComboBox.setObjectName(u"typeComboBox")

        self.verticalLayout.addWidget(self.typeComboBox)

        self.synonyms_label = QLabel(edit_tag_dialog)
        self.synonyms_label.setObjectName(u"synonyms_label")

        self.verticalLayout.addWidget(self.synonyms_label)

        self.synonymTextEdit = QPlainTextEdit(edit_tag_dialog)
        self.synonymTextEdit.setObjectName(u"synonymTextEdit")
        self.synonymTextEdit.setPlainText(u"")

        self.verticalLayout.addWidget(self.synonymTextEdit)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.buttonBox = QDialogButtonBox(edit_tag_dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.horizontalLayout.addWidget(self.buttonBox)


        self.retranslateUi(edit_tag_dialog)
        self.buttonBox.rejected.connect(edit_tag_dialog.reject)
        self.buttonBox.accepted.connect(edit_tag_dialog.accept)

        QMetaObject.connectSlotsByName(edit_tag_dialog)
    # setupUi

    def retranslateUi(self, edit_tag_dialog):
        edit_tag_dialog.setWindowTitle(QCoreApplication.translate("edit_tag_dialog", u"Edit Synonym", None))
        self.english_name_label.setText(QCoreApplication.translate("edit_tag_dialog", u"English Name", None))
        self.type_label.setText(QCoreApplication.translate("edit_tag_dialog", u"Type", None))
        self.synonyms_label.setText(QCoreApplication.translate("edit_tag_dialog", u"Synonyms", None))
    # retranslateUi

