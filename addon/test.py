import sys
# import the main window object (mw) from ankiqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *

import os

from PyQt4 import QtCore, QtGui
from face_map.AnkiWriter import *
from face_map import FaceMap

faceMap = None
ankiWriter = None

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.
def testFunction():
    faceMapDir = os.path.join(mw.pm.addonFolder(), 'face_map')
    global faceMap
    faceMap = FaceMap.FaceMap(faceMapDir)
    imageSetId = faceMap.getImageSetId()
    imagesDir = unicode(os.path.join(faceMapDir, "images" + str(imageSetId)))
    writeToAnkiWhenImagesReady(imagesDir)

# Once the images are written, we should take those
# files and write cards to Anki   
def writeToAnkiWhenImagesReady(imagesDir):
    global ankiWriter
    ankiWriter = AnkiWriter(imagesDir)
    ankiWriteSignal = ankiWriter.getSignal()
    faceMap.setAnkiWriteSignal(ankiWriteSignal)

    
# create a new menu item, "test"
action = QAction("test", mw)
# set it to call testFunction when it's clicked
mw.connect(action, SIGNAL("triggered()"), testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)