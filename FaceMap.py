from PyQt4 import QtGui, QtCore
from CentralWidget import *

class FaceMap(QtGui.QMainWindow):    
    def __init__(self, directory):
        super(FaceMap, self).__init__()
        self.dir = directory
        self.ankiWriteSignal = None
        # Use seconds since 1970 to uniquely identify image folder and images
        self.imageSetId = str(int(time.time()))
        self.initUI()
    
    # Make a drop-enabled window with a custom toolbar
    # along the left hand side   
    def initUI(self):
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('FaceMap')
        self.addCustomToolBar()
        self.addCentralWidget()
        self.show()
        

    # Add a left-hand-side toolbar for the face_map actions
    def addCustomToolBar(self):
        iconsDir = os.path.join(self.dir, 'icons')
        newPersonIcon = os.path.join(iconsDir, 'new_person.jpg')
        newPerson = QtGui.QAction(QtGui.QIcon(newPersonIcon), 'New', self)
        #newPerson = QtGui.QAction(QtGui.QIcon('new_person.jpg'), 'New', self)
        newPerson.setShortcut('Ctrl+N')
        newPerson.triggered.connect(self.chooseFiles)
        
        saveImageIcon = os.path.join(iconsDir, 'save_pictures.jpg')
        saveImage = QtGui.QAction(QtGui.QIcon(saveImageIcon), 'Save', self)
        #saveImage = QtGui.QAction(QtGui.QIcon('save_pictures.jpg'), 'Save', self)
        saveImage.setShortcut('Ctrl+S')
        saveImage.triggered.connect(self.saveImage)
        
        self.toolbar = QtGui.QToolBar()
        self.toolbar.addAction(newPerson)
        self.toolbar.addAction(saveImage)
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolbar)
    
    # Add a central widget with no (default absolute) layout
    def addCentralWidget(self):
        self.centralWidget = CentralWidget(self, self.imageSetId)
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
        self.centralWidget.createQuestionAnswerImages(self.dir)
        if self.ankiWriteSignal:
            self.ankiWriteSignal.emit()       
            
    # Set the signal to be called once writing of images finishes
    def setAnkiWriteSignal(self, signal):
        self.ankiWriteSignal = signal
        
    # Get the imageSetId - the number identifying the folder and the images created
    def getImageSetId(self):
        return self.imageSetId
    
def main():
    app = QtGui.QApplication(sys.argv)
    ex = FaceMap(os.getcwd())
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
