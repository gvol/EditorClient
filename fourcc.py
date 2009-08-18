#
#  fourcc.py
#  EditorClient
#
#  Created by Rob Tillotson on 8/17/09.
#  Copyright (c) 2009 Wicked Carrot Productions. All rights reserved.
#

import struct

def fourcc(s):
    return struct.unpack('>l',s)[0]

def to_fourcc(i):
    return struct.pack('>l',i)
