from PySide6.QtWidgets import QDialog

from ui_compiled.Ui_synonym_edit_dialog import Ui_synonym_edit_dialog

class TagEditDialog(QDialog, Ui_synonym_edit_dialog):
    def __init__(self, parent, tag_name: str, synonyms: set, enName: str, type: str):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.setWindowTitle(f"编辑同义标签：{tag_name}")
        self.synonymTextEdit.setPlainText("\n".join(synonyms))
        self.englishNameEdit.setPlainText(enName)
        self.typeComboBox.addItems(["", "IP", "Character", "R-18"])
        if type:
            self.typeComboBox.setCurrentText(type)

    def accept(self):
        super().accept()
    
    def reject(self):
        super().reject()