from PySide6.QtWidgets import QTextEdit, QTreeWidget
import program_objects as progObjs

# Customized QTreeWidget for tag tree
class MainTagTreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def setTagTree(self, tagTree: progObjs.TagTree):
        self.tagTree = tagTree
        self.addTopLevelItem(tagTree.toTreeWidgetItem())

    def setViewTree(self, viewTree: QTreeWidget): # pass view_tree to sync two tree widgets
        self.viewTree = viewTree

    def setOutputBox(self, outputBox: QTextEdit): # pass output_box to show output
        self.outputBox = outputBox

    def dropEvent(self, event):
        """handle drop event and make changes to the tag tree"""
        targetItem = self.itemAt(event.position().toPoint()) # get the item at the drop position
        if targetItem is None: # if the drop position is not on an item, do nothing
            return
        
        targetTag = targetItem.text(0)
        
        source = event.source().objectName()

        if source == "view_tree":
            dragTag = event.source().currentItem().text(0)
            self.outputBox.append(f"source: {source}, target: {targetTag}, drag: {dragTag}")
        elif source == "new_tag_store_lst":
            dragTag = event.source().currentItem().text()
            self.outputBox.append(f"source: {source}, target: {targetTag}, drag: {dragTag}")
        elif source == "new_tag_orignal_lst":
            dragTag = event.source().currentItem().text()
            self.outputBox.append(f"source: {source}, target: {targetTag}, drag: {dragTag}")
        elif source == "new_tag_transl_lst":
            dragTag = event.source().currentItem().text()
            self.outputBox.append(f"source: {source}, target: {targetTag}, drag: {dragTag}")