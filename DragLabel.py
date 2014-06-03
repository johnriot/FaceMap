import sys
from PyQt4 import QtCore, QtGui


class DragLabel(QtGui.QLabel):
    _draggedIndex = -1
    
    def __init__(self, parent, index):
        super(DragLabel, self).__init__(parent)
        self.index = index
        self.setMaximumWidth(60)
        self.setMaximumHeight(80)
        
    def getId(self):
        return self.index

    def mouseMoveEvent(self, e):
        if e.buttons() != QtCore.Qt.LeftButton:
            return
        
        DragLabel._draggedIndex = self.index
        mimeData = QtCore.QMimeData()
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        drag.start(QtCore.Qt.MoveAction)
        
        
    def mousePressEvent(self, e):
        super(DragLabel, self).mousePressEvent(e)
        if e.button() == QtCore.Qt.LeftButton:
            print 'press'
            
    def setImageLabel(self, fileName):
        image = QtGui.QPixmap(fileName)
    
        width = min(image.width(),  self.maximumWidth())
        height = min(image.height(), self.maximumHeight())
        image = image.scaled(QtCore.QSize(width, height), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.setPixmap(image)
        self.adjustSize()
