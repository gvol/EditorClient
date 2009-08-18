#
#  EditorClientAppDelegate.py
#  EditorClient
#
#  Created by Rob Tillotson on 8/17/09.
#  Copyright 2009 Rob Tillotson. All rights reserved.
#

from Foundation import *
from AppKit import *

from ODBEditorSuite import *
from fourcc import *
from EditorClientWorker import *

class EditorClientAppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, sender):
        NSLog("Application did finish launching.")

    def application_openFiles_(self, app, filenames):
        for fn in filenames:
            NSLog("application:openFiles: %s" % fn)

            evt = NSAppleEventManager.sharedAppleEventManager().currentAppleEvent()
            
            odbserver = evt.paramDescriptorForKeyword_(fourcc(keyFileSender))
            if odbserver is not None:
                odbserver = to_fourcc(odbserver.typeCodeValue())

            odbtoken = evt.paramDescriptorForKeyword_(fourcc(keyFileSenderToken))
            if odbtoken is not None:
                odbtoken = odbtoken.data()

            odbtitle = evt.paramDescriptorForKeyword_(fourcc(keyFileCustomPath))                
            if odbtitle is not None:
                odbtitle = odbtitle.stringValue()
                
            NSLog("ODB server %@, token %@, title %@", odbserver, odbtoken, odbtitle)
                
            thread = EditorClientWorker.alloc().initWithODB(fn, 0, odbserver, odbtoken)
            thread.start()
        
        
