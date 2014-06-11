import sys
# import the main window object (mw) from ankiqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *
# Allow to hook into file
from anki import hooks

from resources import *

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
  
# Called from the 'setupEditorButtons' hook from Anki
def add_face_map_button(ed):
    ed._addButton("new_person", testFunction,
            key="Alt+f", tip = "FaceMap", size=False,
            native=True, canDisable=False)

# Hook to add a button for FaceMap
hooks.addHook('setupEditorButtons', add_face_map_button)
