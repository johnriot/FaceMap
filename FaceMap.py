import sys
from PyQt4 import QtGui, QtCore
from DragLabel import *
from CentralWidget import *

class FaceMap(QtGui.QMainWindow):
    def __init__(self):
        super(FaceMap, self).__init__()
        self.initUI()
    
    # Make a maximised, drop-enabled window with a custom toolbar
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
        self.toolbar = QtGui.QToolBar()
        self.toolbar.addAction(newPerson)
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolbar)
    
    # Add a central widget with no (default absolute) layout
    def addCentralWidget(self):
        self.centralWidget = CentralWidget(self)
        self.setCentralWidget(self.centralWidget)
        
    
    # Create a file-chooser dialog to pick images
    def chooseFiles(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
                '/home', 'Image Files (*.png *.jpg *.bmp, *gif)')
        self.centralWidget.addDraggableImageToList(fname)
    
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = FaceMap()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()