import os

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
        #self.outputDir = self.getOutputDir()
        self.show()
    
    # DOESN'T Work TODO: Debug 
    def getOutputDir(self):
        newdir = 'images'
        imagesDir = ''
        try:
            imagesDir = os.mkdir(newdir)
        except Exception:
            imagesDir = os.path.join(__file__, newdir)
        return imagesDir
           
        
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
    def createQuestionImages(self):
        subdir = 'images'
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
            # Create images for the question
            frame.replaceNameWithQuestionMarks()
            self.saveWidgetAsImage(subdir, questionSuffix, suffix)
            frame.saveFrameAsImage(subdir, questionSuffix, suffix)
            
            # Create images for the answer
            frame.restoreNameLabelHighlightAnswer()
            self.saveWidgetAsImage(subdir, answerSuffix, suffix)
            frame.saveFrameAsImage(subdir, answerSuffix, suffix)
            frame.restoreNameLabelColor()
            suffix+=1
            
    
    # Save to image file
    def saveWidgetAsImage(self, subdir, qaSuffix, suffix):
        pixmap = QtGui.QPixmap(self.size())
        self.render(pixmap)
        filename = 'cw' + qaSuffix + str(suffix) + '.png'
        path = os.path.join(subdir, filename)
        # Find out why this doesn't work
        #path = os.path.join(self.outputDir, filename)
        pixmap.save(path)
          
