# import the main window object (mw) from ankiqt
from aqt import mw
import os

from PyQt4 import QtCore

from aqt.utils import showInfo
import aqt.progress
from aqt.utils import tooltip
import shutil
from anki import notes

class AnkiWriter(QtCore.QObject):
    writeAnkiSignal = QtCore.pyqtSignal()
    
    def __init__(self, imagesDir, deckName):
        super(AnkiWriter, self).__init__()
        self.imagesDir = imagesDir
        self.deckName = deckName
        
        self.writeAnkiSignal.connect(self.writeToDeck)
        
    def getSignal(self):
        return self.writeAnkiSignal
        
    def writeToDeck(self):
        # Pop up a Progress Dialog
        progress = aqt.progress.ProgressManager(self)
        progress.start(label=_("Adding Cards..."), immediate=True)
        # Add each created image to the media folder
        uniDirName = unicode(self.imagesDir)
        listFiles = os.listdir(uniDirName)
        for fileName in listFiles:
            filePath = unicode(os.path.join(uniDirName, fileName))
            mw.col.media.addFile(filePath)
        
        # Configure so notes are written to selected deck
        deck = mw.col.decks.byName(self.deckName)
        did = deck['id']
        # The crucial data to write a note to a deck is the did of the
        # model (saved as _model in the Note class). Create that here
        model = mw.col.models.byName("Basic")
        model['did'] = did
        
        newCount = 0
        # Create a card (4 images) for each person on the map
        for i in range(0, len(listFiles) / 4):
            qWindow, qPerson, aPerson, aWindow = self.findNoteTuple(listFiles, i)
        
        
            # Create and add the note
            note = notes.Note(mw.col, model)
            print "qWindow: " + qWindow
            print "aPerson: " + aPerson
            note['Front'] = u"<img src='" + qWindow + "'>"
            note['Front'] += u"<img src='" + qPerson + "'>"
            note['Back'] = u"<img src='" + aPerson + "'>"
            note['Back'] += u"<img src='" + aWindow + "'>"
            newCount += mw.col.addNote(note)
        
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
    
