import sys
from PyQt4 import QtGui, QtCore
from DragLabel import *
from CentralWidget import *

class FaceMap(QtGui.QMainWindow):
    def __init__(self):
        super(FaceMap, self).__init__()
        self.initUI()
    
    # Make a drop-enabled window with a custom toolbar
    # along the left hand side   
    def initUI(self):
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('FaceMap')
        self.addCustomToolBar()
        self.addCentralWidget()
        self.show()
        

    # Add a left-hand-side toolbar for the FaceMap actions
    def addCustomToolBar(self):
        newPerson = QtGui.QAction(QtGui.QIcon('new_person.jpg'), 'New', self)
        newPerson.setShortcut('Ctrl+N')
        newPerson.triggered.connect(self.chooseFiles)
        
        saveImage = QtGui.QAction(QtGui.QIcon('save_pictures.jpg'), 'Save', self)
        saveImage.setShortcut('Ctrl+S')
        saveImage.triggered.connect(self.saveImage)
        
        self.toolbar = QtGui.QToolBar()
        self.toolbar.addAction(newPerson)
        self.toolbar.addAction(saveImage)
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolbar)
    
    # Add a central widget with no (default absolute) layout
    def addCentralWidget(self):
        self.centralWidget = CentralWidget(self)
        self.setCentralWidget(self.centralWidget)
        
    
    # Create a file-chooser dialog to pick images
    def chooseFiles(self):
        fnames = QtGui.QFileDialog.getOpenFileNames(self, 'Open file', 
                '/home', 'Image Files (*.png *.jpg *.bmp, *gif)')
        for fname in fnames:
            if fname:
                self.centralWidget.addDraggableFrame(fname)
                
    # Create a file-chooser dialog to save images
    def saveImage(self):
        self.centralWidget.createQuestionImages()
    
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = FaceMap()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()