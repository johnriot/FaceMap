# import the main window object (mw) from ankiqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *
from anki.importing import TextImporter

from PyQt4 import QtCore, QtGui

from os import *
from os.path import *

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def testFunction():
    # select deck. mw is a global initialised in __init__.py
    # col is in collection.py. decks is in decks.py
    did = mw.col.decks.id("TestDeck")
    mw.col.decks.select(did)
    # set note type for deck. models is in models.py
    m = mw.col.models.byName("Basic")
    deck = mw.col.decks.get(did)
    # Deck is a dict description of values for the deck, next line specifies the model id
    deck['mid'] = m['id']
    mw.col.decks.save(deck)    
    
    # Add each created image to the media folder
    # TODO: Must change to os.path for Unix compatibility
    uniDirName = unicode("C:/Users/John/workspace/PythonScripts/FaceMap/images")
    listFiles = os.listdir(uniDirName)
    for fileName in listFiles:
        filePath = unicode(os.path.join(uniDirName, fileName))
        mw.col.media.addFile(filePath)
    
    
    # Find an image map
    for i in range(0, len(listFiles) / 4):
        qWindow, qPerson, aPerson, aWindow = findNoteTuple(listFiles, i)
    
    
        # Create and add the note
        note = mw.col.newNote()
        print "qWindow: " + qWindow
        print "aPerson: " + aPerson
        note['Front'] = u"<img src='" + qWindow + "'>"
        note['Front'] += u"<img src='" + qPerson + "'>"
        note['Back'] = u"<img src='" + aPerson + "'>"
        note['Back'] += u"<img src='" + aWindow + "'>"
        newCount = mw.col.addNote(note)
        note.flush()
    
    # Reset the GUI to show updated card counts etc
    mw.reset()

# Find a tuple for the new note to be added
def findNoteTuple(listFiles, indx):
    for fn in listFiles:
        fileString = str(fn)
        
        if(fileString.startswith('cwQ' + str(indx))):
            qWindow = fn
        elif(fileString.startswith('dfQ' + str(indx))):
            qPerson = fn
        elif(fileString.startswith('dfA' + str(indx))):
            aPerson = fn
        elif(fileString.startswith('cwA' + str(indx))):
            aWindow = fn
        
            
    # Make a tuple for the new note
    #showInfo("noteTuple: %s, %s, %s, %s"  % (qWindow, qPerson, aPerson, aWindow))
    return qWindow, qPerson, aPerson, aWindow
    

# create a new menu item, "test"
action = QAction("test", mw)
# set it to call testFunction when it's clicked
mw.connect(action, SIGNAL("triggered()"), testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
