from PyQt4 import QtGui, QtCore
from DragLabel import *
from DragWidget import *
from DragFrame import *



class CentralWidget(QtGui.QWidget):
    _newFrameIndex = 0;
    
    def __init__(self, parent):
        super(CentralWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.frameList = list()
        self.show()
        
    # Support for drag event 
    def dragEnterEvent(self, e):
        e.accept()

    # Support for drop event
    def dropEvent(self, e):
        position = e.pos()
        dragFrame = self.frameList[DragFrame._draggedIndex]
        width =  dragFrame.width()
        height = dragFrame.height()    
        offset = QtCore.QPoint(width/2, height/2)
        dragFrame.move(position - offset)
        DragFrame._draggedIndex = -1 
        e.setDropAction(QtCore.Qt.MoveAction)
        e.accept()
    
    # Adds a draggable image to our list
    def addDraggableFrame(self, fileName):
        dragFrame = DragFrame(self, CentralWidget._newFrameIndex)
        CentralWidget._newFrameIndex+=1
        self.frameList.append(dragFrame)
        dragFrame.setImageLabel(fileName)
    
    # Save to image file
    def saveWidgetAsImage(self):
        pixmap = QtGui.QPixmap(self.size())
        self.render(pixmap)
        pixmap.save("face_map.png");    
