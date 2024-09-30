from PySide6 import QtWidgets
from global_vars import *
import pathlib

class DropList(QtWidgets.QListWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super(DropList, self).__init__(parent, *args, **kwargs)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        md = event.mimeData()
        if md.hasUrls():
            if self.objectName() == 'list_lights':
                for url in md.urls():
                    path = pathlib.Path(url.toLocalFile())
                    self.addItem(path.name)
                    light_files.append(path)
                
                    
            if self.objectName() == 'list_darks':
                for url in md.urls():   
                    path = pathlib.Path(url.toLocalFile())
                    self.addItem(path.name)
                    dark_files.append(path)
                    
            if self.objectName() == 'list_flats':
                for url in md.urls():    
                    path = pathlib.Path(url.toLocalFile())
                    self.addItem(path.name)
                    flat_files.append(path)
                    
            if self.objectName() == 'list_bias':
                for url in md.urls():    
                    path = pathlib.Path(url.toLocalFile())
                    self.addItem(path.name)
                    bias_files.append(path)
            event.acceptProposedAction()
