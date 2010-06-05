#
#  EditorClientWorker.py
#  EditorClient
#
#  Created by Rob Tillotson on 8/17/09.
#  Copyright (c) 2009 Rob Tillotson. All rights reserved.
#

from Foundation import *
from AppKit import *

from fourcc import *
from ODBEditorSuite import *

import subprocess, os

# Kind of wish we could do this with cocoa, but oh well
from aetypes import *
from aepack import pack
from Carbon import AE
from Carbon import AppleEvents
import Carbon.File

if os.getenv('EDITOR_CLIENT_COMMAND'):
    EDITOR_COMMAND = os.getenv('EDITOR_CLIENT_COMMAND')
elif os.getenv('EMACSCLIENT'):
    EDITOR_COMMAND = "%s -c -a '%s' +%%(linenum)s '%%(filename)s'" % (os.getenv('EMACSCLIENT'), os.getenv('EMACS'))
else:
    EDITOR_COMMAND = "/Applications/Emacs.app/Contents/MacOS/bin/emacsclient -c -a '' +%(linenum)s '%(filename)s'"

NSLog('EDITOR_COMMAND: %s', EDITOR_COMMAND )

class EditorClientWorker(NSThread):
    def initWithODB(self, path, linenum=0, odb_app=None, odb_token=None):
        self = super(EditorClientWorker, self).init()
        self.path = path
        self.linenum = linenum
        self.odb_app = odb_app
        self.odb_token = odb_token
        return self

    def main(self):
        pool = NSAutoreleasePool.alloc().init()
        NSLog("editing thread started for %s" % self.path)
        NSLog("shell command: %@", EDITOR_COMMAND % {'linenum': self.linenum, 'filename': self.path})

        stdin = open('/dev/null','r')
        stdout = open('/dev/null','w')
        subprocess.call(EDITOR_COMMAND % {'linenum': self.linenum, 'filename': self.path},
                        shell=True, stdin=stdin, stdout=stdout, stderr=stdout)
        #os.system(EDITOR_COMMAND % {'linenum':self.linenum, 'filename':self.path})

        # Send the "file closed" ODB event.
        if self.odb_app:
            NSLog("sending file closed event to %s, %s" % (self.odb_app, type(self.odb_app)))

            target = AE.AECreateDesc(AppleEvents.typeApplSignature, self.odb_app[::-1])  # For strange endianness reasons, have to reverse this
            event = AE.AECreateAppleEvent(kODBEditorSuite, kAEClosedFile, target, AppleEvents.kAutoGenerateReturnID, AppleEvents.kAnyTransactionID)

            if self.odb_token:
                event.AEPutParamDesc(keySenderToken, pack(self.odb_token, typeWildcard))

            fsr = Carbon.File.FSPathMakeRef(self.path)[0]
            event.AEPutParamDesc(AppleEvents.keyDirectObject, pack(fsr))

            event.AESend(AppleEvents.kAENoReply, AppleEvents.kAENormalPriority, AppleEvents.kAEDefaultTimeout)

            #evt_app = NSAppleEventDescriptor.descriptorWithTypeCode_(fourcc(self.odb_app))
            #evt = NSAppleEventDescriptor.appleEventWithEventClass_eventID_targetDescriptor_returnID_transactionID_(fourcc(kODBEditorSuite),
            #                                                                                                       fourcc(kAEClosedFile),
            #                                                                                                       evt_app,
            #                                                                                                       -1, # kAutoGenerateReturnID
            #                                                                                                       0) # kAnyTransactionID
            #if self.odb_token:
            #    evt_tok = NSAppleEventDescriptor.descriptorWithDescriptorType_data_(fourcc('****'), self.odb_token)
            #    evt.setParamDescriptor_forKeyword_(evt_tok, fourcc(keySenderToken))
            #
            #fsr = objc.FSRef.from_pathname(self.path).data
            #evt_path = NSAppleEventDescriptor.descriptorWithDescriptorType_bytes_length_(fourcc('fsrf'),fsr,len(fsr))
            #evt.setParamDescriptor_forKeyword_(evt_path, fourcc('----'))

        NSLog("editing thread finished for %s" % self.path)
        del pool

