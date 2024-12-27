from typing import TYPE_CHECKING
import os

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Qt

from ui_compiled.Ui_picture_frame import Ui_pictureFrame
from service.database import PicFile, PicMetadata

if TYPE_CHECKING:
    from controller.picture_manager import PictureManagerController

class PictureFrame(QFrame):
    def __init__(self, parent, controller: 'PictureManagerController', pic_data: PicMetadata | PicFile):
        super().__init__(parent=parent)
        self.ui = Ui_pictureFrame()
        self.ui.setupUi(self)
        self.controller = controller
        try:
            if isinstance(pic_data, PicMetadata):
                self.setup_metadata(pic_data)
            elif isinstance(pic_data, PicFile):
                self.setup_pic_file(pic_data)
        except Exception as e:
            print(f"Error in PictureFrame: {e}")
    
    def setup_metadata(self, metadata: PicMetadata):
        self.ui.titleLabel.setText(metadata.title)
        self.ui.illustratorLabel.setText(metadata.user)
        self.ui.pidLabel.setText(str(metadata.pid))
        self.pic_files = self.controller.database.get_file_list([metadata.pid])
        if not self.pic_files:
            return
        if len(self.pic_files) > 1:
            self.ui.fileTypeAndSizeLabel.setText(f"{len(self.pic_files)} pics")
            for pic in self.pic_files:
                if pic.num == 0:
                    pixmap = QPixmap(os.path.join(pic.directory, pic.file_name))
                    pixmap = pixmap.scaled(self.ui.imageLabel.size(), aspectMode=Qt.AspectRatioMode.KeepAspectRatio, mode=Qt.TransformationMode.SmoothTransformation)
                    self.ui.imageLabel.setPixmap(pixmap)
        else:
            pixmap = QPixmap(os.path.join(self.pic_files[0].directory, self.pic_files[0].file_name))
            pixmap = pixmap.scaled(self.ui.imageLabel.size(), aspectMode=Qt.AspectRatioMode.KeepAspectRatio, mode=Qt.TransformationMode.SmoothTransformation)
            self.ui.imageLabel.setPixmap(pixmap)
            self.ui.resolutionLabel.setText(f"{self.pic_files[0].width}x{self.pic_files[0].height}")
            self.ui.fileTypeAndSizeLabel.setText(f"{self.pic_files[0].file_type} | {self.pic_files[0].size / 1024**2:.2f} MB")
    
    def setup_pic_file(self, pic_file: PicFile):
        self.ui.titleLabel.setText(f"{pic_file.pid} - {pic_file.num}")
        self.ui.pidLabel.setText(str(pic_file.pid))
        self.ui.resolutionLabel.setText(f"{pic_file.width}x{pic_file.height}")
        self.ui.fileTypeAndSizeLabel.setText(f"{pic_file.file_type} | {pic_file.size / 1024**2:.2f} MB")
        metadata = self.controller.database.get_metadata_list([pic_file.pid])[0]
        pixmap = QPixmap(os.path.join(pic_file.directory, pic_file.file_name))
        pixmap = pixmap.scaled(self.ui.imageLabel.size(), aspectMode=Qt.AspectRatioMode.KeepAspectRatio, mode=Qt.TransformationMode.SmoothTransformation)
        self.ui.imageLabel.setPixmap(pixmap)
        if metadata:
            self.ui.illustratorLabel.setText(metadata.user)