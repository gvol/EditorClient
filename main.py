#
#  main.py
#  EditorClient
#
#  Created by Rob Tillotson on 8/17/09.
#  Copyright Wicked Carrot Productions 2009. All rights reserved.
#

#import modules required by application
import objc
import Foundation
import AppKit

from PyObjCTools import AppHelper

# import modules containing classes required to start application and load MainMenu.nib
import EditorClientAppDelegate

# pass control to AppKit
AppHelper.runEventLoop()
