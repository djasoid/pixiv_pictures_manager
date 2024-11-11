from PySide6.QtWidgets import QDialog

from ui_compiled.Ui_delete_tag_dialog import Ui_delete_tag_dialog

class DeleteDialog(QDialog, Ui_delete_tag_dialog):
    def __init__(self, parent, tag_name, parent_tag_name):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.deleteInfoLabel.setText(f"确认从 {parent_tag_name} 删除 {tag_name} ?")
    
    def accept(self):
        super().accept()
    
    def reject(self):
        super().reject()