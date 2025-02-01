from typing import TYPE_CHECKING
import os

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Qt

from ui_compiled.Ui_picture_frame import Ui_pictureFrame
from service.database import PicFile, PicMetadata

class PictureFrame(QFrame):
    def __init__(self, parent, image: QPixmap, pic_files: list[PicFile], pic_data: PicMetadata = None):
        super().__init__(parent=parent)
        self.ui = Ui_pictureFrame()
        self.ui.setupUi(self)
        self.image = image
        self.pic_files = pic_files
        self.pic_data = pic_data
        try:
            if pic_data:
                self.setup_metadata()
            else:
                self.setup_pic_file(self.pic_files[0])
        except Exception as e:
            print(f"Error in PictureFrame: {e}")
    
    def setup_metadata(self):
        self.ui.titleLabel.setText(self.pic_data.title)
        self.ui.illustratorLabel.setText(self.pic_data.user)
        self.ui.pidLabel.setText(str(self.pic_data.pid))
        self.image = self.image.scaled(self.ui.imageLabel.size(), aspectMode=Qt.AspectRatioMode.KeepAspectRatio, mode=Qt.TransformationMode.SmoothTransformation)
        self.ui.imageLabel.setPixmap(self.image)
        
        if not self.pic_files:
            return
        
        if len(self.pic_files) > 1:
            self.ui.fileTypeAndSizeLabel.setText(f"{len(self.pic_files)} pics")
        else:
            self.ui.resolutionLabel.setText(f"{self.pic_files[0].width}x{self.pic_files[0].height}")
            self.ui.fileTypeAndSizeLabel.setText(f"{self.pic_files[0].file_type} | {self.pic_files[0].size / 1024**2:.2f} MB")
    
    def setup_pic_file(self, pic_file: PicFile):
        self.ui.titleLabel.setText(f"{pic_file.pid} - {pic_file.num}")
        self.ui.pidLabel.setText(str(pic_file.pid))
        self.ui.resolutionLabel.setText(f"{pic_file.width}x{pic_file.height}")
        self.ui.fileTypeAndSizeLabel.setText(f"{pic_file.file_type} | {pic_file.size / 1024**2:.2f} MB")
        self.image = self.image.scaled(self.ui.imageLabel.size(), aspectMode=Qt.AspectRatioMode.KeepAspectRatio, mode=Qt.TransformationMode.SmoothTransformation)
        self.ui.imageLabel.setPixmap(self.image)