import sys
from PyQt4 import QtCore, QtGui

class DragFrame(QtGui.QFrame):
    _draggedIndex = -1
    _lastX = 0
    _lastY = 0
    
    def __init__(self, parent, index):
        super(DragFrame, self).__init__(parent)
        self.index = index
        self.initUI()
        
    def initUI(self):        
        self.imageLabel = QtGui.QLabel()
        self.imageLabel.setMaximumWidth(80)
        self.imageLabel.setMaximumHeight(100)
        
        self.nameLabel = QtGui.QLabel("Double-Click!")
        self.nameLabel.setMaximumHeight(30)
        self.nameLabel.setMinimumHeight(30)
        self.nameLabel.setWordWrap(True)
        
        self.setMaximumSize(90, 140)
        self.setMinimumSize(90, 140)
        self.vbox = QtGui.QVBoxLayout()
        self.vbox.setSpacing(0)
        
    # Overridden method to process mouse move events
    def mouseMoveEvent(self, e):
        if e.buttons() != QtCore.Qt.LeftButton:
            return
        
        DragFrame._draggedIndex = self.index
        mimeData = QtCore.QMimeData()
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        drag.start(QtCore.Qt.MoveAction)
        
    # Overridden method to process mouse press events
    def mousePressEvent(self, e):
        super(DragFrame, self).mousePressEvent(e)
        if e.button() == QtCore.Qt.RightButton:
            self.promptDeleteFrame()
    
    # Prompt the user to check they want to delete the frame      
    def promptDeleteFrame(self):
        reply = self.confirmDeleteFrame()
        if reply == QtGui.QMessageBox.Yes:        
            self.deleteLater()
    
    # Confirm deletion of the person frame
    def confirmDeleteFrame(self):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Delete Person?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        return reply
        
       
    # React to a double-click
    def mouseDoubleClickEvent(self, e):
        self.showDialog()
    
    
    # Pop-up a dialog to change the name of the person
    def showDialog(self):    
        text, ok = QtGui.QInputDialog.getText(self, 'Name', 
            'Enter name:')
        if ok:
            self.nameLabel.setText(str(text))

    # Sets the image label to the maximum size        
    def setImageLabel(self, fileName):
        image = QtGui.QPixmap(fileName)
        width = min(image.width(),  self.imageLabel.maximumWidth())
        height = min(image.height(), self.imageLabel.maximumHeight())
        image = image.scaled(QtCore.QSize(width, height), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.imageLabel.setPixmap(image)
        self.imageLabel.setStyleSheet("border: 2px solid black")
        self.imageLabel.adjustSize()
        self.vbox.addWidget(self.imageLabel)
        self.nameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.nameLabel.setStyleSheet("border: 2px solid black")
        self.vbox.addWidget(self.nameLabel)
        self.setLayout(self.vbox)
        self.moveNextSpace()
        self.show()
    
    # Places the next picture in a new (and hopefully empty) position 
    def moveNextSpace(self):
        maxSize = self.parent().size()
        maxWidth = maxSize.width()
        maxHeight = maxSize.height()
        if(DragFrame._lastX + 180 < maxWidth):
            DragFrame._lastX += 90
        elif(DragFrame._lastY + 280 < maxHeight):
            DragFrame._lastX = 0
            DragFrame._lastY += 140
        else:
            DragFrame._lastX = 0
            DragFrame._lastY += 0   
            
        self.move(DragFrame._lastX, DragFrame._lastY)
       