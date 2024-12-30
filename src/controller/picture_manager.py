from typing import TYPE_CHECKING

from PySide6.QtWidgets import QTreeWidget, QApplication, QTreeWidgetItem, QAbstractItemView, QTextEdit, QListWidgetItem, QDialog, QLayout, QFileDialog
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QDropEvent, QBrush, QColor, QPalette
from PySide6.QtCore import QThread, Signal

from service.tag_tree import TagTree, Tag
from service.database import PicDatabase, PicFile, PicMetadata
from tools.log import log_execution
from component.widget.tag_widget import TagWidget
from component.widget.picture_frame import PictureFrame
from component.dialog.data_collect_progress_message_box import DataCollectProcessMessageBox

if TYPE_CHECKING:
    from view.picture_manager import MainWindow

class PictureManagerController:
    def __init__(self, view: 'MainWindow'):
        self.view = view
        self.view.setup_controller(self)
        self._init_ui()
        self.tag_index_cache = {}
        self.database = PicDatabase()
        self._init_context()
        self._init_tag_tree()
        self._init_tag_search()
        
    def _init_ui(self):
        self.view.sortComboBox.addItems(['id'])
        self.timer = QTimer(self.view)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.add_include_tag)
        
    def _init_context(self):
        self.displayed_widget = []
        self.refresh_browse_area_width()
        self.display_index = 0
        self.display_row = 0
        self.display_column = 0
        self.show_restricted = False
        self.include_tag_set = set()
        self.exclude_tag_set = set()
        self.tag_filtered_pids: set[int] = []
        self.pic_metadata_dict: dict[int, PicMetadata] = {}
        self.pic_file_list: list[PicFile] = []
        self.display_pic_list: list[PicFile | PicMetadata] = []
        self.last_file_type_filter = {
            'jpg': True,
            'png': True,
            'gif': True
        }
        self.last_resolution_filter = {
            'width': self._parse_resolution_range(self.view.resolutionWidthEdit.toPlainText()),
            'height': self._parse_resolution_range(self.view.resolutionHeightEdit.toPlainText())
        }
        self.sort_ratio = 1
        self.slider_edited = False
        self.spin_box_edited = False
        self.current_sort = 'id'
        
    def _init_tag_tree(self):
        self.tag_tree = TagTree()
        self.tag_item_dict: dict[str, set[QTreeWidgetItem]] = {}
        self.highlighted_tags: set[str] = set()
        self.default_background_color = self.view.characterTagTree.palette().color(QPalette.ColorRole.Base)
        for top_tag in self.tag_tree.root.sub_tags.values():
            if top_tag.tag_type == '__CHARACTER__':
                self.character_top_tag = top_tag
                for sub_tag in top_tag.sub_tags.values():
                    self.view.characterTagTree.addTopLevelItem(self._get_tree_item(sub_tag))
            elif top_tag.tag_type == '__ATTRIBUTE__':
                self.attribute_top_tag = top_tag
                for sub_tag in top_tag.sub_tags.values():
                    self.view.attributeTagTree.addTopLevelItem(self._get_tree_item(sub_tag))
        
    def _get_tree_item(self, tag: Tag) -> QTreeWidgetItem:
        item = QTreeWidgetItem([tag.name])
        if tag.name in self.tag_item_dict:
            self.tag_item_dict[tag.name].add(item)
        else:
            self.tag_item_dict[tag.name] = {item}
        
        for sub_tag in tag.sub_tags.values():
            if not self.show_restricted and sub_tag.tag_type == 'R-18':
                continue
            item.addChild(self._get_tree_item(sub_tag))
        
        return item
    
    def handle_single_click(self, item: QTreeWidgetItem) -> None:
        self.single_clicked_item = item
        self.timer.start(250)

    def add_include_tag(self):
        item = self.single_clicked_item
        tag_name = item.text(0)
        tag = self.tag_tree.get_tag(tag_name)
        if not tag.is_tag:
            return
        
        if tag_name in self.include_tag_set and tag_name in self.exclude_tag_set:
            return
        
        self.include_tag_set.add(tag_name)
        tag_widget = TagWidget(self.view.selectedTagScrollAreaWidgetContent, self, tag_name, True)
        self.view.selectedTagLayout.insertWidget(0, tag_widget)
        self._pic_tag_search()
        
    def add_exclude_tag(self, item: QTreeWidgetItem):
        self.timer.stop()
        tag_name = item.text(0)
        tag = self.tag_tree.get_tag(tag_name)
        if tag_name in self.exclude_tag_set or tag_name in self.include_tag_set:
            return
        
        if not tag.is_tag:
            return

        self.exclude_tag_set.add(tag_name)
        self.view.selectedTagLayout.addWidget(TagWidget(self.view.selectedTagScrollAreaWidgetContent, self, tag_name, False))
        self._pic_tag_search()
        
    def remove_selected_tag(self, tag_widget: TagWidget):
        if tag_widget.include:
            self.include_tag_set.remove(tag_widget.tag_name)
        else:
            self.exclude_tag_set.remove(tag_widget.tag_name)

        self.view.selectedTagLayout.removeWidget(tag_widget)
        tag_widget.deleteLater()
        self._pic_tag_search()
    
    def _init_tag_search(self):
        self.tag_last_search = ""
        self.tag_search_results = []
        self.tag_search_index = 0

    def tag_search(self, search_text: str):
        if search_text == self.tag_last_search and self.tag_search_results:
            if self.tag_search_index < len(self.tag_search_results):
                self._expand_and_scroll_to_tag_item(self.tag_search_results[self.tag_search_index])
                self.tag_search_index += 1
            else:
                self.tag_search_index = 0
                self._expand_and_scroll_to_tag_item(self.tag_search_results[self.tag_search_index])
        else:
            character_search_results = self.view.characterTagTree.findItems(search_text, Qt.MatchFlag.MatchContains | Qt.MatchFlag.MatchRecursive)
            attribute_search_results = self.view.attributeTagTree.findItems(search_text, Qt.MatchFlag.MatchContains | Qt.MatchFlag.MatchRecursive)
            self.tag_search_results = character_search_results + attribute_search_results
            self.tag_last_search = search_text
            self.tag_search_index = 0
            if self.tag_search_results:
                self._expand_and_scroll_to_tag_item(self.tag_search_results[self.tag_search_index])
                self.tag_search_index += 1
                
    def _expand_and_scroll_to_tag_item(self, tag_item: QTreeWidgetItem):
        """Expand the tag tree and select the tag item"""
        tree_widget = tag_item.treeWidget()
        if tree_widget is self.view.characterTagTree:
            self.view.tagTreeTabWidget.setCurrentIndex(0)
        elif tree_widget is self.view.attributeTagTree:
            self.view.tagTreeTabWidget.setCurrentIndex(1)
            
        parent_item = tag_item.parent()
        while parent_item:
            parent_item.setExpanded(True)
            parent_item = parent_item.parent()
            
        tree_widget.setCurrentItem(tag_item)
        tree_widget.scrollToItem(tag_item, QAbstractItemView.ScrollHint.PositionAtCenter)
        
    def _pic_tag_search(self) -> None:
        """
        Search for pictures with tags.
        the search will return a set of picture ids that have all the tags in includeTags and none of the tags in excludeTags.
        """
        def find_pids(tag: str) -> set:
            related_tags = {tag} | self.tag_tree.get_sub_tags(tag)
            pids = set()
            for related_tag in related_tags:
                if related_tag in self.tag_index_cache:
                    pids.update(self.tag_index_cache[related_tag])
                else:
                    tag_pids = self.database.get_pids_by_tag(related_tag)
                    self.tag_index_cache[related_tag] = tag_pids
                    pids.update(tag_pids)

            return pids
                
        included_pids = None
        for tag in self.include_tag_set:
            if included_pids is None:
                included_pids = find_pids(tag)
            else:
                included_pids &= find_pids(tag)

        excluded_pids = set()
        for tag in self.exclude_tag_set:
            excluded_pids.update(find_pids(tag))
        
        self.tag_filtered_pids = included_pids - excluded_pids if included_pids else set()
        self.pic_metadata_dict = self.database.get_metadata_dict(self.tag_filtered_pids)
        self.pic_file_list = self.database.get_file_list(self.tag_filtered_pids)
        self.display_pic_list = [i for i in self.pic_metadata_dict.values()]
        self._refresh_pic_display()
        self._clear_highlighted_tags()
        self._highlight_available_tags()
        
    def _highlight_available_tags(self) -> None:
        def highlight_item(tag: str) -> None:
            if tag in self.tag_item_dict:
                self.highlighted_tags.add(tag)
                for item in self.tag_item_dict[tag]:
                    font = item.font(0)
                    font.setBold(True)
                    item.setFont(0, font)
                    item.setBackground(0, QBrush('#808080'))
                    parent_item = item.parent()
                    if parent_item:
                        parent_tag = parent_item.text(0)
                        if parent_tag not in self.highlighted_tags:
                            highlight_item(parent_tag)
                        
        available_tags = set()
        for data in self.pic_metadata_dict.values():
            available_tags.update(data.tags)
        
        for available_tag in available_tags:
            if available_tag in self.tag_item_dict:
                highlight_item(available_tag)
                
    def _clear_highlighted_tags(self) -> None:
        for tag in self.tag_item_dict:
            for item in self.tag_item_dict[tag]:
                font = item.font(0)
                font.setBold(False)
                item.setFont(0, font)
                item.setBackground(0, QBrush(self.default_background_color))
                
        self.highlighted_tags.clear()            

    def _is_match_file_type(self, pic_file: PicFile) -> bool:
        return self.last_file_type_filter.get(pic_file.file_type, False)
    
    def _is_match_resolution(self, pic_file: PicFile) -> bool:
        min_width, max_width = self.last_resolution_filter['width']
        min_height, max_height = self.last_resolution_filter['height']
    
        if min_width != -1 and pic_file.width < min_width:
            return False
        
        if max_width != -1 and pic_file.width > max_width:
            return False
        
        if min_height != -1 and pic_file.height < min_height:
            return False
        
        if max_height != -1 and pic_file.height > max_height:
            return False
    
        return True
    
    def _parse_resolution_range(self, resolution_range: str) -> tuple[int, int]:
        try:
            if resolution_range.startswith('>'):
                return int(resolution_range[1:]), -1
            elif resolution_range.startswith('<'):
                return -1, int(resolution_range[1:])
            elif '-' in resolution_range:
                return tuple(map(int, resolution_range.split('-')))
            else:
                value = int(resolution_range)
                return value, value
            
        except ValueError:
            return -1, -1 # this will be treated as no limit

    def filt_and_sort_pic_files(self) -> None:
        file_type_filter = {
            'jpg': self.view.jpgCheckBox.isChecked(),
            'png': self.view.pngCheckBox.isChecked(),
            'gif': self.view.gifCheckBox.isChecked()
        }
        resolution_filter = {
            'width': self._parse_resolution_range(self.view.resolutionWidthEdit.toPlainText()),
            'height': self._parse_resolution_range(self.view.resolutionHeightEdit.toPlainText())
        }
        
        if self.last_file_type_filter == file_type_filter:
            filt_file_type = False
        else:
            filt_file_type = True
            self.last_file_type_filter = file_type_filter

        if self.last_resolution_filter == resolution_filter:
            filt_resolution = False
        else:
            filt_resolution = True
            self.last_resolution_filter = resolution_filter
        
        self.display_pic_list = []
        for pic_file in self.pic_file_list:
            if filt_file_type and not self._is_match_file_type(pic_file):
                continue

            if filt_resolution and not self._is_match_resolution(pic_file):
                continue
            
            self.display_pic_list.append(pic_file)
        
        self._sort_display_pic()

    def clear_resolution_filter(self) -> None:
        self.view.resolutionWidthEdit.clear()
        self.view.resolutionHeightEdit.clear()
        self.filt_and_sort_pic_files()
        
    def ratio_slider_sort(self) -> None:
        if self.spin_box_edited:
            return
        
        self.slider_edited = True
        slider_value = self.view.ratioSlider.value()
        if slider_value >= 0:
            temp = 1 + (slider_value / 20)
            ratio = 1 / temp
            self.view.heightRatioSpinBox.setValue(temp)
            self.view.widthRatioSpinBox.setValue(1)
        else:
            ratio = 1 - (slider_value / 20)
            self.view.widthRatioSpinBox.setValue(ratio)
            self.view.heightRatioSpinBox.setValue(1)
            
        self.slider_edited = False
        self.sort_ratio = ratio
        self.filt_and_sort_pic_files()
            
    def ratio_spin_box_sort(self) -> None:
        if self.slider_edited:
            return
        
        self.spin_box_edited = True
        if self.view.widthRatioSpinBox.value() == 0:
            ratio = 0
        elif self.view.heightRatioSpinBox.value() == 0:
            ratio = 10000
        else:
            ratio = self.view.widthRatioSpinBox.value() / self.view.heightRatioSpinBox.value()
            
        self.view.ratioSlider.setValue(self._convert_to_slider_value(ratio))
        self.spin_box_edited = False
        self.sort_ratio = ratio
        self.filt_and_sort_pic_files()

    def _sort_display_pic(self) -> None:
        if self.view.enableRatioCheckBox.isChecked():
            self.display_pic_list.sort(key=lambda pic_file: abs(pic_file.ratio - self.sort_ratio))
        elif self.current_sort == 'id':
            self.display_pic_list.sort(key=lambda pic_file: pic_file.pid)
        
        self._refresh_pic_display()
            
    def _convert_to_slider_value(self, ratio: float) -> int:
        if ratio <= 0:
            return 40
        elif ratio >= 3:
            return -40
        
        if ratio < 1:
            return int(((1/(ratio)) - 1) * 20)
        else:
            return int((1 - ratio) * 20)

    def _is_restricted(self, data: PicMetadata | PicFile) -> bool:
        if isinstance(data, PicMetadata):
            if data.x_restrict != 'allAges':
                return True
        elif isinstance(data, PicFile):
            metadata = self.pic_metadata_dict.get(data.pid)
            if metadata and metadata.x_restrict != 'allAges':
                return True

        return False
    
    def refresh_browse_area_width(self) -> None:
        current_width = self.view.picBrowseScrollArea.width()
        self.max_widgets_per_row = current_width // 250 if current_width >= 250 else 1
        for i, widget in enumerate(self.displayed_widget):
            row = i // self.max_widgets_per_row
            column = i % self.max_widgets_per_row
            self.view.picDisplayLayout.addWidget(widget, row, column)
    
    def _refresh_pic_display(self) -> None:
        self.displayed_widget.clear()
        self.refresh_browse_area_width()
        self._clear_all_widgets(self.view.picDisplayLayout)
        self.display_row = 0
        self.display_column = 0
        self.load_more_pics(0)
            
    def _clear_all_widgets(self, layout: 'QLayout') -> None:
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self._clear_all_widgets(child.layout())

    def load_more_pics(self, current_index: int = None) -> None:
        if current_index is None:
            current_index = self.display_index
        else:
            self.display_index = current_index
            
        if current_index >= len(self.display_pic_list):
            return
        
        load_amount = self.max_widgets_per_row * 3
        
        while current_index < len(self.display_pic_list) and load_amount > 0:
            if self._is_restricted(self.display_pic_list[current_index]) and not self.show_restricted:
                current_index += 1
                continue
            
            pic_frame = PictureFrame(self.view.picBrowseContentWidget, self, self.display_pic_list[current_index])
            self.displayed_widget.append(pic_frame)
            self.view.picDisplayLayout.addWidget(pic_frame, self.display_row, self.display_column)
            self.display_column += 1
            if self.display_column == self.max_widgets_per_row:
                self.display_column = 0
                self.display_row += 1
        
            current_index += 1
            load_amount -= 1
            
        self.display_index = current_index
        
    @log_execution("Info", "Adding new pictures from directory {args[1]}", "new pictures added")
    def add_new_pics(self, directory: str) -> None:
        message_box = DataCollectProcessMessageBox()

        def update_status(status):
            message_box.setText(status)

        def close_message_box():
            print("Data collection finished. Closing message box.")
            message_box.done(0)

        thread = DataCollectThread(self.database, self.tag_tree, directory)
        thread.status_update.connect(update_status)
        thread.finished.connect(close_message_box)
        thread.start()

        message_box.exec_()
        
    def select_directory_for_new_pics(self) -> None:
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        if dialog.exec():
            directory = dialog.selectedFiles()[0]
            if directory:
                self.add_new_pics(directory)
        
    def show_restricted_pics(self) -> None:
        if self.view.showRestrictedAction.isChecked():
            self.show_restricted = True
        else:
            self.show_restricted = False
            
        self.view.attributeTagTree.clear()
        self.view.characterTagTree.clear()
        self._init_tag_tree()
        self._highlight_available_tags()
        self._pic_tag_search()

class DataCollectThread(QThread):
    status_update = Signal(str)
    finished = Signal()

    def __init__(self, database: PicDatabase, tag_tree: TagTree, directory):
        super().__init__()
        self.database = database
        self.tag_tree = tag_tree
        self.directory = directory

    def run(self):
        self.connection = self.database.get_new_connection()
        new_pics = self.database.collect_data(self.directory, thread=self, connection=self.connection)
        self.status_update.emit("Completing tags...")
        self.database.complete_tag(self.tag_tree, new_pics, self.connection)
        self.status_update.emit("Indexing tags...")
        self.database.init_tag_index(self.tag_tree, new_pics, self.connection)
        print("Data collection finished.")
        self.finished.emit()
