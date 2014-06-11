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
    writeToAnkiWhenImagesReady(imageSetId)

# Once the images are written, we should take those
# files and write cards to Anki   
def writeToAnkiWhenImagesReady(imageSetId):
    global ankiWriter
    ankiWriter = AnkiWriter(imageSetId)
    ankiWriteSignal = ankiWriter.getSignal()
    faceMap.setAnkiWriteSignal(ankiWriteSignal)

# Remove files - cleanup only
def removeFiles():
    pass
    #files = (u'dfA0.png', u'cwQ.png')
    #mw.col.media.removeExisting(files)
    
# create a new menu item, "test"
action = QAction("test", mw)
# set it to call testFunction when it's clicked
mw.connect(action, SIGNAL("triggered()"), testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)