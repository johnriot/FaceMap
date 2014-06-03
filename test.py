import sys
from PyQt4 import QtGui, QtCore
from DragLabel import *
from CentralWidget import *

class Test(QtGui.QMainWindow):
    def __init__(self):
        super(Test, self).__init__()
        self.initUI()
        self.centralWidget = CentralWidget()
        # self.centralWidget = QtGui.QWidget()
        self.setCentralWidget(self.centralWidget)
        self.chooseFiles()
    
    def initUI(self):
        self.setGeometry(100, 100, 600, 400)
        self.show()
      
    # Create a file-chooser dialog to pick images
    def chooseFiles(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
                '/home', 'Image Files (*.png *.jpg *.bmp, *gif)')
        # self.label = QtGui.QLabel(self)
        label = DragLabel(self)
        #self.setCentralWidget(self.label)
        #self.centralWidget().addWidget(label)
        #image = QtGui.QPixmap(fname)
        #self.label.setPixmap(image)
        self.centralWidget.addDraggableImage(fname)
        
  
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Test()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    
