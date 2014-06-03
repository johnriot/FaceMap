import sys
from PyQt4 import QtCore, QtGui


class DragWidget(QtGui.QWidget):
    def __init__(self):
        super(DragWidget, self).__init__()

    def mouseMoveEvent(self, e):
        if e.buttons() != QtCore.Qt.LeftButton:
            return
        
        mimeData = QtCore.QMimeData()
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        drag.start(QtCore.Qt.MoveAction)
        
    def mousePressEvent(self, e):
        super(DragWidget, self).mousePressEvent(e)
        if e.button() == QtCore.Qt.LeftButton:
            print 'press'
