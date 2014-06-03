from PyQt4 import QtGui, QtCore
from DragLabel import *
from DragWidget import *



class CentralWidget(QtGui.QWidget):
    _newImageIndex = 0;
    
    def __init__(self, parent):
        super(CentralWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        # Not sure why DragLabel construction needs to go here, but
        # having it in addDraggableImage() doesn't seem to work
        self.imageList = list()
        maxPictures = 100
        for i in range(maxPictures):
            self.imageList.append(DragLabel(self, i))
        self.show()
        
    # Support for drag event 
    def dragEnterEvent(self, e):
        e.accept()

    # Support for drop event
    def dropEvent(self, e):
        position = e.pos()
        dragImageLabel = self.imageList[DragLabel._draggedIndex]
        width =  dragImageLabel.width()
        height = dragImageLabel.height()    
        offset = QtCore.QPoint(width/2, height/2)
        dragImageLabel.move(position - offset)
        DragLabel._draggedIndex = -1 
        e.setDropAction(QtCore.Qt.MoveAction)
        e.accept()
    
    # Adds a draggable image to our central widget
    def addDraggableImage(self, imageName):
        image = QtGui.QPixmap(imageName)
        self.dragImageLabel.setPixmap(image)
        self.dragImageLabel.adjustSize()
    
    # Adds a draggable image to our list
    def addDraggableImageToList(self, fileName):
        dragImageLabel = self.imageList[CentralWidget._newImageIndex]
        CentralWidget._newImageIndex+=1
        dragImageLabel.setImageLabel(fileName)
        
