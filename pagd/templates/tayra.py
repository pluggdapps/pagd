# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2013 R Pratap Chakravarthy

from   pluggdapps.plugin        import Plugin, implements
import pluggdapps.utils         as h

import pagd.interfaces
import pluggdapps.interfaces

class Tayra( Plugin ):
    """Plugin to translate tayra templates to html files."""
    implements( pagd.interfaces.ITemplate )

    def __init__( self ):
        self.siteconfig = self['siteconfig'] if 'siteconfig' in self else {}
        setts = h.settingsfor( 'tayra.ttlcompiler.', self.siteconfig )
        setts.update( debug=True )
        self.ttlplugin = self.qp(
                pluggdapps.interfaces.ITemplate, 'tayra.TTLCompiler',
                settings=setts )
        
    def render( self, page ):
        return self.ttlplugin.render( page.context, file=page.templatefile )
