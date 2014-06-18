import os

from PyQt4 import QtGui, QtCore
from DragFrame import *

class CentralWidget(QtGui.QWidget):
    _newFrameIndex = 0;
    
    def __init__(self, parent, imageSetId):
        super(CentralWidget, self).__init__(parent)
        self.imageSetId = imageSetId
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
    
    
    # Cycle through each of the DragFrames, replacing the name with red ????
    # and turning the border red.
    def createQuestionAnswerImages(self, directory):        
        subdir = os.path.join(directory, ('images' + self.imageSetId))
        try:
            os.mkdir(subdir)
        except Exception:
            pass
        
        # Suffix fileneams to indicate which DragFrame we're writing
        # and whether it's a question frame or an answer frame.
        questionSuffix = 'Q'
        answerSuffix = 'A'
        suffix = 0
        
        # Create an image for each Question Frame
        for frame in self.frameList:
            deleted = frame.isDeleted
            if deleted == False:
                # Create images for the question
                frame.replaceNameWithQuestionMarks()
                self.saveWidgetAsImage(subdir, self.imageSetId, questionSuffix, suffix)
                frame.saveFrameAsImage(subdir, self.imageSetId, questionSuffix, suffix)
                
                # Create images for the answer
                frame.restoreNameLabelHighlightAnswer()
                self.saveWidgetAsImage(subdir, self.imageSetId, answerSuffix, suffix)
                frame.saveFrameAsImage(subdir, self.imageSetId, answerSuffix, suffix)
                frame.restoreNameLabelColor()
                suffix+=1
            
    
    # Save to image file
    def saveWidgetAsImage(self, subdir, filePre, qaSuffix, suffix):
        pixmap = QtGui.QPixmap(self.size())
        self.render(pixmap)
        filename = filePre + 'cw' + qaSuffix + str(suffix) + '.png'
        path = os.path.join(subdir, filename)
        pixmap.save(path)
          
