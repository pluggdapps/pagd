# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2013 R Pratap Chakravarthy

"""Helper functions for pagd's layout templates."""

import sys
from   os.path      import dirname, join, isfile

__all__ = [ 'readfile' ]

#---- Generic helper functions.

def readfile( relpath ):
    """Read file from path ``relpath`` relative to calling template."""
    frame = sys._getframe(1)
    filen = frame.f_globals.get('_ttlfile', None)
    if isfile( filen ) :
        f = join( dirname(filen), relpath )
        if isfile( f ) :
            return open(f).read()
    return ''
