# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2013 R Pratap Chakravarthy

"""Pagd is static web site creator based on pluggdapps component system - it
can be extended in many ways."""
    
__version__ = '0.2dev'


def package( pa ) :
    """Pluggdapps package must implement this entry point. This function
    will be called during platform pre-booting."""
    return {
    }

import pagd.interfaces  # Interface specifications defined by this package.
import pagd.commands    # Sub-commands for command line script.
import pagd.contents    # Contain content translation plugins.
import pagd.contexts    # Contain IXContext plugins for external context.
import pagd.layouts     # Contain layout plugins
import pagd.templates   # Contain template plugins
import pagd.rst         # Contain directives for reStructuredText

