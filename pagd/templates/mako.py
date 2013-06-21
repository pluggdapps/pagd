# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2013 R Pratap Chakravarthy

import io

from   pluggdapps.plugin        import Plugin, implements
import pluggdapps.interfaces

import pagd.interfaces

try    :
    from   mako.template import Template
    from   mako.runtime import Context
    class Mako( Plugin ):
        """Plugin to translate mako templates to html files."""
        implements( pagd.interfaces.ITemplate )

        def __init__( self ):
            self.kwargs = {
                'module_directory' : \
                        self['siteconfig'].get('mako.module_directory', None),
            }

        def render( self, page ):
            mytemplate = Template( page.templatefile, **self.kwargs )
            buf = io.StringIO()
            mytemplate.render_context( Context(buf, **page.context) )
            return buf.getvalue()
except :
    pass

