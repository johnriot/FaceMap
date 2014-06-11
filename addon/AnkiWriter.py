# import the main window object (mw) from ankiqt
from aqt import mw
import os

from PyQt4 import QtCore

from aqt.utils import showInfo
import aqt.progress
from aqt.utils import tooltip
import shutil

class AnkiWriter(QtCore.QObject):
    writeAnkiSignal = QtCore.pyqtSignal()
    
    def __init__(self, imagesDir):
        super(AnkiWriter, self).__init__()
        self.imagesDir = imagesDir
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
        # Direct the code where to go when we get an emit() on this signal
        self.writeAnkiSignal.connect(self.writeToDeck)
        
    def getSignal(self):
        return self.writeAnkiSignal
        
    def writeToDeck(self):
        # Pop up a Progress Dialog
        progress = aqt.progress.ProgressManager(self)
        progress.start(label=_("Adding Cards..."), immediate=True)
        # Add each created image to the media folder
        # TODO: Must change to os.path for Unix compatibility
        uniDirName = unicode(self.imagesDir)
        listFiles = os.listdir(uniDirName)
        for fileName in listFiles:
            filePath = unicode(os.path.join(uniDirName, fileName))
            mw.col.media.addFile(filePath)
        
        newCount = 0
        # Create a card (4 images) for each person on the map
        for i in range(0, len(listFiles) / 4):
            qWindow, qPerson, aPerson, aWindow = self.findNoteTuple(listFiles, i)
        
        
            # Create and add the note
            note = mw.col.newNote()
            print "qWindow: " + qWindow
            print "aPerson: " + aPerson
            note['Front'] = u"<img src='" + qWindow + "'>"
            note['Front'] += u"<img src='" + qPerson + "'>"
            note['Back'] = u"<img src='" + aPerson + "'>"
            note['Back'] += u"<img src='" + aWindow + "'>"
            newCount += mw.col.addNote(note)
            note.flush()
        
        progress.finish()
        # Popup to tell users that cards were added
        tooltip(_("Added %d Notes" % newCount), period=2000)
        
        # Remove images folder
        shutil.rmtree(self.imagesDir)
        
        # Reset the GUI to show updated card counts etc
        mw.reset()


    # Find a tuple for the new note to be added
    def findNoteTuple(self, listFiles, indx):
        for fn in listFiles:
            fileString = str(fn)
            
            if(fileString.endswith('cwQ' + str(indx) + '.png')):
                qWindow = fn
            elif(fileString.endswith('dfQ' + str(indx) + '.png')):
                qPerson = fn
            elif(fileString.endswith('dfA' + str(indx) + '.png')):
                aPerson = fn
            elif(fileString.endswith('cwA' + str(indx) + '.png')):
                aWindow = fn
            
        # Make a tuple for the new note
        #showInfo("noteTuple: %s, %s, %s, %s"  % (qWindow, qPerson, aPerson, aWindow))
        return qWindow, qPerson, aPerson, aWindow
    
