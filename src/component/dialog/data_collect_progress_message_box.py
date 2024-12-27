from PySide6.QtWidgets import QMessageBox

class DataCollectProcessMessageBox(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Collecting")
        self.setText("Data is being collected, please wait...")
        self.setStandardButtons(QMessageBox.StandardButton.NoButton)
        self.setModal(True)
        self.show()
        
    def update_progress(self, progress: int):
        self.setText(f"Processed {progress} files")
        
    def set_status(self, status: str):
        self.setText(status)