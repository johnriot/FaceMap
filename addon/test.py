# import the main window object (mw) from ankiqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *
from anki.importing import TextImporter

from PyQt4 import QtCore, QtGui

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
    
    # Add the image file to media
    uniFilename = unicode("C:/Users/John/Pictures/arnie.jpg")
    mw.col.media.addFile(uniFilename)
    
    # Create and add the note
    note = mw.col.newNote()
    note['Front'] = u'3'
    note['Back'] = u"<img src='arnie.jpg'>" 
    newCount = mw.col.addNote(note)
    note.flush()
    
    # show the new count
    showInfo("John Card count: %d" % newCount)
    
    # Reset the GUI to show updated card counts etc
    mw.reset()
    

# create a new menu item, "test"
action = QAction("test", mw)
# set it to call testFunction when it's clicked
mw.connect(action, SIGNAL("triggered()"), testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
