from PySide6.QtWidgets import QMessageBox

class DataCollectProcessMessageBox(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("正在收集数据")
        self.setStandardButtons(QMessageBox.StandardButton.NoButton)
        self.setModal(True)
        self.show()
        
    def set_status(self, status: str):
        self.setText(status)